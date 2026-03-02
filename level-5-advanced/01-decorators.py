"""
Level 5 - Exercise 01: Decorators
==================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Learn to create and use Python decorators -- functions that wrap other
functions to extend their behaviour without modifying the original code.

Exercises
---------
1. timing_decorator   - Measures and prints execution time of a function.
2. retry_decorator    - Retries a function up to N times on exception.
3. memoize_decorator  - Caches results of expensive function calls.
4. logging_decorator  - Logs function name, arguments, and return value.

Expected output (approximate):
------------------------------
# timing_decorator
# >>> slow_add(2, 3)
# slow_add took 1.0012s
# 5

# retry_decorator
# >>> flaky_function()
# Attempt 1 failed: Random failure
# Attempt 2 failed: Random failure
# Attempt 3 succeeded!
# "Success"

# memoize_decorator
# >>> fibonacci(35)  # first call is slow, second is instant
# 9227465

# logging_decorator
# >>> multiply(3, 4)
# Calling multiply(3, 4)
# multiply returned 12
# 12
"""

import time
import functools
import random


# ---------------------------------------------------------------------------
# 1. Timing Decorator
# ---------------------------------------------------------------------------
def timing(func):
    """Decorator that prints how long a function took to execute.

    Usage:
        @timing
        def slow_add(a, b):
            time.sleep(1)
            return a + b
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


# ---------------------------------------------------------------------------
# 2. Retry Decorator
# ---------------------------------------------------------------------------
def retry(max_attempts=3, delay=0.1):
    """Decorator that retries a function up to *max_attempts* times.

    If the function raises an exception, wait *delay* seconds and try again.
    After all attempts are exhausted the last exception is re-raised.

    Usage:
        @retry(max_attempts=5, delay=0.5)
        def unreliable():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    print(f"Attempt {attempt} succeeded!")
                    return result
                except Exception as exc:
                    last_exception = exc
                    print(f"Attempt {attempt} failed: {exc}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# 3. Memoize Decorator
# ---------------------------------------------------------------------------
def memoize(func):
    """Decorator that caches return values keyed by positional arguments.

    Subsequent calls with the same arguments return the cached result
    instead of re-executing the function.

    Usage:
        @memoize
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    wrapper.cache = cache          # expose for inspection / clearing
    return wrapper


# ---------------------------------------------------------------------------
# 4. Logging Decorator
# ---------------------------------------------------------------------------
def logging_decorator(func):
    """Decorator that logs the function call and its return value.

    Prints the function name and arguments before calling, and the
    return value after the call completes.

    Usage:
        @logging_decorator
        def multiply(a, b):
            return a * b
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = ", ".join(
            [repr(a) for a in args]
            + [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"Calling {func.__name__}({args_repr})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    # --- 1. Timing ---
    print("=" * 50)
    print("1. Timing Decorator")
    print("=" * 50)

    @timing
    def slow_add(a, b):
        time.sleep(0.3)
        return a + b

    result = slow_add(2, 3)
    print(f"Result: {result}\n")

    # --- 2. Retry ---
    print("=" * 50)
    print("2. Retry Decorator")
    print("=" * 50)

    call_count = 0

    @retry(max_attempts=4, delay=0.05)
    def flaky_function():
        global call_count
        call_count += 1
        if call_count < 3:
            raise RuntimeError("Random failure")
        return "Success"

    result = flaky_function()
    print(f"Result: {result}\n")

    # --- 3. Memoize ---
    print("=" * 50)
    print("3. Memoize Decorator")
    print("=" * 50)

    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    start = time.perf_counter()
    fib_35 = fibonacci(35)
    first_call = time.perf_counter() - start

    start = time.perf_counter()
    fib_35_again = fibonacci(35)
    second_call = time.perf_counter() - start

    print(f"fibonacci(35) = {fib_35}")
    print(f"First call:  {first_call:.6f}s")
    print(f"Second call: {second_call:.6f}s  (cached)\n")

    # --- 4. Logging ---
    print("=" * 50)
    print("4. Logging Decorator")
    print("=" * 50)

    @logging_decorator
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)
    print(f"Result: {result}")
