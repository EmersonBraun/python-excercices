"""
Exercise 03 - Prime Numbers
=============================
Level: 2 - Functions & Collections
Difficulty: 2/5
Estimated Time: 20 minutes

Problem:
--------
Implement prime number utilities:
  1. Check if a number is prime
  2. Generate primes up to N using the Sieve of Eratosthenes
  3. Find prime factors of a number
  4. Generate the first N primes

Expected Input/Output:
----------------------
# is_prime(7)          -> True
# is_prime(10)         -> False
# is_prime(1)          -> False
# is_prime(2)          -> True
# sieve_of_eratosthenes(30) -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
# prime_factors(60)    -> [2, 2, 3, 5]
# first_n_primes(5)    -> [2, 3, 5, 7, 11]
"""

import math


def is_prime(n: int) -> bool:
    """
    Check if a number is prime using trial division.

    A prime number is greater than 1 and has no divisors other than 1 and itself.
    Optimization: only check up to sqrt(n), skip even numbers after 2.

    Args:
        n: An integer to check.

    Returns:
        True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check divisors of the form 6k +/- 1 up to sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def sieve_of_eratosthenes(limit: int) -> list:
    """
    Generate all prime numbers up to 'limit' using the Sieve of Eratosthenes.

    Algorithm:
      1. Create a boolean list of size limit+1, all True initially.
      2. Starting from 2, mark all multiples of each prime as not prime.
      3. Collect all indices still marked True.

    Args:
        limit: Upper bound (inclusive) for prime search.

    Returns:
        A sorted list of all primes <= limit.
    """
    if limit < 2:
        return []

    is_prime_arr = [True] * (limit + 1)
    is_prime_arr[0] = False
    is_prime_arr[1] = False

    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime_arr[i]:
            # Mark all multiples of i starting from i*i
            for multiple in range(i * i, limit + 1, i):
                is_prime_arr[multiple] = False

    return [i for i, prime in enumerate(is_prime_arr) if prime]


def prime_factors(n: int) -> list:
    """
    Find the prime factorization of a number.

    Args:
        n: A positive integer greater than 1.

    Returns:
        A sorted list of prime factors (with repetition).

    Raises:
        ValueError: If n < 2.
    """
    if n < 2:
        raise ValueError("n must be >= 2 for prime factorization")

    factors = []

    # Extract all factors of 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd factors from 3 to sqrt(n)
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # If n is still > 1, then it's a prime factor
    if n > 1:
        factors.append(n)

    return factors


def first_n_primes(n: int) -> list:
    """
    Generate the first n prime numbers.

    Args:
        n: How many primes to generate.

    Returns:
        A list of the first n primes.
    """
    if n <= 0:
        return []

    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes


def prime_range(start: int, end: int) -> list:
    """
    Find all prime numbers in a range [start, end].

    Args:
        start: Start of range (inclusive).
        end: End of range (inclusive).

    Returns:
        List of primes in the range.
    """
    return [n for n in range(max(2, start), end + 1) if is_prime(n)]


def is_twin_prime(n: int) -> bool:
    """
    Check if n is part of a twin prime pair.
    Twin primes differ by 2 (e.g., 11 and 13).

    Args:
        n: An integer.

    Returns:
        True if n and n+2 (or n-2) are both prime.
    """
    if not is_prime(n):
        return False
    return is_prime(n - 2) or is_prime(n + 2)


def goldbach_conjecture(n: int) -> tuple:
    """
    Find two primes that sum to n (Goldbach's conjecture: every even n > 2).

    Args:
        n: An even integer greater than 2.

    Returns:
        A tuple (p, q) where p + q = n and both are prime.

    Raises:
        ValueError: If n is odd or <= 2.
    """
    if n <= 2 or n % 2 != 0:
        raise ValueError("n must be an even integer greater than 2")

    for i in range(2, n // 2 + 1):
        if is_prime(i) and is_prime(n - i):
            return (i, n - i)

    return None  # Should never reach here if Goldbach's conjecture holds


if __name__ == "__main__":
    print("=" * 50)
    print("  Prime Numbers Demo")
    print("=" * 50)

    # is_prime tests
    print("\n--- Primality Tests ---")
    test_numbers = [1, 2, 3, 4, 7, 10, 13, 17, 25, 29, 97, 100]
    for n in test_numbers:
        print(f"  is_prime({n:>3}) = {is_prime(n)}")

    # Sieve of Eratosthenes
    print("\n--- Sieve of Eratosthenes (primes up to 100) ---")
    primes_100 = sieve_of_eratosthenes(100)
    print(f"  Count: {len(primes_100)}")
    print(f"  Primes: {primes_100}")

    # First N primes
    print("\n--- First 20 Primes ---")
    first_20 = first_n_primes(20)
    print(f"  {first_20}")

    # Prime factorization
    print("\n--- Prime Factorization ---")
    test_factors = [12, 60, 100, 97, 360, 1024, 9999]
    for n in test_factors:
        factors = prime_factors(n)
        product = " x ".join(str(f) for f in factors)
        print(f"  {n:>5} = {product}")

    # Twin primes
    print("\n--- Twin Primes (up to 100) ---")
    twins = [(n, n + 2) for n in range(2, 99) if is_prime(n) and is_prime(n + 2)]
    print(f"  {twins}")

    # Goldbach's conjecture
    print("\n--- Goldbach's Conjecture ---")
    for n in [4, 10, 20, 30, 50, 100]:
        p, q = goldbach_conjecture(n)
        print(f"  {n} = {p} + {q}")

    # Performance: Sieve vs trial division
    print("\n--- Sieve Performance ---")
    import time

    for limit in [1000, 10000, 100000]:
        start = time.perf_counter()
        primes = sieve_of_eratosthenes(limit)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  Primes up to {limit:>7}: {len(primes):>5} primes found in {elapsed:.2f}ms")

    print("\nPrime numbers exercise complete!")
