"""
Level 6 - Exercise 05: Unit Tests with pytest Style
=====================================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Write unit tests using pytest conventions.  This file is designed to
work BOTH with `pytest` (if installed) AND as a standalone script via
`python3 05-pytest-examples.py` using simple assert-based checks.

Topics Covered
--------------
1. Basic assertions and test functions.
2. Testing exceptions (pytest.raises equivalent).
3. Parameterized tests (manual and pytest-style).
4. Fixtures (setup/teardown patterns).
5. Testing classes and dataclasses.

Usage:
    python3 05-pytest-examples.py          # standalone runner
    pytest  05-pytest-examples.py -v       # if pytest is installed

Expected output (standalone):
------------------------------
    test_add_positive ................. PASS
    test_add_negative ................. PASS
    ...
    22 tests passed, 0 failed
"""

import os
import tempfile
from dataclasses import dataclass


# ===================================================================
# Code Under Test
# ===================================================================
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def divide(a: float, b: float) -> float:
    """Divide a by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (0-indexed)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome (case-insensitive, ignoring spaces)."""
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


@dataclass
class BankAccount:
    """Simple bank account for testing."""
    owner: str
    balance: float = 0.0

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def transfer(self, other: "BankAccount", amount: float) -> None:
        self.withdraw(amount)
        other.deposit(amount)


class Stack:
    """Simple stack implementation for testing."""

    def __init__(self):
        self._items: list = []

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("Peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


# ===================================================================
# Tests -- Section 1: Basic Assertions
# ===================================================================
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_float():
    assert abs(add(0.1, 0.2) - 0.3) < 1e-9

def test_add_zero():
    assert add(0, 0) == 0


# ===================================================================
# Tests -- Section 2: Exception Testing
# ===================================================================
def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    try:
        divide(10, 0)
        assert False, "Expected ZeroDivisionError"
    except ZeroDivisionError as e:
        assert "Cannot divide by zero" in str(e)

def test_fibonacci_negative():
    try:
        fibonacci(-1)
        assert False, "Expected ValueError"
    except ValueError:
        pass

def test_bank_overdraw():
    account = BankAccount("Alice", 100.0)
    try:
        account.withdraw(200.0)
        assert False, "Expected ValueError for insufficient funds"
    except ValueError as e:
        assert "Insufficient" in str(e)


# ===================================================================
# Tests -- Section 3: Parameterized Tests
# ===================================================================
FIBONACCI_CASES = [
    (0, 0),
    (1, 1),
    (2, 1),
    (5, 5),
    (10, 55),
    (20, 6765),
]

def test_fibonacci_parameterized():
    for n, expected in FIBONACCI_CASES:
        result = fibonacci(n)
        assert result == expected, f"fibonacci({n}) = {result}, expected {expected}"

PALINDROME_CASES = [
    ("racecar", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("", True),
    ("ab", False),
    ("aba", True),
    ("Was it a car or a cat I saw", True),
]

def test_palindrome_parameterized():
    for s, expected in PALINDROME_CASES:
        result = is_palindrome(s)
        assert result == expected, f"is_palindrome({s!r}) = {result}, expected {expected}"


# ===================================================================
# Tests -- Section 4: Fixtures / Setup-Teardown
# ===================================================================
def make_temp_file(content: str = "test data") -> str:
    """Fixture-like helper: create a temp file with content."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path


def test_temp_file_creation():
    path = make_temp_file("hello world")
    try:
        assert os.path.exists(path)
        with open(path) as f:
            assert f.read() == "hello world"
    finally:
        os.unlink(path)

def test_temp_file_cleanup():
    path = make_temp_file()
    os.unlink(path)
    assert not os.path.exists(path)


# ===================================================================
# Tests -- Section 5: Class Testing (BankAccount)
# ===================================================================
def test_bank_deposit():
    acc = BankAccount("Bob", 0.0)
    acc.deposit(100.0)
    assert acc.balance == 100.0

def test_bank_withdraw():
    acc = BankAccount("Bob", 100.0)
    acc.withdraw(40.0)
    assert acc.balance == 60.0

def test_bank_transfer():
    alice = BankAccount("Alice", 200.0)
    bob = BankAccount("Bob", 50.0)
    alice.transfer(bob, 75.0)
    assert alice.balance == 125.0
    assert bob.balance == 125.0

def test_bank_negative_deposit():
    acc = BankAccount("Test")
    try:
        acc.deposit(-10)
        assert False, "Expected ValueError"
    except ValueError:
        pass


# ===================================================================
# Tests -- Section 6: Stack Testing
# ===================================================================
def test_stack_push_pop():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.pop() == 1

def test_stack_peek():
    s = Stack()
    s.push("a")
    assert s.peek() == "a"
    assert len(s) == 1  # peek doesn't remove

def test_stack_empty():
    s = Stack()
    assert s.is_empty()
    s.push(1)
    assert not s.is_empty()

def test_stack_pop_empty():
    s = Stack()
    try:
        s.pop()
        assert False, "Expected IndexError"
    except IndexError:
        pass


# ===================================================================
# Standalone Test Runner
# ===================================================================
def run_all_tests():
    """Discover and run all test_* functions in this module."""
    import inspect

    current_module = sys.modules[__name__]
    test_functions = [
        (name, obj)
        for name, obj in inspect.getmembers(current_module, inspect.isfunction)
        if name.startswith("test_")
    ]

    passed = 0
    failed = 0
    errors = []

    for name, func in sorted(test_functions):
        try:
            func()
            status = "PASS"
            passed += 1
        except AssertionError as e:
            status = "FAIL"
            failed += 1
            errors.append((name, str(e)))
        except Exception as e:
            status = "ERROR"
            failed += 1
            errors.append((name, f"{type(e).__name__}: {e}"))

        dots = "." * (40 - len(name))
        print(f"  {name} {dots} {status}")

    print(f"\n{'=' * 50}")
    print(f"  {passed + failed} tests: {passed} passed, {failed} failed")
    print(f"{'=' * 50}")

    if errors:
        print("\nFailures:")
        for name, msg in errors:
            print(f"  {name}: {msg}")

    return failed == 0


# ===================================================================
# Main
# ===================================================================
import sys

if __name__ == "__main__":
    print("Running all tests...\n")
    success = run_all_tests()
    sys.exit(0 if success else 1)
