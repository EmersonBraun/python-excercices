"""
Exercise 07 - Count Vowels and Consonants
===========================================
Level: 1 - Foundations
Difficulty: 1/5
Estimated Time: 10 minutes

Problem:
--------
Write functions to count vowels and consonants in a given text.
Consider only English alphabetic characters (a-z).

Expected Input/Output:
----------------------
# count_vowels("Hello World")      -> 3
# count_consonants("Hello World")  -> 7
# count_both("Hello World")        -> {'vowels': 3, 'consonants': 7}
# vowel_percentage("Hello World")  -> 30.0  (3 vowels out of 10 letters)
# get_vowel_positions("Hello")     -> {1: 'e', 3: 'l'... no, -> {1: 'e', 4: 'o'}
"""

VOWELS = set("aeiouAEIOU")


def count_vowels(text: str) -> int:
    """
    Count the number of vowels (a, e, i, o, u) in the text.

    Args:
        text: The input string.

    Returns:
        The count of vowels.
    """
    return sum(1 for char in text if char in VOWELS)


def count_consonants(text: str) -> int:
    """
    Count the number of consonants in the text.

    Args:
        text: The input string.

    Returns:
        The count of consonants (alphabetic characters that are not vowels).
    """
    return sum(1 for char in text if char.isalpha() and char not in VOWELS)


def count_both(text: str) -> dict:
    """
    Count both vowels and consonants in the text.

    Args:
        text: The input string.

    Returns:
        A dict with 'vowels' and 'consonants' counts.
    """
    vowels = 0
    consonants = 0
    for char in text:
        if char.isalpha():
            if char in VOWELS:
                vowels += 1
            else:
                consonants += 1
    return {"vowels": vowels, "consonants": consonants}


def vowel_percentage(text: str) -> float:
    """
    Calculate the percentage of letters that are vowels.

    Args:
        text: The input string.

    Returns:
        The percentage of vowels among all alphabetic characters, rounded to 1 decimal.
    """
    total_letters = sum(1 for char in text if char.isalpha())
    if total_letters == 0:
        return 0.0
    vowel_count = count_vowels(text)
    return round((vowel_count / total_letters) * 100, 1)


def get_vowel_positions(text: str) -> dict:
    """
    Find the positions (0-indexed) and values of all vowels in the text.

    Args:
        text: The input string.

    Returns:
        A dict mapping position (int) to the vowel character.
    """
    return {i: char for i, char in enumerate(text) if char in VOWELS}


def vowel_frequency(text: str) -> dict:
    """
    Count the frequency of each vowel in the text (case-insensitive).

    Args:
        text: The input string.

    Returns:
        A dict mapping each vowel to its count.
    """
    freq = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for char in text.lower():
        if char in freq:
            freq[char] += 1
    return freq


if __name__ == "__main__":
    print("=" * 50)
    print("  Count Vowels & Consonants Demo")
    print("=" * 50)

    test_strings = [
        "Hello World",
        "Python Programming",
        "AEIOU",
        "bcdfg",
        "The quick brown fox jumps over the lazy dog",
        "",
        "12345!@#",
    ]

    # Count vowels and consonants
    print("\n--- Vowel & Consonant Counts ---")
    for s in test_strings:
        counts = count_both(s)
        pct = vowel_percentage(s)
        print(f"  '{s}'")
        print(f"    Vowels: {counts['vowels']}, Consonants: {counts['consonants']}, Vowel%: {pct}%")

    # Vowel positions
    print("\n--- Vowel Positions ---")
    for s in ["Hello", "Programming", "AEIOU"]:
        positions = get_vowel_positions(s)
        print(f"  '{s}' -> {positions}")

    # Vowel frequency
    print("\n--- Vowel Frequency ---")
    sample = "The quick brown fox jumps over the lazy dog"
    freq = vowel_frequency(sample)
    print(f"  Text: '{sample}'")
    for vowel, count in freq.items():
        bar = "#" * count
        print(f"    {vowel}: {count:>2} {bar}")

    print("\nVowels & consonants exercise complete!")
