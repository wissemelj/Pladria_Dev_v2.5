"""
Performance optimization utilities.
"""

import time
import threading
import logging
from typing import Callable, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and optimize application performance."""
    
    def __init__(self):
        """Initialize the performance monitor."""
        self.metrics = {}
        self.thresholds = {
            'file_read': 2.0,      # seconds
            'data_process': 1.0,   # seconds
            'ui_update': 0.1,      # seconds
            'excel_generate': 5.0  # seconds
        }
    
    def time_operation(self, operation_name: str):
        """Decorator to time operations."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    
                    # Log performance
                    self._log_performance(operation_name, duration)
                    
                    # Store metrics
                    if operation_name not in self.metrics:
                        self.metrics[operation_name] = []
                    self.metrics[operation_name].append(duration)
                    
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    logger.error(f"Operation '{operation_name}' failed after {duration:.2f}s: {e}")
                    raise
            return wrapper
        return decorator
    
    def _log_performance(self, operation: str, duration: float):
        """Log performance information."""
        threshold = self.thresholds.get(operation, 1.0)
        
        if duration > threshold:
            logger.warning(f"Slow operation: {operation} took {duration:.2f}s (threshold: {threshold}s)")
        else:
            logger.debug(f"Performance: {operation} completed in {duration:.2f}s")
    
    def get_average_time(self, operation_name: str) -> Optional[float]:
        """Get average time for an operation."""
        if operation_name in self.metrics and self.metrics[operation_name]:
            return sum(self.metrics[operation_name]) / len(self.metrics[operation_name])
        return None


class AsyncTaskManager:
    """Manage asynchronous tasks for better UI responsiveness."""
    
    def __init__(self):
        """Initialize the task manager."""
        self.active_tasks = {}
        self.task_counter = 0
    
    def run_async(self, 
                  task_func: Callable,
                  callback: Optional[Callable] = None,
                  error_callback: Optional[Callable] = None,
                  task_name: str = None) -> str:
        """
        Run a task asynchronously.
        
        Args:
            task_func: Function to run asynchronously
            callback: Function to call when task completes successfully
            error_callback: Function to call when task fails
            task_name: Name for the task (for logging)
            
        Returns:
            Task ID
        """
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        
        if task_name is None:
            task_name = task_id
        
        def worker():
            try:
                logger.debug(f"Starting async task: {task_name}")
                result = task_func()
                
                if callback:
                    callback(result)
                
                logger.debug(f"Async task completed: {task_name}")
                
            except Exception as e:
                logger.error(f"Async task failed: {task_name} - {e}")
                
                if error_callback:
                    error_callback(e)
            
            finally:
                # Clean up
                if task_id in self.active_tasks:
                    del self.active_tasks[task_id]
        
        # Start the task
        thread = threading.Thread(target=worker, daemon=True)
        self.active_tasks[task_id] = {
            'thread': thread,
            'name': task_name,
            'start_time': time.time()
        }
        
        thread.start()
        return task_id
    
    def is_task_running(self, task_id: str) -> bool:
        """Check if a task is still running."""
        return task_id in self.active_tasks and self.active_tasks[task_id]['thread'].is_alive()
    
    def get_active_tasks(self) -> list:
        """Get list of active task names."""
        return [task['name'] for task in self.active_tasks.values() 
                if task['thread'].is_alive()]


class MemoryOptimizer:
    """Optimize memory usage."""
    
    @staticmethod
    def clear_dataframe_memory(df):
        """Optimize DataFrame memory usage."""
        if df is None:
            return None
        
        try:
            # Convert object columns to category if they have few unique values
            for col in df.select_dtypes(include=['object']).columns:
                if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
                    df[col] = df[col].astype('category')
            
            # Downcast numeric types
            for col in df.select_dtypes(include=['int']).columns:
                df[col] = df[col].astype('int32')
            
            for col in df.select_dtypes(include=['float']).columns:
                df[col] = df[col].astype('float32')
            
            return df
        except Exception as e:
            logger.warning(f"Memory optimization failed: {e}")
            return df
    



# Global instances
performance_monitor = PerformanceMonitor()
async_task_manager = AsyncTaskManager()
memory_optimizer = MemoryOptimizer()


def timed_operation(operation_name: str):
    """Decorator for timing operations."""
    return performance_monitor.time_operation(operation_name)


def run_async_task(task_func: Callable, 
                   callback: Optional[Callable] = None,
                   error_callback: Optional[Callable] = None,
                   task_name: str = None) -> str:
    """Run a task asynchronously."""
    return async_task_manager.run_async(task_func, callback, error_callback, task_name)


def optimize_dataframe_memory(df):
    """Optimize DataFrame memory usage."""
    return memory_optimizer.clear_dataframe_memory(df)
