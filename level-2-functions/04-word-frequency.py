"""
Exercise 04 - Word Frequency Counter
======================================
Level: 2 - Functions & Collections
Difficulty: 2/5
Estimated Time: 15 minutes

Problem:
--------
Count the frequency of each word in a given text.
Handle:
  1. Case insensitivity
  2. Punctuation removal
  3. Sorting by frequency
  4. Top N most common words

Expected Input/Output:
----------------------
# count_words("the cat sat on the mat") -> {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
# top_n_words("the cat sat on the mat", 2) -> [('the', 2), ('cat', 1)]
# word_frequency_sorted("hello world hello") -> [('hello', 2), ('world', 1)]
"""

import string
from collections import Counter


def clean_text(text: str) -> str:
    """
    Clean text by converting to lowercase and removing punctuation.

    Args:
        text: Raw input text.

    Returns:
        Cleaned text with only lowercase words and spaces.
    """
    # Remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    cleaned = text.translate(translator)
    # Normalize whitespace and lowercase
    return " ".join(cleaned.lower().split())


def count_words(text: str) -> dict:
    """
    Count the frequency of each word in the text.

    Args:
        text: Input text string.

    Returns:
        A dictionary mapping each word to its count.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return {}

    word_count = {}
    for word in cleaned.split():
        word_count[word] = word_count.get(word, 0) + 1
    return word_count


def count_words_counter(text: str) -> Counter:
    """
    Count word frequencies using collections.Counter.

    Args:
        text: Input text string.

    Returns:
        A Counter object with word frequencies.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return Counter()
    return Counter(cleaned.split())


def top_n_words(text: str, n: int = 10) -> list:
    """
    Return the top N most frequent words.

    Args:
        text: Input text string.
        n: Number of top words to return.

    Returns:
        A list of (word, count) tuples sorted by frequency descending.
    """
    counter = count_words_counter(text)
    return counter.most_common(n)


def word_frequency_sorted(text: str, reverse: bool = True) -> list:
    """
    Return all words sorted by frequency.

    Args:
        text: Input text string.
        reverse: If True, sort descending (most frequent first).

    Returns:
        A list of (word, count) tuples sorted by frequency.
    """
    word_count = count_words(text)
    return sorted(word_count.items(), key=lambda x: (-x[1], x[0]) if reverse else (x[1], x[0]))


def word_length_distribution(text: str) -> dict:
    """
    Compute the distribution of word lengths.

    Args:
        text: Input text string.

    Returns:
        A dict mapping word length to the count of words with that length.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return {}

    distribution = {}
    for word in cleaned.split():
        length = len(word)
        distribution[length] = distribution.get(length, 0) + 1
    return dict(sorted(distribution.items()))


def unique_words(text: str) -> set:
    """
    Return the set of unique words in the text.

    Args:
        text: Input text string.

    Returns:
        A set of unique lowercase words.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return set()
    return set(cleaned.split())


def text_statistics(text: str) -> dict:
    """
    Compute overall statistics about the text.

    Args:
        text: Input text string.

    Returns:
        A dict with total_words, unique_words, avg_word_length, longest_word, shortest_word.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return {
            "total_words": 0,
            "unique_words": 0,
            "avg_word_length": 0,
            "longest_word": "",
            "shortest_word": "",
        }

    words = cleaned.split()
    unique = set(words)
    avg_len = sum(len(w) for w in words) / len(words)
    longest = max(words, key=len)
    shortest = min(words, key=len)

    return {
        "total_words": len(words),
        "unique_words": len(unique),
        "avg_word_length": round(avg_len, 2),
        "longest_word": longest,
        "shortest_word": shortest,
    }


if __name__ == "__main__":
    print("=" * 50)
    print("  Word Frequency Counter Demo")
    print("=" * 50)

    sample_text = """
    Python is a great programming language. Python is easy to learn.
    Many developers love Python because Python is versatile.
    You can use Python for web development, data science, automation,
    and much more. Python's community is amazing and helpful!
    """

    # Word count
    print("\n--- Word Frequency ---")
    freq = count_words(sample_text)
    for word, count in sorted(freq.items(), key=lambda x: -x[1]):
        bar = "#" * count
        print(f"  {word:>15}: {count:>2} {bar}")

    # Top 5 words
    print("\n--- Top 5 Words ---")
    top5 = top_n_words(sample_text, 5)
    for i, (word, count) in enumerate(top5, 1):
        print(f"  {i}. '{word}' ({count} times)")

    # Simple sentence test
    print("\n--- Simple Test ---")
    simple = "the cat sat on the mat the cat"
    print(f"  Text: '{simple}'")
    print(f"  Counts: {count_words(simple)}")
    print(f"  Sorted: {word_frequency_sorted(simple)}")

    # Word length distribution
    print("\n--- Word Length Distribution ---")
    dist = word_length_distribution(sample_text)
    for length, count in dist.items():
        bar = "#" * count
        print(f"  {length:>2} letters: {count:>2} words {bar}")

    # Unique words
    print("\n--- Unique Words ---")
    uniq = unique_words(sample_text)
    print(f"  Count: {len(uniq)}")
    print(f"  Words: {sorted(uniq)}")

    # Text statistics
    print("\n--- Text Statistics ---")
    stats = text_statistics(sample_text)
    for key, value in stats.items():
        print(f"  {key:>20}: {value}")

    # Empty text handling
    print("\n--- Edge Cases ---")
    print(f"  Empty text: {count_words('')}")
    print(f"  Punctuation only: {count_words('...!!!')}")
    print(f"  Single word: {count_words('hello')}")

    print("\nWord frequency exercise complete!")
