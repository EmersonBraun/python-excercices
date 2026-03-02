"""
Level 5 - Exercise 02: Generators
===================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Learn to create generator functions and understand lazy evaluation.
Generators produce items one at a time and only when requested, making
them memory-efficient for large (or infinite) sequences.

Exercises
---------
1. fibonacci_gen    - Infinite Fibonacci sequence generator.
2. my_range         - Clone of the built-in range() function.
3. file_line_gen    - Lazily yields lines from a file (simulated here).
4. prime_gen        - Yields prime numbers indefinitely.

Expected output (approximate):
------------------------------
# fibonacci_gen
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# my_range
# list(my_range(1, 10, 2))  ->  [1, 3, 5, 7, 9]

# file_line_gen
# Line 1: Hello
# Line 2: World

# prime_gen
# First 15 primes: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
"""

import itertools
import tempfile
import os


# ---------------------------------------------------------------------------
# 1. Infinite Fibonacci Generator
# ---------------------------------------------------------------------------
def fibonacci_gen():
    """Yield Fibonacci numbers forever: 0, 1, 1, 2, 3, 5, 8, ...

    >>> gen = fibonacci_gen()
    >>> [next(gen) for _ in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# ---------------------------------------------------------------------------
# 2. Range Clone
# ---------------------------------------------------------------------------
def my_range(start, stop=None, step=1):
    """Re-implementation of the built-in range() as a generator.

    Supports one, two, or three arguments just like range():
        my_range(5)        -> 0, 1, 2, 3, 4
        my_range(2, 8)     -> 2, 3, 4, 5, 6, 7
        my_range(0, 10, 3) -> 0, 3, 6, 9

    >>> list(my_range(5))
    [0, 1, 2, 3, 4]
    >>> list(my_range(1, 10, 2))
    [1, 3, 5, 7, 9]
    >>> list(my_range(10, 0, -2))
    [10, 8, 6, 4, 2]
    """
    if stop is None:
        start, stop = 0, start

    if step == 0:
        raise ValueError("my_range() step argument must not be zero")

    current = start
    if step > 0:
        while current < stop:
            yield current
            current += step
    else:
        while current > stop:
            yield current
            current += step


# ---------------------------------------------------------------------------
# 3. File Line Generator
# ---------------------------------------------------------------------------
def file_line_gen(filepath):
    """Yield stripped lines from a text file one at a time.

    This is memory-efficient for very large files because only one
    line is held in memory at a time.

    >>> for line in file_line_gen("example.txt"):
    ...     print(line)
    """
    with open(filepath, "r", encoding="utf-8") as fh:
        for line in fh:
            yield line.rstrip("\n")


# ---------------------------------------------------------------------------
# 4. Infinite Prime Generator
# ---------------------------------------------------------------------------
def prime_gen():
    """Yield prime numbers in ascending order, starting from 2.

    Uses a simple trial-division approach suitable for educational
    purposes and moderate-size primes.

    >>> gen = prime_gen()
    >>> [next(gen) for _ in range(10)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    def is_prime(n):
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    yield 2
    candidate = 3
    while True:
        if is_prime(candidate):
            yield candidate
        candidate += 2


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    # --- 1. Fibonacci ---
    print("=" * 50)
    print("1. Infinite Fibonacci Generator")
    print("=" * 50)
    fib = fibonacci_gen()
    first_10 = [next(fib) for _ in range(10)]
    print(f"First 10 Fibonacci numbers: {first_10}\n")

    # --- 2. Range clone ---
    print("=" * 50)
    print("2. my_range (range clone)")
    print("=" * 50)
    print(f"my_range(5):          {list(my_range(5))}")
    print(f"my_range(2, 8):       {list(my_range(2, 8))}")
    print(f"my_range(1, 10, 2):   {list(my_range(1, 10, 2))}")
    print(f"my_range(10, 0, -2):  {list(my_range(10, 0, -2))}")
    print()

    # --- 3. File line generator ---
    print("=" * 50)
    print("3. File Line Generator")
    print("=" * 50)
    # Create a temporary file for demonstration
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    tmp.write("Hello\nWorld\nPython\nGenerators\nAre\nAwesome\n")
    tmp.close()
    for i, line in enumerate(file_line_gen(tmp.name), 1):
        print(f"  Line {i}: {line}")
    os.unlink(tmp.name)
    print()

    # --- 4. Prime generator ---
    print("=" * 50)
    print("4. Infinite Prime Generator")
    print("=" * 50)
    primes = prime_gen()
    first_15 = [next(primes) for _ in range(15)]
    print(f"First 15 primes: {first_15}")

    # Bonus: combine generators with itertools
    print("\nBonuses using itertools:")
    fib = fibonacci_gen()
    fibs_under_100 = list(itertools.takewhile(lambda x: x < 100, fib))
    print(f"Fibonacci < 100: {fibs_under_100}")

    primes2 = prime_gen()
    primes_50_to_100 = list(
        itertools.takewhile(
            lambda x: x <= 100,
            itertools.dropwhile(lambda x: x < 50, primes2),
        )
    )
    print(f"Primes 50..100:  {primes_50_to_100}")
