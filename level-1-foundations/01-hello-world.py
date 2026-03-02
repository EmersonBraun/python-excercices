"""
Exercise 01 - Hello World Variants
===================================
Level: 1 - Foundations
Difficulty: 1/5
Estimated Time: 5 minutes

Problem:
--------
Explore different ways to output text in Python.
Implement functions that demonstrate:
  1. Basic print statements
  2. String concatenation
  3. str.format() method
  4. f-strings (formatted string literals)
  5. %-formatting (old style)

Expected Input/Output:
----------------------
# greet_basic("Alice")       -> prints "Hello, Alice!"
# greet_concat("Bob")        -> prints "Hello, Bob!"
# greet_format("Charlie")    -> prints "Hello, Charlie! Welcome to Python."
# greet_fstring("Diana", 25) -> prints "Hello, Diana! You are 25 years old."
# greet_percent("Eve")       -> prints "Hello, Eve!"
# multi_line_greeting("Frank") -> prints a 3-line greeting
"""


def greet_basic(name: str) -> None:
    """Print a basic greeting using a simple print statement."""
    print("Hello, " + name + "!")


def greet_concat(name: str) -> str:
    """Return a greeting built with string concatenation."""
    greeting = "Hello, " + name + "!"
    return greeting


def greet_format(name: str) -> str:
    """Return a greeting using str.format() method."""
    return "Hello, {}! Welcome to Python.".format(name)


def greet_fstring(name: str, age: int) -> str:
    """Return a greeting using f-string with name and age."""
    return f"Hello, {name}! You are {age} years old."


def greet_percent(name: str) -> str:
    """Return a greeting using %-formatting (old style)."""
    return "Hello, %s!" % name


def multi_line_greeting(name: str) -> str:
    """Return a multi-line greeting using triple-quoted strings."""
    return f"""==========================
  Welcome, {name}!
  Enjoy learning Python!
=========================="""


def repeat_greeting(name: str, times: int = 3) -> list:
    """Return a list of greetings repeated 'times' number of times."""
    return [f"Hello, {name}! (#{i + 1})" for i in range(times)]


if __name__ == "__main__":
    print("=" * 40)
    print("  Hello World Variants Demo")
    print("=" * 40)

    # 1. Basic print
    print("\n--- Basic Print ---")
    greet_basic("Alice")

    # 2. Concatenation
    print("\n--- Concatenation ---")
    result = greet_concat("Bob")
    print(result)

    # 3. str.format()
    print("\n--- str.format() ---")
    result = greet_format("Charlie")
    print(result)

    # 4. f-strings
    print("\n--- f-strings ---")
    result = greet_fstring("Diana", 25)
    print(result)

    # 5. %-formatting
    print("\n--- %-formatting ---")
    result = greet_percent("Eve")
    print(result)

    # 6. Multi-line
    print("\n--- Multi-line Greeting ---")
    result = multi_line_greeting("Frank")
    print(result)

    # 7. Repeat greeting
    print("\n--- Repeated Greetings ---")
    greetings = repeat_greeting("Grace", 3)
    for g in greetings:
        print(g)

    print("\nAll Hello World variants demonstrated!")
