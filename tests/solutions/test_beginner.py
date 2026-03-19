def test_fizzbuzz():
    """FizzBuzz should return correct results"""
    def fizzbuzz(n):
        if n % 15 == 0: return "FizzBuzz"
        if n % 3 == 0: return "Fizz"
        if n % 5 == 0: return "Buzz"
        return n

    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(1) == 1


def test_fibonacci():
    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(10) == 55


def test_caesar_cipher():
    def caesar(text, shift):
        result = ""
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base + shift) % 26 + base)
            else:
                result += c
        return result

    assert caesar("abc", 3) == "def"
    assert caesar("xyz", 3) == "abc"
    assert caesar("Hello", 1) == "Ifmmp"
