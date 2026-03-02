"""
Exercise 07 - Anagram Checker
===============================
Level: 2 - Functions & Collections
Difficulty: 2/5
Estimated Time: 10 minutes

Problem:
--------
Determine if two strings are anagrams of each other.
Two strings are anagrams if they contain the same characters
with the same frequencies, regardless of order.

Implement multiple approaches:
  1. Sorting approach
  2. Character counting approach (dict)
  3. Counter approach (collections.Counter)

Expected Input/Output:
----------------------
# is_anagram("listen", "silent")      -> True
# is_anagram("hello", "world")        -> False
# is_anagram("Astronomer", "Moon starer") -> True (ignoring spaces/case)
# is_anagram("rail safety", "fairy tales") -> True
# find_anagrams("listen", ["enlist", "google", "inlets", "banana"]) -> ["enlist", "inlets"]
"""

from collections import Counter


def is_anagram_sort(s1: str, s2: str) -> bool:
    """
    Check if two strings are anagrams using sorting.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        True if s1 and s2 are anagrams (case-sensitive, exact).
    """
    return sorted(s1) == sorted(s2)


def is_anagram_count(s1: str, s2: str) -> bool:
    """
    Check if two strings are anagrams using character counting (dict).

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        True if s1 and s2 are anagrams.
    """
    if len(s1) != len(s2):
        return False

    char_count = {}
    for char in s1:
        char_count[char] = char_count.get(char, 0) + 1

    for char in s2:
        if char not in char_count:
            return False
        char_count[char] -= 1
        if char_count[char] < 0:
            return False

    return all(v == 0 for v in char_count.values())


def is_anagram_counter(s1: str, s2: str) -> bool:
    """
    Check if two strings are anagrams using collections.Counter.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        True if s1 and s2 are anagrams.
    """
    return Counter(s1) == Counter(s2)


def is_anagram(s1: str, s2: str, ignore_spaces: bool = True, ignore_case: bool = True) -> bool:
    """
    Check if two strings are anagrams with optional case/space handling.

    Args:
        s1: First string.
        s2: Second string.
        ignore_spaces: If True, ignore whitespace.
        ignore_case: If True, ignore letter casing.

    Returns:
        True if the cleaned strings are anagrams.
    """
    def clean(s: str) -> str:
        if ignore_spaces:
            s = s.replace(" ", "")
        if ignore_case:
            s = s.lower()
        return s

    return is_anagram_counter(clean(s1), clean(s2))


def find_anagrams(word: str, candidates: list) -> list:
    """
    Find all anagrams of a word from a list of candidates.

    Args:
        word: The target word.
        candidates: A list of words to check.

    Returns:
        A list of words from candidates that are anagrams of word.
    """
    word_sorted = sorted(word.lower())
    return [
        candidate for candidate in candidates
        if sorted(candidate.lower()) == word_sorted
    ]


def group_anagrams(words: list) -> list:
    """
    Group a list of words into anagram groups.

    Args:
        words: A list of words.

    Returns:
        A list of lists, where each inner list contains words that are anagrams.
    """
    anagram_map = {}
    for word in words:
        key = tuple(sorted(word.lower()))
        if key not in anagram_map:
            anagram_map[key] = []
        anagram_map[key].append(word)

    return [group for group in anagram_map.values() if len(group) > 1]


def anagram_distance(s1: str, s2: str) -> int:
    """
    Calculate how many character changes are needed to make s2 an anagram of s1.
    Both strings must have the same length.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Number of character replacements needed, or -1 if different lengths.
    """
    if len(s1) != len(s2):
        return -1

    count1 = Counter(s1.lower())
    count2 = Counter(s2.lower())

    # Count excess characters in s2 that are not in s1
    diff = count2 - count1
    return sum(diff.values())


if __name__ == "__main__":
    print("=" * 50)
    print("  Anagram Checker Demo")
    print("=" * 50)

    # Basic anagram tests
    print("\n--- Basic Anagram Tests ---")
    test_pairs = [
        ("listen", "silent", True),
        ("hello", "world", False),
        ("triangle", "integral", True),
        ("apple", "papel", True),
        ("rat", "car", False),
        ("night", "thing", True),
    ]

    for s1, s2, expected in test_pairs:
        result_sort = is_anagram_sort(s1, s2)
        result_count = is_anagram_count(s1, s2)
        result_counter = is_anagram_counter(s1, s2)
        status = "PASS" if result_sort == expected else "FAIL"
        print(f"  [{status}] '{s1}' & '{s2}': sort={result_sort}, count={result_count}, counter={result_counter}")

    # Case-insensitive / space-ignoring tests
    print("\n--- Advanced Anagram Tests (ignore case & spaces) ---")
    advanced_pairs = [
        ("Astronomer", "Moon starer", True),
        ("rail safety", "fairy tales", True),
        ("The eyes", "They see", True),
        ("Dormitory", "Dirty room", True),
        ("Hello", "World", False),
    ]

    for s1, s2, expected in advanced_pairs:
        result = is_anagram(s1, s2)
        status = "PASS" if result == expected else "FAIL"
        print(f"  [{status}] '{s1}' & '{s2}' -> {result}")

    # Find anagrams in a list
    print("\n--- Find Anagrams ---")
    word = "listen"
    candidates = ["enlist", "google", "inlets", "banana", "silent", "tinsel"]
    found = find_anagrams(word, candidates)
    print(f"  Anagrams of '{word}': {found}")

    # Group anagrams
    print("\n--- Group Anagrams ---")
    word_list = ["eat", "tea", "tan", "ate", "nat", "bat", "listen", "silent", "enlist"]
    groups = group_anagrams(word_list)
    for group in groups:
        print(f"  {group}")

    # Anagram distance
    print("\n--- Anagram Distance ---")
    distance_tests = [
        ("abc", "abc", 0),
        ("abc", "abd", 1),
        ("abc", "xyz", 3),
        ("hello", "jello", 1),
    ]
    for s1, s2, expected in distance_tests:
        dist = anagram_distance(s1, s2)
        status = "PASS" if dist == expected else "FAIL"
        print(f"  [{status}] '{s1}' & '{s2}': distance = {dist}")

    print("\nAnagram checker exercise complete!")
