"""
Logging configuration for the Suivi Generator application.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional


def setup_logging(log_level: str = "INFO", 
                 log_to_file: bool = True,
                 log_file_path: Optional[str] = None) -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to a file
        log_file_path: Custom log file path (optional)
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if log_to_file:
        if log_file_path is None:
            # Create logs directory if it doesn't exist
            logs_dir = "logs"
            os.makedirs(logs_dir, exist_ok=True)
            
            # Generate log filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            log_file_path = os.path.join(logs_dir, f"suivi_generator_{timestamp}.log")
        
        try:
            # Use RotatingFileHandler to manage log file size
            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
            
            logging.info(f"Logging to file: {log_file_path}")
            
        except Exception as e:
            logging.warning(f"Failed to set up file logging: {e}")
    
    # Log startup information
    logging.info("=" * 50)
    logging.info("Suivi Generator Application Started")
    logging.info(f"Log level: {log_level}")
    logging.info(f"File logging: {'Enabled' if log_to_file else 'Disabled'}")
    logging.info("=" * 50)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_exception(logger: logging.Logger, message: str = "An error occurred"):
    """
    Log an exception with full traceback.
    
    Args:
        logger: Logger instance
        message: Custom message to include
    """
    logger.exception(message)


def log_performance(logger: logging.Logger, operation: str, duration: float):
    """
    Log performance information.
    
    Args:
        logger: Logger instance
        operation: Description of the operation
        duration: Duration in seconds
    """
    if duration < 1:
        logger.info(f"Performance: {operation} completed in {duration*1000:.1f}ms")
    else:
        logger.info(f"Performance: {operation} completed in {duration:.2f}s")


class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, logger: logging.Logger, operation: str):
        """
        Initialize the performance timer.
        
        Args:
            logger: Logger instance
            operation: Description of the operation being timed
        """
        self.logger = logger
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        """Start timing."""
        import time
        self.start_time = time.time()
        self.logger.debug(f"Starting: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and log results."""
        import time
        if self.start_time is not None:
            duration = time.time() - self.start_time
            if exc_type is None:
                log_performance(self.logger, self.operation, duration)
            else:
                self.logger.error(f"Failed: {self.operation} after {duration:.2f}s")


def configure_third_party_loggers():
    """Configure logging levels for third-party libraries."""
    # Reduce verbosity of common third-party libraries
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('openpyxl').setLevel(logging.WARNING)
    logging.getLogger('pandas').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)


# Example usage functions
def log_file_operation(logger: logging.Logger, operation: str, file_path: str, success: bool = True):
    """
    Log file operations with consistent formatting.
    
    Args:
        logger: Logger instance
        operation: Type of operation (e.g., "loaded", "saved", "deleted")
        file_path: Path to the file
        success: Whether the operation was successful
    """
    filename = os.path.basename(file_path)
    if success:
        logger.info(f"File {operation}: {filename}")
    else:
        logger.error(f"Failed to {operation.lower()} file: {filename}")


def log_data_processing(logger: logging.Logger, operation: str, input_count: int, output_count: int):
    """
    Log data processing operations.
    
    Args:
        logger: Logger instance
        operation: Description of the processing operation
        input_count: Number of input records
        output_count: Number of output records
    """
    if input_count == output_count:
        logger.info(f"{operation}: processed {input_count} records")
    else:
        filtered = input_count - output_count
        logger.info(f"{operation}: processed {input_count} records, filtered {filtered}, output {output_count}")
