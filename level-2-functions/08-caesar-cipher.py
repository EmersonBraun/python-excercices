"""
Exercise 08 - Caesar Cipher
=============================
Level: 2 - Functions & Collections
Difficulty: 2/5
Estimated Time: 15 minutes

Problem:
--------
Implement the Caesar cipher encryption and decryption.

The Caesar cipher shifts each letter in the plaintext by a fixed number
of positions in the alphabet. For example, with a shift of 3:
  A -> D, B -> E, C -> F, ..., X -> A, Y -> B, Z -> C

Implement:
  1. Encrypt a message with a given shift
  2. Decrypt a message with a given shift
  3. Brute-force crack (try all 26 shifts)
  4. Preserve case and non-alphabetic characters

Expected Input/Output:
----------------------
# encrypt("HELLO", 3)       -> "KHOOR"
# decrypt("KHOOR", 3)       -> "HELLO"
# encrypt("Hello, World!", 5)-> "Mjqqt, Btwqi!"
# decrypt("Mjqqt, Btwqi!", 5)-> "Hello, World!"
# brute_force("KHOOR")      -> list of 26 possible decryptions
"""


def encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypt a message using the Caesar cipher.

    Args:
        plaintext: The message to encrypt.
        shift: Number of positions to shift each letter (can be negative).

    Returns:
        The encrypted ciphertext. Non-alphabetic characters are preserved.
    """
    shift = shift % 26  # Normalize shift to 0-25
    result = []

    for char in plaintext:
        if char.isalpha():
            # Determine base: 'A' for uppercase, 'a' for lowercase
            base = ord("A") if char.isupper() else ord("a")
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)

    return "".join(result)


def decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypt a Caesar cipher message.

    Decryption is just encryption with the negative shift.

    Args:
        ciphertext: The encrypted message.
        shift: The shift that was used during encryption.

    Returns:
        The decrypted plaintext.
    """
    return encrypt(ciphertext, -shift)


def brute_force(ciphertext: str) -> list:
    """
    Try all 26 possible shifts to crack a Caesar cipher.

    Args:
        ciphertext: The encrypted message.

    Returns:
        A list of (shift, decrypted_text) tuples for all 26 shifts.
    """
    return [(shift, decrypt(ciphertext, shift)) for shift in range(26)]


def frequency_analysis(text: str) -> dict:
    """
    Perform letter frequency analysis on a text.

    Args:
        text: The input text.

    Returns:
        A dict mapping each letter to its frequency percentage.
    """
    text_lower = text.lower()
    total_letters = sum(1 for c in text_lower if c.isalpha())
    if total_letters == 0:
        return {}

    freq = {}
    for char in text_lower:
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1

    return {
        char: round((count / total_letters) * 100, 2)
        for char, count in sorted(freq.items())
    }


def crack_with_frequency(ciphertext: str) -> tuple:
    """
    Attempt to crack the cipher using frequency analysis.

    In English, 'e' is the most common letter (~12.7%).
    Find the most frequent letter in the ciphertext and assume it maps to 'e'.

    Args:
        ciphertext: The encrypted message.

    Returns:
        A tuple (estimated_shift, decrypted_text).
    """
    freq = frequency_analysis(ciphertext)
    if not freq:
        return (0, ciphertext)

    # Find the most frequent letter in the ciphertext
    most_common = max(freq, key=freq.get)

    # Assume it corresponds to 'e'
    estimated_shift = (ord(most_common) - ord("e")) % 26

    return (estimated_shift, decrypt(ciphertext, estimated_shift))


def rot13(text: str) -> str:
    """
    Apply ROT13 encoding (Caesar cipher with shift 13).

    ROT13 is its own inverse: applying it twice returns the original text.

    Args:
        text: The input text.

    Returns:
        The ROT13-encoded text.
    """
    return encrypt(text, 13)


if __name__ == "__main__":
    print("=" * 50)
    print("  Caesar Cipher Demo")
    print("=" * 50)

    # Basic encryption / decryption
    print("\n--- Encrypt & Decrypt ---")
    test_cases = [
        ("HELLO", 3),
        ("Hello, World!", 5),
        ("The quick brown fox jumps over the lazy dog", 13),
        ("abc XYZ", 1),
        ("ATTACK AT DAWN", 7),
    ]

    for plaintext, shift in test_cases:
        encrypted = encrypt(plaintext, shift)
        decrypted = decrypt(encrypted, shift)
        print(f"  Shift {shift:>2}: '{plaintext}'")
        print(f"           -> '{encrypted}' (encrypted)")
        print(f"           -> '{decrypted}' (decrypted)")
        assert decrypted == plaintext, "Decryption failed!"
        print()

    # Brute force
    print("--- Brute Force Attack ---")
    secret = encrypt("MEET ME AT NOON", 8)
    print(f"  Ciphertext: '{secret}'")
    print(f"  Trying all shifts:")
    for shift, attempt in brute_force(secret):
        marker = " <-- MATCH" if "MEET" in attempt else ""
        print(f"    Shift {shift:>2}: {attempt}{marker}")

    # ROT13
    print("\n--- ROT13 ---")
    original = "Hello, World!"
    encoded = rot13(original)
    decoded = rot13(encoded)
    print(f"  Original: '{original}'")
    print(f"  ROT13:    '{encoded}'")
    print(f"  ROT13x2:  '{decoded}' (back to original)")

    # Frequency analysis
    print("\n--- Frequency Analysis ---")
    long_text = encrypt(
        "The quick brown fox jumps over the lazy dog. "
        "This is a sample text to demonstrate frequency analysis. "
        "English text has predictable letter frequency patterns.",
        17,
    )
    print(f"  Ciphertext: '{long_text[:50]}...'")

    estimated_shift, cracked = crack_with_frequency(long_text)
    print(f"  Estimated shift: {estimated_shift}")
    print(f"  Cracked text: '{cracked[:50]}...'")

    # Letter frequency of ciphertext
    print("\n--- Letter Frequency (ciphertext) ---")
    freq = frequency_analysis(long_text)
    for letter, pct in list(freq.items())[:10]:
        bar = "#" * int(pct)
        print(f"    {letter}: {pct:>5.1f}% {bar}")

    print("\nCaesar cipher exercise complete!")
