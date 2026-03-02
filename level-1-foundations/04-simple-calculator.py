"""
Exercise 04 - Simple Calculator
================================
Level: 1 - Foundations
Difficulty: 2/5
Estimated Time: 15 minutes

Problem:
--------
Create a calculator that supports the following operations:
  + (addition), - (subtraction), * (multiplication),
  / (division), ** (exponentiation), % (modulus)

Handle edge cases like division by zero.

Expected Input/Output:
----------------------
# calculate(10, 5, '+')  -> 15
# calculate(10, 5, '-')  -> 5
# calculate(10, 5, '*')  -> 50
# calculate(10, 5, '/')  -> 2.0
# calculate(10, 3, '**') -> 1000
# calculate(10, 3, '%')  -> 1
# calculate(10, 0, '/')  -> raises ValueError
"""


def calculate(a: float, b: float, operator: str) -> float:
    """
    Perform a calculation with two numbers and an operator.

    Args:
        a: First operand.
        b: Second operand.
        operator: One of '+', '-', '*', '/', '**', '%'.

    Returns:
        The result of the operation.

    Raises:
        ValueError: If division/modulus by zero or invalid operator.
    """
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    elif operator == "**":
        return a ** b
    elif operator == "%":
        if b == 0:
            raise ValueError("Cannot perform modulus by zero")
        return a % b
    else:
        raise ValueError(f"Invalid operator: '{operator}'. Use +, -, *, /, **, or %")


def calculate_expression(expression: str) -> float:
    """
    Parse and evaluate a simple math expression string like '10 + 5'.

    Args:
        expression: A string with format 'number operator number'.

    Returns:
        The result of the calculation.
    """
    parts = expression.split()
    if len(parts) != 3:
        raise ValueError("Expression must be in format: 'number operator number'")

    a = float(parts[0])
    operator = parts[1]
    b = float(parts[2])

    return calculate(a, b, operator)


def calculator_history() -> dict:
    """
    Return a calculator object that keeps history of operations.

    Returns:
        A dict with 'calculate' function and 'history' list.
    """
    history = []

    def calc(a: float, b: float, operator: str) -> float:
        result = calculate(a, b, operator)
        history.append({
            "expression": f"{a} {operator} {b}",
            "result": result,
        })
        return result

    return {"calculate": calc, "history": history}


if __name__ == "__main__":
    print("=" * 40)
    print("  Simple Calculator Demo")
    print("=" * 40)

    # Basic operations
    print("\n--- Basic Operations ---")
    operations = [
        (10, 5, "+"),
        (10, 5, "-"),
        (10, 5, "*"),
        (10, 5, "/"),
        (2, 10, "**"),
        (10, 3, "%"),
    ]

    for a, b, op in operations:
        result = calculate(a, b, op)
        print(f"  {a} {op} {b} = {result}")

    # Division by zero handling
    print("\n--- Error Handling ---")
    try:
        calculate(10, 0, "/")
    except ValueError as e:
        print(f"  10 / 0 -> Error: {e}")

    try:
        calculate(10, 0, "%")
    except ValueError as e:
        print(f"  10 % 0 -> Error: {e}")

    try:
        calculate(10, 5, "^")
    except ValueError as e:
        print(f"  10 ^ 5 -> Error: {e}")

    # Expression parser
    print("\n--- Expression Parser ---")
    expressions = ["15 + 7", "100 / 4", "3 ** 3", "17 % 5"]
    for expr in expressions:
        result = calculate_expression(expr)
        print(f"  '{expr}' = {result}")

    # Calculator with history
    print("\n--- Calculator with History ---")
    calc = calculator_history()
    calc["calculate"](100, 25, "+")
    calc["calculate"](125, 5, "*")
    calc["calculate"](625, 2, "**")

    for entry in calc["history"]:
        print(f"  {entry['expression']} = {entry['result']}")

    print("\nCalculator exercise complete!")
