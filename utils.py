import time

def runner(func):
    def wrapper(*args):
        start = time.perf_counter_ns()
        result = func(*args)
        end = time.perf_counter_ns()
        execution_time = end - start
        print(f"Function '{func.__name__}' took {(1e-6 * execution_time):.3f} ms to execute "
              f"and the result is: {result}")
        return result
    return wrapper
