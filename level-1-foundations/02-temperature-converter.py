"""
Exercise 02 - Temperature Converter
=====================================
Level: 1 - Foundations
Difficulty: 1/5
Estimated Time: 10 minutes

Problem:
--------
Create functions to convert temperatures between Celsius, Fahrenheit, and Kelvin.

Formulas:
  - F = C * 9/5 + 32
  - C = (F - 32) * 5/9
  - K = C + 273.15
  - C = K - 273.15

Expected Input/Output:
----------------------
# celsius_to_fahrenheit(0)    -> 32.0
# celsius_to_fahrenheit(100)  -> 212.0
# fahrenheit_to_celsius(32)   -> 0.0
# fahrenheit_to_celsius(212)  -> 100.0
# celsius_to_kelvin(0)        -> 273.15
# kelvin_to_celsius(273.15)   -> 0.0
# fahrenheit_to_kelvin(32)    -> 273.15
# kelvin_to_fahrenheit(373.15)-> 212.0
"""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin."""
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert Fahrenheit to Kelvin."""
    celsius = fahrenheit_to_celsius(fahrenheit)
    return celsius_to_kelvin(celsius)


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    celsius = kelvin_to_celsius(kelvin)
    return celsius_to_fahrenheit(celsius)


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    General-purpose temperature converter.

    Args:
        value: The temperature value to convert.
        from_unit: Source unit ('C', 'F', or 'K').
        to_unit: Target unit ('C', 'F', or 'K').

    Returns:
        The converted temperature rounded to 2 decimal places.

    Raises:
        ValueError: If an invalid unit is provided.
    """
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    valid_units = {"C", "F", "K"}
    if from_unit not in valid_units or to_unit not in valid_units:
        raise ValueError(f"Invalid unit. Use 'C', 'F', or 'K'. Got: {from_unit}, {to_unit}")

    if from_unit == to_unit:
        return round(value, 2)

    converters = {
        ("C", "F"): celsius_to_fahrenheit,
        ("F", "C"): fahrenheit_to_celsius,
        ("C", "K"): celsius_to_kelvin,
        ("K", "C"): kelvin_to_celsius,
        ("F", "K"): fahrenheit_to_kelvin,
        ("K", "F"): kelvin_to_fahrenheit,
    }

    result = converters[(from_unit, to_unit)](value)
    return round(result, 2)


if __name__ == "__main__":
    print("=" * 40)
    print("  Temperature Converter Demo")
    print("=" * 40)

    # Celsius to Fahrenheit
    print("\n--- Celsius -> Fahrenheit ---")
    for c in [0, 100, -40, 37]:
        f = celsius_to_fahrenheit(c)
        print(f"  {c}°C = {f:.2f}°F")

    # Fahrenheit to Celsius
    print("\n--- Fahrenheit -> Celsius ---")
    for f in [32, 212, -40, 98.6]:
        c = fahrenheit_to_celsius(f)
        print(f"  {f}°F = {c:.2f}°C")

    # Celsius to Kelvin
    print("\n--- Celsius -> Kelvin ---")
    for c in [0, 100, -273.15]:
        k = celsius_to_kelvin(c)
        print(f"  {c}°C = {k:.2f}K")

    # Kelvin to Fahrenheit
    print("\n--- Kelvin -> Fahrenheit ---")
    for k in [0, 273.15, 373.15]:
        f = kelvin_to_fahrenheit(k)
        print(f"  {k}K = {f:.2f}°F")

    # General converter
    print("\n--- General Converter ---")
    print(f"  100°C -> K: {convert_temperature(100, 'C', 'K')}K")
    print(f"  32°F -> C: {convert_temperature(32, 'F', 'C')}°C")
    print(f"  300K -> F: {convert_temperature(300, 'K', 'F')}°F")

    print("\nAll temperature conversions demonstrated!")
