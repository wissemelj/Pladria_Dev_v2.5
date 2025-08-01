"""
OTA Update Manager for Pladria v2.5
Handles automatic updates with GitHub releases integration
"""

import os
import sys
import json
import hashlib
import zipfile
import shutil
import tempfile
import threading
import subprocess
from pathlib import Path
from typing import Dict, Optional, Callable, Tuple, List
import logging

try:
    import requests
    from packaging import version
except ImportError:
    requests = None
    version = None

from config.constants import AppInfo
from utils.file_utils import get_resource_path

logger = logging.getLogger(__name__)


class UpdateConfig:
    """Configuration for the update system"""

    # GitHub repository information
    GITHUB_OWNER = "wissemelj"  # Replace with actual owner
    GITHUB_REPO = "Pladria_Dev_v2.5"  # Replace with actual repo

    # GitHub token for private repositories (optional)
    GITHUB_TOKEN = None  # Set this if repository is private

    # Update server URLs
    GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    
    # Update settings
    CHECK_INTERVAL_HOURS = 24  # Check for updates every 24 hours
    DOWNLOAD_TIMEOUT = 300  # 5 minutes timeout for downloads
    CHUNK_SIZE = 8192  # Download chunk size
    
    # File patterns for updates
    UPDATE_PACKAGE_PATTERN = "Pladria-v{version}-update.zip"
    FULL_PACKAGE_PATTERN = "Pladria-v{version}-full.zip"
    
    # Backup settings
    BACKUP_FOLDER = "backup"
    MAX_BACKUPS = 3


class UpdateInfo:
    """Information about an available update"""
    
    def __init__(self, version_str: str, download_url: str, release_notes: str = "", 
                 file_size: int = 0, checksum: str = "", is_critical: bool = False):
        self.version = version_str
        self.download_url = download_url
        self.release_notes = release_notes
        self.file_size = file_size
        self.checksum = checksum
        self.is_critical = is_critical
        
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'version': self.version,
            'download_url': self.download_url,
            'release_notes': self.release_notes,
            'file_size': self.file_size,
            'checksum': self.checksum,
            'is_critical': self.is_critical
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UpdateInfo':
        """Create from dictionary"""
        return cls(
            version_str=data.get('version', ''),
            download_url=data.get('download_url', ''),
            release_notes=data.get('release_notes', ''),
            file_size=data.get('file_size', 0),
            checksum=data.get('checksum', ''),
            is_critical=data.get('is_critical', False)
        )


class UpdateManager:
    """Main update manager class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_version = AppInfo.VERSION
        self.update_in_progress = False
        self.download_progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        
        # Paths
        self.app_dir = self._get_app_directory()
        self.backup_dir = os.path.join(self.app_dir, UpdateConfig.BACKUP_FOLDER)
        self.temp_dir = tempfile.mkdtemp(prefix="pladria_update_")
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
        
        self.logger.info(f"UpdateManager initialized - Current version: {self.current_version}")
    
    def _get_app_directory(self) -> str:
        """Get the application directory"""
        try:
            # PyInstaller mode
            return os.path.dirname(sys.executable)
        except:
            # Development mode
            return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    def set_progress_callback(self, callback: Callable[[int, str], None]):
        """Set callback for progress updates"""
        self.download_progress_callback = callback
    
    def set_status_callback(self, callback: Callable[[str], None]):
        """Set callback for status updates"""
        self.status_callback = callback
    
    def _update_status(self, message: str):
        """Update status with callback"""
        self.logger.info(message)
        if self.status_callback:
            self.status_callback(message)
    
    def _update_progress(self, progress: int, message: str = ""):
        """Update progress with callback"""
        if self.download_progress_callback:
            self.download_progress_callback(progress, message)
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are available"""
        if requests is None:
            self.logger.error("requests library not available")
            return False
        if version is None:
            self.logger.error("packaging library not available")
            return False
        return True
    
    def check_for_updates(self) -> Optional[UpdateInfo]:
        """
        Check for available updates from GitHub releases

        Returns:
            UpdateInfo if update available, None otherwise
        """
        if not self.check_dependencies():
            self.logger.error("Dependencies not available for update check")
            return None

        try:
            self._update_status("🔍 Vérification des mises à jour...")

            # Try latest release first
            latest_url = UpdateConfig.GITHUB_API_URL
            all_releases_url = f"https://api.github.com/repos/{UpdateConfig.GITHUB_OWNER}/{UpdateConfig.GITHUB_REPO}/releases"

            release_data = None

            # Prepare headers for GitHub API
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Pladria-Update-System'
            }

            # Add authentication if token is provided
            if UpdateConfig.GITHUB_TOKEN:
                headers['Authorization'] = f'token {UpdateConfig.GITHUB_TOKEN}'

            # Method 1: Try to get latest release
            try:
                response = requests.get(
                    latest_url,
                    timeout=30,
                    headers=headers
                )
                if response.status_code == 200:
                    release_data = response.json()
                    self.logger.info("Found latest release")
                else:
                    self.logger.info(f"Latest release API returned {response.status_code}")
            except Exception as e:
                self.logger.info(f"Latest release API failed: {e}")

            # Method 2: If latest fails, try all releases (including pre-releases)
            if not release_data:
                try:
                    self.logger.info("Trying all releases API...")
                    response = requests.get(
                        all_releases_url,
                        timeout=30,
                        headers=headers
                    )
                    response.raise_for_status()

                    all_releases = response.json()
                    if all_releases and len(all_releases) > 0:
                        # Get the most recent release (first in the list)
                        release_data = all_releases[0]
                        self.logger.info(f"Found release from all releases: {release_data.get('tag_name', 'unknown')}")
                    else:
                        self.logger.info("No releases found in repository")

                except Exception as e:
                    self.logger.error(f"All releases API also failed: {e}")

            if not release_data:
                self._update_status("❌ Aucune release trouvée")
                return None
            
            # Extract version information
            latest_version = release_data.get('tag_name', '').lstrip('v')
            release_notes = release_data.get('body', '')
            
            # Compare versions
            if self._is_newer_version(latest_version, self.current_version):
                # Find download URL for update package
                download_url = self._find_download_url(release_data.get('assets', []))
                
                if download_url:
                    # Get file size from assets
                    file_size = self._get_file_size_from_assets(release_data.get('assets', []), download_url)
                    
                    update_info = UpdateInfo(
                        version_str=latest_version,
                        download_url=download_url,
                        release_notes=release_notes,
                        file_size=file_size,
                        is_critical=self._is_critical_update(release_notes)
                    )
                    
                    self._update_status(f"✅ Mise à jour disponible: v{latest_version}")
                    return update_info
                else:
                    self.logger.warning("No suitable download URL found in release assets")
            else:
                self._update_status("✅ Application à jour")
                
        except requests.RequestException as e:
            self.logger.error(f"Network error checking for updates: {e}")
            self._update_status("❌ Erreur réseau lors de la vérification")
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            self._update_status("❌ Erreur lors de la vérification")
        
        return None
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compare version strings"""
        try:
            return version.parse(latest) > version.parse(current)
        except Exception as e:
            self.logger.error(f"Error comparing versions: {e}")
            return False
    
    def _find_download_url(self, assets: List[Dict]) -> Optional[str]:
        """Find the appropriate download URL from release assets"""
        for asset in assets:
            name = asset.get('name', '')
            # Look for update package first, then full package
            if 'update.zip' in name.lower() or 'pladria' in name.lower():
                return asset.get('browser_download_url')
        return None
    
    def _get_file_size_from_assets(self, assets: List[Dict], download_url: str) -> int:
        """Get file size from assets"""
        for asset in assets:
            if asset.get('browser_download_url') == download_url:
                return asset.get('size', 0)
        return 0
    
    def _is_critical_update(self, release_notes: str) -> bool:
        """Determine if update is critical based on release notes"""
        critical_keywords = ['critical', 'security', 'urgent', 'hotfix', 'critique', 'sécurité']
        return any(keyword in release_notes.lower() for keyword in critical_keywords)

    def download_update(self, update_info: UpdateInfo) -> Optional[str]:
        """
        Download update package

        Args:
            update_info: Information about the update to download

        Returns:
            Path to downloaded file if successful, None otherwise
        """
        if self.update_in_progress:
            self.logger.warning("Update already in progress")
            return None

        self.update_in_progress = True

        try:
            self._update_status(f"📥 Téléchargement de la mise à jour v{update_info.version}...")
            self._update_progress(0, "Initialisation du téléchargement...")

            # Create download path
            filename = f"pladria-v{update_info.version}-update.zip"
            download_path = os.path.join(self.temp_dir, filename)

            # Download with progress tracking
            response = requests.get(update_info.download_url, stream=True, timeout=UpdateConfig.DOWNLOAD_TIMEOUT)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', update_info.file_size or 0))
            downloaded = 0

            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=UpdateConfig.CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self._update_progress(progress, f"Téléchargé: {downloaded // 1024} KB / {total_size // 1024} KB")

            # Verify download
            if os.path.exists(download_path):
                file_size = os.path.getsize(download_path)
                self._update_status(f"✅ Téléchargement terminé ({file_size // 1024} KB)")

                # Verify checksum if provided
                if update_info.checksum:
                    if self._verify_checksum(download_path, update_info.checksum):
                        self._update_status("✅ Vérification de l'intégrité réussie")
                    else:
                        self._update_status("❌ Échec de la vérification de l'intégrité")
                        os.remove(download_path)
                        return None

                return download_path
            else:
                self._update_status("❌ Échec du téléchargement")
                return None

        except requests.RequestException as e:
            self.logger.error(f"Download error: {e}")
            self._update_status("❌ Erreur de téléchargement")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during download: {e}")
            self._update_status("❌ Erreur inattendue")
            return None
        finally:
            self.update_in_progress = False

    def _verify_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Verify file checksum"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)

            calculated_checksum = sha256_hash.hexdigest()
            return calculated_checksum.lower() == expected_checksum.lower()
        except Exception as e:
            self.logger.error(f"Error verifying checksum: {e}")
            return False

    def create_backup(self) -> bool:
        """Create backup of current application"""
        try:
            self._update_status("💾 Création de la sauvegarde...")

            # Create backup filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"pladria_v{self.current_version}_{timestamp}"
            backup_path = os.path.join(self.backup_dir, backup_name)

            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)

            # Copy essential files
            essential_files = [
                "Pladria.exe",
                "Icone_App.png",
                "Icone_App_Sharp.ico",
                "logo_Sofrecom.png",
                "Background.png"
            ]

            for file_name in essential_files:
                src_path = os.path.join(self.app_dir, file_name)
                if os.path.exists(src_path):
                    dst_path = os.path.join(backup_path, file_name)
                    shutil.copy2(src_path, dst_path)

            # Copy any additional directories that might exist
            for item in os.listdir(self.app_dir):
                item_path = os.path.join(self.app_dir, item)
                if os.path.isdir(item_path) and item not in ['backup', '__pycache__']:
                    dst_path = os.path.join(backup_path, item)
                    shutil.copytree(item_path, dst_path, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))

            # Clean old backups
            self._cleanup_old_backups()

            self._update_status("✅ Sauvegarde créée avec succès")
            self.logger.info(f"Backup created at: {backup_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            self._update_status("❌ Erreur lors de la sauvegarde")
            return False

    def _cleanup_old_backups(self):
        """Remove old backups to save space"""
        try:
            backups = []
            for item in os.listdir(self.backup_dir):
                item_path = os.path.join(self.backup_dir, item)
                if os.path.isdir(item_path):
                    backups.append((item_path, os.path.getctime(item_path)))

            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x[1], reverse=True)

            # Remove old backups
            for backup_path, _ in backups[UpdateConfig.MAX_BACKUPS:]:
                shutil.rmtree(backup_path)
                self.logger.info(f"Removed old backup: {backup_path}")

        except Exception as e:
            self.logger.error(f"Error cleaning up old backups: {e}")

    def install_update(self, update_package_path: str) -> bool:
        """
        Install the downloaded update

        Args:
            update_package_path: Path to the downloaded update package

        Returns:
            True if installation successful, False otherwise
        """
        try:
            self._update_status("🔧 Installation de la mise à jour...")

            # Extract update package
            extract_path = os.path.join(self.temp_dir, "extracted")
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(update_package_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            self._update_status("📦 Extraction terminée")

            # Apply updates
            if self._apply_update_files(extract_path):
                self._update_status("✅ Mise à jour installée avec succès")
                return True
            else:
                self._update_status("❌ Échec de l'installation")
                return False

        except zipfile.BadZipFile:
            self.logger.error("Invalid zip file")
            self._update_status("❌ Fichier de mise à jour corrompu")
            return False
        except Exception as e:
            self.logger.error(f"Error installing update: {e}")
            self._update_status("❌ Erreur lors de l'installation")
            return False

    def _apply_update_files(self, extract_path: str) -> bool:
        """Apply extracted update files to application directory"""
        try:
            # Look for update manifest or apply all files
            for root, dirs, files in os.walk(extract_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, extract_path)
                    dst_file = os.path.join(self.app_dir, rel_path)

                    # Create destination directory if needed
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                    # Copy file
                    shutil.copy2(src_file, dst_file)
                    self.logger.debug(f"Updated file: {rel_path}")

            return True
        except Exception as e:
            self.logger.error(f"Error applying update files: {e}")
            return False

    def rollback_update(self) -> bool:
        """Rollback to previous version using backup"""
        try:
            self._update_status("🔄 Restauration de la version précédente...")

            # Find most recent backup
            backups = []
            for item in os.listdir(self.backup_dir):
                item_path = os.path.join(self.backup_dir, item)
                if os.path.isdir(item_path):
                    backups.append((item_path, os.path.getctime(item_path)))

            if not backups:
                self._update_status("❌ Aucune sauvegarde trouvée")
                return False

            # Get most recent backup
            latest_backup = max(backups, key=lambda x: x[1])[0]

            # Restore files from backup
            for root, dirs, files in os.walk(latest_backup):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, latest_backup)
                    dst_file = os.path.join(self.app_dir, rel_path)

                    # Create destination directory if needed
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                    # Copy file
                    shutil.copy2(src_file, dst_file)

            self._update_status("✅ Restauration terminée")
            return True

        except Exception as e:
            self.logger.error(f"Error during rollback: {e}")
            self._update_status("❌ Erreur lors de la restauration")
            return False

    def restart_application(self):
        """Restart the application after update"""
        try:
            self._update_status("🔄 Redémarrage de l'application...")

            # Get current executable path
            if getattr(sys, 'frozen', False):
                # PyInstaller executable
                exe_path = sys.executable
            else:
                # Development mode - restart Python script
                exe_path = sys.executable
                script_path = os.path.join(self.app_dir, "src", "main.py")
                subprocess.Popen([exe_path, script_path])
                return

            # Start new instance
            subprocess.Popen([exe_path])

            # Exit current instance
            sys.exit(0)

        except Exception as e:
            self.logger.error(f"Error restarting application: {e}")
            self._update_status("❌ Erreur lors du redémarrage")

    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.logger.debug("Temporary files cleaned up")
        except Exception as e:
            self.logger.error(f"Error cleaning up temporary files: {e}")

    def __del__(self):
        """Cleanup on destruction"""
        self.cleanup()


class UpdateScheduler:
    """Handles scheduled update checks"""

    def __init__(self, update_manager: UpdateManager):
        self.update_manager = update_manager
        self.check_timer = None
        self.logger = logging.getLogger(__name__)

    def start_periodic_checks(self, interval_hours: int = UpdateConfig.CHECK_INTERVAL_HOURS):
        """Start periodic update checks"""
        def check_updates():
            try:
                update_info = self.update_manager.check_for_updates()
                if update_info:
                    self.logger.info(f"Update available: v{update_info.version}")
                    # Trigger notification (will be handled by UI)
            except Exception as e:
                self.logger.error(f"Error in scheduled update check: {e}")

            # Schedule next check
            self.check_timer = threading.Timer(interval_hours * 3600, check_updates)
            self.check_timer.daemon = True
            self.check_timer.start()

        # Start first check
        check_updates()

    def stop_periodic_checks(self):
        """Stop periodic update checks"""
        if self.check_timer:
            self.check_timer.cancel()
            self.check_timer = None
