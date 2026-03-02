"""
Text Statistics Analyzer
=========================
Difficulty: 2/5
Estimated time: 20 minutes

Problem:
--------
Analyze a block of text and produce statistics:
1. Total word count.
2. Total character count (with and without spaces).
3. Sentence count.
4. Paragraph count.
5. Average word length.
6. Most common words (top N, excluding stop words).
7. Estimated reading time (based on ~200 words per minute).
8. Longest and shortest words.

Concepts practiced:
- String methods (split, lower, strip)
- collections.Counter
- Regular expressions
- Formatted output

Expected output (example):
--------------------------
# === Text Statistics ===
# Words:                84
# Characters (spaces):  487
# Characters (no sp.):  409
# Sentences:            6
# Paragraphs:           2
# Avg word length:      4.87 chars
# Reading time:         ~1 min
#
# Top 5 most common words:
#   1. python    (4)
#   2. language  (3)
#   3. used      (2)
#   ...
#
# Longest word:  programming (11 chars)
# Shortest word: a (1 char)
"""

import re
from collections import Counter


# Common English stop words to exclude from frequency analysis
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "its", "as", "was", "were",
    "are", "be", "been", "being", "have", "has", "had", "do", "does",
    "did", "will", "would", "could", "should", "may", "might", "shall",
    "can", "this", "that", "these", "those", "i", "you", "he", "she",
    "we", "they", "me", "him", "her", "us", "them", "my", "your", "his",
    "our", "their", "not", "no", "so", "if", "than", "also", "very",
    "just", "about", "into", "more", "some", "such", "what", "which",
}


def count_words(text):
    """Return the total number of words in the text."""
    words = text.split()
    return len(words)


def count_characters(text, include_spaces=True):
    """Return character count, optionally excluding spaces."""
    if include_spaces:
        return len(text)
    return len(text.replace(" ", "").replace("\n", "").replace("\t", ""))


def count_sentences(text):
    """Count sentences by splitting on sentence-ending punctuation."""
    sentences = re.split(r"[.!?]+", text)
    # Filter out empty strings from trailing punctuation
    return len([s for s in sentences if s.strip()])


def count_paragraphs(text):
    """Count paragraphs (blocks of text separated by blank lines)."""
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return len([p for p in paragraphs if p.strip()])


def average_word_length(text):
    """Return the average word length (alphabetic characters only)."""
    words = re.findall(r"[a-zA-Z]+", text)
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)


def most_common_words(text, n=5):
    """
    Return the N most common words, excluding stop words.

    Parameters:
        text (str): Input text.
        n (int): Number of top words to return.

    Returns:
        list[tuple]: List of (word, count) tuples.
    """
    words = re.findall(r"[a-zA-Z]+", text.lower())
    filtered = [w for w in words if w not in STOP_WORDS]
    return Counter(filtered).most_common(n)


def reading_time(text, wpm=200):
    """
    Estimate reading time in minutes.

    Parameters:
        text (str): Input text.
        wpm (int): Words per minute reading speed.

    Returns:
        float: Estimated minutes to read.
    """
    words = count_words(text)
    return max(1, round(words / wpm))


def longest_shortest_words(text):
    """
    Find the longest and shortest words in the text.

    Returns:
        tuple: (longest_word, shortest_word)
    """
    words = re.findall(r"[a-zA-Z]+", text)
    if not words:
        return ("", "")
    longest = max(words, key=len)
    shortest = min(words, key=len)
    return longest, shortest


def analyze_text(text, top_n=5):
    """
    Run all analyses on the given text and print a formatted report.

    Parameters:
        text (str): Text to analyze.
        top_n (int): Number of top common words to show.
    """
    words = count_words(text)
    chars_with = count_characters(text, include_spaces=True)
    chars_without = count_characters(text, include_spaces=False)
    sentences = count_sentences(text)
    paragraphs = count_paragraphs(text)
    avg_len = average_word_length(text)
    read_time = reading_time(text)
    top_words = most_common_words(text, n=top_n)
    longest, shortest = longest_shortest_words(text)

    print("=" * 40)
    print("        TEXT STATISTICS")
    print("=" * 40)
    print(f"  Words:                {words}")
    print(f"  Characters (spaces):  {chars_with}")
    print(f"  Characters (no sp.):  {chars_without}")
    print(f"  Sentences:            {sentences}")
    print(f"  Paragraphs:           {paragraphs}")
    print(f"  Avg word length:      {avg_len:.2f} chars")
    print(f"  Reading time:         ~{read_time} min")
    print()

    print(f"  Top {top_n} most common words:")
    for i, (word, cnt) in enumerate(top_words, start=1):
        print(f"    {i}. {word:15s} ({cnt})")
    print()

    print(f"  Longest word:  {longest} ({len(longest)} chars)")
    print(f"  Shortest word: {shortest} ({len(shortest)} char{'s' if len(shortest) != 1 else ''})")
    print("=" * 40)


if __name__ == "__main__":
    sample_text = """Python is a high-level, general-purpose programming language. Its design
philosophy emphasizes code readability with the use of significant indentation.
Python is dynamically typed and garbage-collected. It supports multiple
programming paradigms, including structured, object-oriented and functional
programming.

Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde
and Informatica as a successor to the ABC programming language. Python
consistently ranks as one of the most popular programming languages. It is used
extensively in web development, data science, artificial intelligence, scientific
computing, and automation. The language provides a large standard library and an
active community that contributes thousands of third-party packages."""

    print("--- Text Statistics Analyzer Demo ---\n")
    print("Sample text (first 80 chars):", repr(sample_text[:80]), "...\n")
    analyze_text(sample_text, top_n=8)
