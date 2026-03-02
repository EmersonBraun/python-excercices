"""
Shape Hierarchy (Abstract Base Classes)
=========================================
Difficulty: 3/5
Estimated time: 20 minutes

Problem:
--------
Create an abstract Shape class and concrete subclasses:
1. Shape (ABC) - abstract methods: area(), perimeter(), describe().
2. Circle - defined by radius.
3. Rectangle - defined by width and height.
4. Triangle - defined by three side lengths (with validation).

Each shape should:
- Compute its area and perimeter.
- Provide a human-readable description.
- Support comparison by area (==, <, >).
- Have a __repr__ for debugging.

Concepts practiced:
- Abstract Base Classes (abc module)
- Inheritance and method overriding
- Operator overloading
- math module
- Input validation

Expected output (example):
--------------------------
# Circle(radius=5)
#   Area:      78.54
#   Perimeter: 31.42
#
# Rectangle(width=4, height=6)
#   Area:      24.00
#   Perimeter: 20.00
#
# Triangle(a=3, b=4, c=5)
#   Area:      6.00
#   Perimeter: 12.00
#
# Sorted by area: [Triangle(6.00), Rectangle(24.00), Circle(78.54)]
"""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for geometric shapes."""

    @abstractmethod
    def area(self):
        """Calculate and return the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self):
        """Calculate and return the perimeter of the shape."""
        pass

    def describe(self):
        """Print a description of the shape with area and perimeter."""
        print(f"{self!r}")
        print(f"  Area:      {self.area():.2f}")
        print(f"  Perimeter: {self.perimeter():.2f}")

    # Comparison by area
    def __eq__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return math.isclose(self.area(), other.area(), rel_tol=1e-9)

    def __lt__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()

    def __gt__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() > other.area()

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other


class Circle(Shape):
    """A circle defined by its radius."""

    def __init__(self, radius):
        if radius <= 0:
            raise ValueError(f"Radius must be positive, got {radius}")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def __repr__(self):
        return f"Circle(radius={self.radius})"


class Rectangle(Shape):
    """A rectangle defined by width and height."""

    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError(f"Dimensions must be positive, got width={width}, height={height}")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    @property
    def is_square(self):
        """Check if this rectangle is a square."""
        return math.isclose(self.width, self.height)

    def __repr__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


class Triangle(Shape):
    """A triangle defined by three side lengths. Uses Heron's formula for area."""

    def __init__(self, a, b, c):
        # Validate positive sides
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError(f"All sides must be positive, got a={a}, b={b}, c={c}")

        # Triangle inequality
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError(
                f"Invalid triangle: sides ({a}, {b}, {c}) violate the triangle inequality."
            )

        self.a = a
        self.b = b
        self.c = c

    def area(self):
        """Calculate area using Heron's formula."""
        s = self.perimeter() / 2  # semi-perimeter
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c

    @property
    def is_right_triangle(self):
        """Check if this is a right triangle (Pythagorean theorem)."""
        sides = sorted([self.a, self.b, self.c])
        return math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2)

    def __repr__(self):
        return f"Triangle(a={self.a}, b={self.b}, c={self.c})"


if __name__ == "__main__":
    print("--- Shape Hierarchy Demo ---\n")

    # Create shapes
    circle = Circle(5)
    rect = Rectangle(4, 6)
    triangle = Triangle(3, 4, 5)
    square = Rectangle(5, 5)

    # Describe each
    for shape in [circle, rect, triangle, square]:
        shape.describe()
        print()

    # Special properties
    print(f"Is {rect!r} a square? {rect.is_square}")
    print(f"Is {square!r} a square? {square.is_square}")
    print(f"Is {triangle!r} a right triangle? {triangle.is_right_triangle}")
    print()

    # Comparisons
    print("--- Comparisons (by area) ---")
    print(f"Circle > Rectangle? {circle > rect}")
    print(f"Triangle < Rectangle? {triangle < rect}")
    print()

    # Sort shapes by area
    shapes = [circle, rect, triangle, square]
    sorted_shapes = sorted(shapes)
    print("Sorted by area (ascending):")
    for s in sorted_shapes:
        print(f"  {s!r:40s} area = {s.area():.2f}")
    print()

    # Validation errors
    print("--- Validation Errors ---")
    try:
        Circle(-1)
    except ValueError as e:
        print(f"Circle(-1): {e}")

    try:
        Triangle(1, 2, 10)
    except ValueError as e:
        print(f"Triangle(1, 2, 10): {e}")

    # Demonstrate abstract class cannot be instantiated
    try:
        Shape()
    except TypeError as e:
        print(f"Shape(): {e}")
