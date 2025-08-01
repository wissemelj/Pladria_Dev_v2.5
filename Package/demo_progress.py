#!/usr/bin/env python3
"""
Demo script to showcase the progress bar functionality
"""

import time
from build_and_package import ProgressBar

def demo_progress_bar():
    """Demonstrate progress bar with time estimation"""
    print("🎯 Demo: Progress Bar with Time Estimation")
    print("=" * 50)
    
    progress = ProgressBar(total_steps=20, width=50)
    progress.start("Starting demo process...")
    
    # Simulate different speed steps
    steps = [
        ("Initializing...", 0.2),
        ("Loading configuration...", 0.3),
        ("Checking dependencies...", 0.1),
        ("Installing packages...", 0.5),
        ("Compiling code...", 0.8),
        ("Running tests...", 0.4),
        ("Creating package...", 0.6),
        ("Calculating checksums...", 0.3),
        ("Uploading files...", 0.7),
        ("Finalizing...", 0.2)
    ]
    
    step_num = 0
    for desc, delay in steps:
        for i in range(2):  # 2 sub-steps per main step
            step_num += 1
            progress.update(step_num, f"{desc} ({i+1}/2)")
            time.sleep(delay)
    
    progress.finish("🎉 Demo completed successfully!")
    print()

def demo_spinner():
    """Demonstrate spinner for indeterminate tasks"""
    print("🌀 Demo: Spinner for Indeterminate Tasks")
    print("=" * 50)
    
    spinner = ProgressBar()
    
    tasks = [
        ("Connecting to server...", 2),
        ("Authenticating...", 1.5),
        ("Downloading data...", 3),
        ("Processing results...", 2.5)
    ]
    
    for desc, duration in tasks:
        spinner.spinner_start(desc)
        time.sleep(duration)
        spinner.finish(f"✅ {desc.replace('...', '')} complete")
        time.sleep(0.5)  # Brief pause between tasks
    
    print()

def demo_mixed_operations():
    """Demonstrate mixed progress bar and spinner operations"""
    print("🔄 Demo: Mixed Progress and Spinner Operations")
    print("=" * 50)
    
    # Start with a progress bar
    progress = ProgressBar(total_steps=10, width=40)
    progress.start("Phase 1: Deterministic operations...")
    
    for i in range(1, 6):
        progress.update(i, f"Processing item {i}/5...")
        time.sleep(0.5)
    
    progress.update(5, "Phase 1 complete, switching to indeterminate...")
    time.sleep(1)
    progress.finish("Phase 1 completed")
    
    # Switch to spinner for unknown duration
    spinner = ProgressBar()
    spinner.spinner_start("Phase 2: Network operations (unknown duration)...")
    time.sleep(3)
    spinner.finish("Phase 2 completed")
    
    # Back to progress bar
    progress2 = ProgressBar(total_steps=5, width=40)
    progress2.start("Phase 3: Final steps...")
    
    for i in range(1, 6):
        progress2.update(i, f"Finalizing step {i}/5...")
        time.sleep(0.3)
    
    progress2.finish("🎉 All phases completed!")
    print()

def main():
    """Run all demos"""
    print("🚀 Progress Bar System Demo")
    print("=" * 60)
    print("This demo showcases the advanced progress bar system")
    print("with time estimation and visual feedback.")
    print()
    
    input("Press Enter to start Demo 1 (Progress Bar)...")
    demo_progress_bar()
    
    input("Press Enter to start Demo 2 (Spinner)...")
    demo_spinner()
    
    input("Press Enter to start Demo 3 (Mixed Operations)...")
    demo_mixed_operations()
    
    print("✅ All demos completed!")
    print("🎯 The progress bar system is ready for use in the build script.")

if __name__ == "__main__":
    main()
