"""
Exercise 06 - String Reversal & Palindrome Checker
====================================================
Level: 1 - Foundations
Difficulty: 1/5
Estimated Time: 10 minutes

Problem:
--------
Implement functions to:
  1. Reverse a string (multiple approaches)
  2. Check if a string is a palindrome
  3. Handle edge cases (spaces, punctuation, case sensitivity)

Expected Input/Output:
----------------------
# reverse_string("hello")             -> "olleh"
# reverse_string_loop("hello")        -> "olleh"
# is_palindrome("racecar")            -> True
# is_palindrome("hello")              -> False
# is_palindrome("A man a plan a canal Panama") -> True  (ignoring spaces/case)
# is_palindrome("Was it a car or a cat I saw?") -> True  (ignoring punctuation)
"""


def reverse_string(s: str) -> str:
    """Reverse a string using slicing."""
    return s[::-1]


def reverse_string_loop(s: str) -> str:
    """Reverse a string using a loop."""
    reversed_s = ""
    for char in s:
        reversed_s = char + reversed_s
    return reversed_s


def reverse_string_recursive(s: str) -> str:
    """Reverse a string using recursion."""
    if len(s) <= 1:
        return s
    return reverse_string_recursive(s[1:]) + s[0]


def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome (case-sensitive, exact match).

    Args:
        s: The string to check.

    Returns:
        True if the string reads the same forwards and backwards.
    """
    return s == s[::-1]


def is_palindrome_ignore_case(s: str) -> bool:
    """
    Check if a string is a palindrome, ignoring case and non-alphanumeric characters.

    Args:
        s: The string to check.

    Returns:
        True if the cleaned string is a palindrome.
    """
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def longest_palindrome_substring(s: str) -> str:
    """
    Find the longest palindromic substring in a string.

    Args:
        s: The input string.

    Returns:
        The longest palindromic substring.
    """
    if len(s) < 2:
        return s

    longest = s[0]

    for i in range(len(s)):
        # Odd-length palindromes (centered on s[i])
        left, right = i, i
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > len(longest):
                longest = s[left:right + 1]
            left -= 1
            right += 1

        # Even-length palindromes (centered between s[i] and s[i+1])
        left, right = i, i + 1
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > len(longest):
                longest = s[left:right + 1]
            left -= 1
            right += 1

    return longest


if __name__ == "__main__":
    print("=" * 50)
    print("  String Reversal & Palindrome Demo")
    print("=" * 50)

    # String reversal
    print("\n--- String Reversal ---")
    test_strings = ["hello", "Python", "12345", "a", ""]
    for s in test_strings:
        rev_slice = reverse_string(s)
        rev_loop = reverse_string_loop(s)
        rev_recur = reverse_string_recursive(s)
        print(f"  '{s}' -> slice: '{rev_slice}', loop: '{rev_loop}', recursive: '{rev_recur}'")

    # Simple palindrome check
    print("\n--- Palindrome Check (exact) ---")
    palindrome_tests = ["racecar", "madam", "hello", "level", "noon", "abc"]
    for s in palindrome_tests:
        result = is_palindrome(s)
        print(f"  '{s}' -> {result}")

    # Palindrome ignoring case/spaces/punctuation
    print("\n--- Palindrome Check (ignore case & non-alphanum) ---")
    phrase_tests = [
        "A man a plan a canal Panama",
        "Was it a car or a cat I saw?",
        "No lemon, no melon",
        "Hello, World!",
        "Madam, I'm Adam",
        "race a car",
    ]
    for s in phrase_tests:
        result = is_palindrome_ignore_case(s)
        print(f"  '{s}' -> {result}")

    # Longest palindromic substring
    print("\n--- Longest Palindromic Substring ---")
    substring_tests = ["babad", "cbbd", "racecarxyz", "abcba", "a", "abacdfgdcaba"]
    for s in substring_tests:
        result = longest_palindrome_substring(s)
        print(f"  '{s}' -> '{result}'")

    print("\nString reversal & palindrome exercise complete!")
