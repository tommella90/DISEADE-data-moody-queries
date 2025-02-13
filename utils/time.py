import time

def time_it(func):
    """Decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()  
        result = func(*args, **kwargs) 
        end_time = time.time() 
        elapsed_time = end_time - start_time  
        print(f"Execution time: {elapsed_time:.4f} seconds")  
        return result
    return wrapper