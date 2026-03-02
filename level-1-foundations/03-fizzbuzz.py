"""
Exercise 03 - FizzBuzz
=======================
Level: 1 - Foundations
Difficulty: 1/5
Estimated Time: 10 minutes

Problem:
--------
Implement the classic FizzBuzz problem:
  - For numbers 1 to 100:
    - Print "Fizz" if the number is divisible by 3
    - Print "Buzz" if the number is divisible by 5
    - Print "FizzBuzz" if the number is divisible by both 3 and 5
    - Otherwise, print the number itself

Expected Input/Output:
----------------------
# fizzbuzz(1)  -> "1"
# fizzbuzz(3)  -> "Fizz"
# fizzbuzz(5)  -> "Buzz"
# fizzbuzz(15) -> "FizzBuzz"
# fizzbuzz(7)  -> "7"
# fizzbuzz_range(1, 15) -> ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
"""


def fizzbuzz(n: int) -> str:
    """
    Return FizzBuzz result for a single number.

    Args:
        n: A positive integer.

    Returns:
        'FizzBuzz' if divisible by 3 and 5,
        'Fizz' if divisible by 3,
        'Buzz' if divisible by 5,
        the number as string otherwise.
    """
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def fizzbuzz_range(start: int, end: int) -> list:
    """
    Return a list of FizzBuzz results for a range of numbers.

    Args:
        start: Start of range (inclusive).
        end: End of range (inclusive).

    Returns:
        List of FizzBuzz results as strings.
    """
    return [fizzbuzz(n) for n in range(start, end + 1)]


def fizzbuzz_custom(n: int, rules: dict) -> str:
    """
    Generalized FizzBuzz with custom divisor-word rules.

    Args:
        n: A positive integer.
        rules: Dict mapping divisors to words, e.g. {3: 'Fizz', 5: 'Buzz', 7: 'Bazz'}.

    Returns:
        Concatenated words for all matching divisors, or the number as string.
    """
    result = ""
    for divisor in sorted(rules.keys()):
        if n % divisor == 0:
            result += rules[divisor]
    return result if result else str(n)


if __name__ == "__main__":
    print("=" * 40)
    print("  FizzBuzz Demo")
    print("=" * 40)

    # Classic FizzBuzz 1-100
    print("\n--- Classic FizzBuzz (1-100) ---")
    results = fizzbuzz_range(1, 100)
    for i, result in enumerate(results, 1):
        print(f"{result:>8}", end="")
        if i % 10 == 0:
            print()

    # Single number tests
    print("\n--- Single Number Tests ---")
    test_cases = [1, 3, 5, 15, 7, 30, 45, 98]
    for n in test_cases:
        print(f"  fizzbuzz({n:>3}) = {fizzbuzz(n)}")

    # Custom FizzBuzz with extra rule
    print("\n--- Custom FizzBuzz (Fizz=3, Buzz=5, Bazz=7) for 1-21 ---")
    custom_rules = {3: "Fizz", 5: "Buzz", 7: "Bazz"}
    for i in range(1, 22):
        result = fizzbuzz_custom(i, custom_rules)
        print(f"  {i:>2} -> {result}")

    print("\nFizzBuzz exercise complete!")
