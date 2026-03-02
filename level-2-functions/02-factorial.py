"""
Exercise 02 - Factorial
========================
Level: 2 - Functions & Collections
Difficulty: 2/5
Estimated Time: 10 minutes

Problem:
--------
Implement the factorial function using multiple approaches:
  1. Iterative
  2. Recursive
  3. Using math.factorial (built-in comparison)

Factorial definition: n! = n * (n-1) * (n-2) * ... * 2 * 1
  0! = 1 (by definition)
  1! = 1

Expected Input/Output:
----------------------
# factorial_iterative(5)   -> 120
# factorial_recursive(5)   -> 120
# factorial_iterative(0)   -> 1
# factorial_iterative(10)  -> 3628800
# factorial_iterative(-1)  -> raises ValueError
"""

import math
import time


def factorial_iterative(n: int) -> int:
    """
    Calculate n! iteratively.

    Args:
        n: A non-negative integer.

    Returns:
        n factorial.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    """
    Calculate n! recursively.

    Args:
        n: A non-negative integer.

    Returns:
        n factorial.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_reduce(n: int) -> int:
    """
    Calculate n! using functools.reduce.

    Args:
        n: A non-negative integer.

    Returns:
        n factorial.
    """
    from functools import reduce
    from operator import mul

    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return reduce(mul, range(2, n + 1), 1)


def trailing_zeros(n: int) -> int:
    """
    Count the number of trailing zeros in n!.

    Trailing zeros come from factors of 10 = 2 * 5.
    Since there are always more 2s than 5s, we count factors of 5.

    Args:
        n: A non-negative integer.

    Returns:
        The number of trailing zeros in n!.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    count = 0
    power_of_5 = 5
    while power_of_5 <= n:
        count += n // power_of_5
        power_of_5 *= 5
    return count


def digit_count(n: int) -> int:
    """
    Calculate the number of digits in n! without computing the full factorial.
    Uses Stirling's approximation via logarithms.

    Args:
        n: A non-negative integer.

    Returns:
        The number of digits in n!.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1

    import math as m
    # Number of digits = floor(log10(n!)) + 1
    # log10(n!) = sum of log10(i) for i in 2..n
    log_sum = sum(m.log10(i) for i in range(2, n + 1))
    return int(log_sum) + 1


def combinations(n: int, r: int) -> int:
    """
    Calculate C(n, r) = n! / (r! * (n-r)!) using factorial.

    Args:
        n: Total number of items.
        r: Number of items to choose.

    Returns:
        The number of combinations.
    """
    if r < 0 or r > n:
        return 0
    return factorial_iterative(n) // (factorial_iterative(r) * factorial_iterative(n - r))


def permutations(n: int, r: int) -> int:
    """
    Calculate P(n, r) = n! / (n-r)! using factorial.

    Args:
        n: Total number of items.
        r: Number of items to arrange.

    Returns:
        The number of permutations.
    """
    if r < 0 or r > n:
        return 0
    return factorial_iterative(n) // factorial_iterative(n - r)


if __name__ == "__main__":
    print("=" * 50)
    print("  Factorial Exercise Demo")
    print("=" * 50)

    # Basic factorial calculations
    print("\n--- Factorials (0-12) ---")
    print(f"  {'n':>3} | {'Iterative':>12} | {'Recursive':>12} | {'math.factorial':>14}")
    print(f"  {'-'*3}-+-{'-'*12}-+-{'-'*12}-+-{'-'*14}")
    for n in range(13):
        iter_val = factorial_iterative(n)
        recur_val = factorial_recursive(n)
        math_val = math.factorial(n)
        print(f"  {n:>3} | {iter_val:>12} | {recur_val:>12} | {math_val:>14}")

    # Large factorial
    print("\n--- Large Factorials ---")
    for n in [20, 50, 100]:
        result = factorial_iterative(n)
        digits = digit_count(n)
        zeros = trailing_zeros(n)
        print(f"  {n}! has {digits} digits and {zeros} trailing zeros")

    # Error handling
    print("\n--- Error Handling ---")
    try:
        factorial_iterative(-1)
    except ValueError as e:
        print(f"  factorial(-1) -> Error: {e}")

    # Combinations and Permutations
    print("\n--- Combinations C(n, r) ---")
    test_cases = [(5, 2), (10, 3), (52, 5), (6, 0), (6, 6)]
    for n, r in test_cases:
        print(f"  C({n}, {r}) = {combinations(n, r)}")

    print("\n--- Permutations P(n, r) ---")
    for n, r in [(5, 2), (10, 3), (6, 4)]:
        print(f"  P({n}, {r}) = {permutations(n, r)}")

    # Performance comparison
    print("\n--- Performance Comparison ---")
    for n in [100, 500, 900]:
        start = time.perf_counter()
        factorial_iterative(n)
        iter_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        factorial_reduce(n)
        reduce_time = (time.perf_counter() - start) * 1000

        print(f"  n={n:>4}: Iterative={iter_time:.3f}ms, Reduce={reduce_time:.3f}ms")

    print("\nFactorial exercise complete!")
