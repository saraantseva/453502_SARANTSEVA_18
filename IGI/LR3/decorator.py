import time

def timer(func):
    """
    Decorator that measures function execution time.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start:.6f} seconds")
        return result
    return wrapper

def logger(func):
    """
    Decorator that logs function calls.
    """
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper