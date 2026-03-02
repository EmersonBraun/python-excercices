"""
Exercise 01 - Fibonacci Sequence
==================================
Level: 2 - Functions & Collections
Difficulty: 2/5
Estimated Time: 15 minutes

Problem:
--------
Implement the Fibonacci sequence using three approaches:
  1. Iterative
  2. Recursive (naive)
  3. Recursive with memoization

The Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
  F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n >= 2

Expected Input/Output:
----------------------
# fibonacci_iterative(10)    -> 55
# fibonacci_recursive(10)    -> 55
# fibonacci_memoized(10)     -> 55
# fibonacci_sequence(8)      -> [0, 1, 1, 2, 3, 5, 8, 13]
# fibonacci_generator(5)     -> yields 0, 1, 1, 2, 3  (via generator)
"""

import time
from functools import lru_cache


def fibonacci_iterative(n: int) -> int:
    """
    Calculate the nth Fibonacci number iteratively.

    Args:
        n: The index in the Fibonacci sequence (0-indexed).

    Returns:
        The nth Fibonacci number.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_recursive(n: int) -> int:
    """
    Calculate the nth Fibonacci number recursively (naive, exponential time).

    WARNING: Very slow for large n (> 35).

    Args:
        n: The index in the Fibonacci sequence (0-indexed).

    Returns:
        The nth Fibonacci number.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_memoized(n: int, memo: dict = None) -> int:
    """
    Calculate the nth Fibonacci number with manual memoization.

    Args:
        n: The index in the Fibonacci sequence (0-indexed).
        memo: Dictionary cache for previously computed values.

    Returns:
        The nth Fibonacci number.
    """
    if memo is None:
        memo = {}

    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n
    if n in memo:
        return memo[n]

    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fibonacci_lru(n: int) -> int:
    """
    Calculate the nth Fibonacci number using functools.lru_cache.

    Args:
        n: The index in the Fibonacci sequence (0-indexed).

    Returns:
        The nth Fibonacci number.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_sequence(count: int) -> list:
    """
    Generate the first 'count' Fibonacci numbers as a list.

    Args:
        count: How many Fibonacci numbers to generate.

    Returns:
        A list of the first 'count' Fibonacci numbers.
    """
    return [fibonacci_iterative(i) for i in range(count)]


def fibonacci_generator(count: int):
    """
    Generator that yields the first 'count' Fibonacci numbers.

    Args:
        count: How many Fibonacci numbers to yield.

    Yields:
        Fibonacci numbers one at a time.
    """
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b


def benchmark(func, n: int, label: str) -> tuple:
    """Time a Fibonacci function call and return (result, elapsed_ms)."""
    start = time.perf_counter()
    result = func(n)
    elapsed = (time.perf_counter() - start) * 1000
    return result, elapsed


if __name__ == "__main__":
    print("=" * 50)
    print("  Fibonacci Sequence Demo")
    print("=" * 50)

    # First 15 Fibonacci numbers
    print("\n--- First 15 Fibonacci Numbers ---")
    seq = fibonacci_sequence(15)
    for i, val in enumerate(seq):
        print(f"  F({i:>2}) = {val}")

    # Generator demo
    print("\n--- Generator (first 10) ---")
    gen_values = list(fibonacci_generator(10))
    print(f"  {gen_values}")

    # Verify all methods agree
    print("\n--- Method Comparison (n=20) ---")
    n = 20
    results = {
        "Iterative": fibonacci_iterative(n),
        "Recursive": fibonacci_recursive(n),
        "Memoized": fibonacci_memoized(n),
        "LRU Cache": fibonacci_lru(n),
    }
    for method, result in results.items():
        print(f"  {method:>12}: F({n}) = {result}")

    # Performance benchmark
    print("\n--- Performance Benchmark ---")
    # Iterative vs Memoized for large n
    for n_val in [30, 100, 500]:
        result_iter, time_iter = benchmark(fibonacci_iterative, n_val, "Iterative")
        result_memo, time_memo = benchmark(fibonacci_memoized, n_val, "Memoized")
        print(f"  n={n_val:>4}: Iterative={time_iter:.3f}ms, Memoized={time_memo:.3f}ms, Result={result_iter}")

    # Naive recursive is slow -- only test small n
    print("\n--- Naive Recursive Benchmark (slow!) ---")
    for n_val in [20, 25, 30]:
        result, elapsed = benchmark(fibonacci_recursive, n_val, "Recursive")
        print(f"  F({n_val}) = {result:>10}, Time: {elapsed:.1f}ms")

    print("\nFibonacci exercise complete!")
