"""
Level 5 - Exercise 05: Type Annotations & Dataclasses
=======================================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Learn to use Python type hints, dataclasses, and runtime validation
to create robust, self-documenting data structures.

Exercises
---------
1. Typed functions    - Functions with full type annotations.
2. Product dataclass  - Dataclass with __post_init__ validation.
3. Inventory system   - Generic container with type-safe operations.
4. User dataclass     - Nested dataclasses with default_factory.

Expected output (approximate):
------------------------------
# merge_dicts({'a': 1}, {'b': 2}) -> {'a': 1, 'b': 2}
# Product(name='Widget', price=9.99, quantity=100)
# Inventory: 3 items, total value = $59.94
# User(name='Alice', email='alice@example.com', orders=[...])
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional
from datetime import datetime


# ---------------------------------------------------------------------------
# 1. Typed Functions
# ---------------------------------------------------------------------------
def merge_dicts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """Merge two dictionaries; values for duplicate keys are summed.

    >>> merge_dicts({'x': 1, 'y': 2}, {'y': 3, 'z': 4})
    {'x': 1, 'y': 5, 'z': 4}
    """
    result: dict[str, int] = {**a}
    for key, value in b.items():
        result[key] = result.get(key, 0) + value
    return result


def first_or_default(items: list[str], default: str = "") -> str:
    """Return the first element or *default* if the list is empty.

    >>> first_or_default(["hello", "world"])
    'hello'
    >>> first_or_default([])
    ''
    """
    return items[0] if items else default


def safe_divide(a: float, b: float) -> Optional[float]:
    """Divide a by b, returning None instead of raising ZeroDivisionError.

    >>> safe_divide(10, 3)
    3.3333333333333335
    >>> safe_divide(10, 0) is None
    True
    """
    if b == 0:
        return None
    return a / b


# ---------------------------------------------------------------------------
# 2. Product Dataclass with Validation
# ---------------------------------------------------------------------------
@dataclass
class Product:
    """Represents a product with runtime validation.

    Validates that:
    - name is a non-empty string
    - price is a positive number
    - quantity is a non-negative integer

    >>> p = Product("Widget", 9.99, 100)
    >>> p.total_value
    999.0
    """
    name: str
    price: float
    quantity: int = 0

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError(f"name must be a non-empty string, got {self.name!r}")
        if self.price <= 0:
            raise ValueError(f"price must be positive, got {self.price}")
        if self.quantity < 0:
            raise ValueError(f"quantity must be >= 0, got {self.quantity}")

    @property
    def total_value(self) -> float:
        return round(self.price * self.quantity, 2)

    def restock(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("restock amount must be non-negative")
        self.quantity += amount

    def sell(self, amount: int) -> bool:
        if amount > self.quantity:
            return False
        self.quantity -= amount
        return True


# ---------------------------------------------------------------------------
# 3. Generic Inventory Container
# ---------------------------------------------------------------------------
T = TypeVar("T")


@dataclass
class Inventory(Generic[T]):
    """A type-safe container for items with add/remove/search.

    >>> inv = Inventory[Product]()
    >>> inv.add(Product("Bolt", 0.5, 1000))
    >>> len(inv)
    1
    """
    _items: list[T] = field(default_factory=list, repr=False)

    def add(self, item: T) -> None:
        self._items.append(item)

    def remove(self, item: T) -> bool:
        try:
            self._items.remove(item)
            return True
        except ValueError:
            return False

    def find(self, predicate) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def find_all(self, predicate) -> list[T]:
        return [item for item in self._items if predicate(item)]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Inventory({len(self._items)} items)"


# ---------------------------------------------------------------------------
# 4. Nested Dataclasses -- User + Order
# ---------------------------------------------------------------------------
@dataclass
class OrderItem:
    """Single item in an order."""
    product_name: str
    unit_price: float
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)


@dataclass
class Order:
    """An order containing one or more OrderItems."""
    order_id: int
    items: list[OrderItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def __repr__(self) -> str:
        return (f"Order(id={self.order_id}, items={len(self.items)}, "
                f"total=${self.total:.2f})")


@dataclass
class User:
    """User with email validation and a list of orders.

    >>> u = User("Alice", "alice@example.com")
    >>> u.place_order([OrderItem("Widget", 9.99, 2)])
    """
    name: str
    email: str
    orders: list[Order] = field(default_factory=list)
    _next_order_id: int = field(default=1, repr=False)

    def __post_init__(self) -> None:
        if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", self.email):
            raise ValueError(f"Invalid email: {self.email!r}")

    def place_order(self, items: list[OrderItem]) -> Order:
        order = Order(order_id=self._next_order_id, items=items)
        self.orders.append(order)
        self._next_order_id += 1
        return order

    @property
    def total_spent(self) -> float:
        return round(sum(o.total for o in self.orders), 2)


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    # --- 1. Typed functions ---
    print("=" * 50)
    print("1. Typed Functions")
    print("=" * 50)
    print(f"merge_dicts({{'x':1,'y':2}}, {{'y':3,'z':4}}) = "
          f"{merge_dicts({'x': 1, 'y': 2}, {'y': 3, 'z': 4})}")
    print(f"first_or_default(['hello', 'world']) = "
          f"{first_or_default(['hello', 'world'])!r}")
    print(f"first_or_default([]) = {first_or_default([])!r}")
    print(f"safe_divide(10, 3) = {safe_divide(10, 3)}")
    print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")
    print()

    # --- 2. Product dataclass ---
    print("=" * 50)
    print("2. Product Dataclass")
    print("=" * 50)
    widget = Product("Widget", 9.99, 100)
    print(f"Product: {widget}")
    print(f"Total value: ${widget.total_value:.2f}")
    widget.sell(10)
    print(f"After selling 10: quantity={widget.quantity}")
    widget.restock(50)
    print(f"After restocking 50: quantity={widget.quantity}")

    # Validation demo
    try:
        bad = Product("", 9.99)
    except ValueError as e:
        print(f"Validation error: {e}")
    try:
        bad = Product("Bad", -5.0)
    except ValueError as e:
        print(f"Validation error: {e}")
    print()

    # --- 3. Inventory ---
    print("=" * 50)
    print("3. Generic Inventory")
    print("=" * 50)
    inv: Inventory[Product] = Inventory()
    inv.add(Product("Bolt", 0.50, 1000))
    inv.add(Product("Nut", 0.30, 2000))
    inv.add(Product("Washer", 0.10, 5000))
    print(f"Inventory: {inv}")
    expensive = inv.find(lambda p: p.price > 0.25)
    print(f"First product > $0.25: {expensive}")
    cheap_items = inv.find_all(lambda p: p.price <= 0.30)
    print(f"Products <= $0.30: {[p.name for p in cheap_items]}")
    total_value = sum(p.total_value for p in inv)
    print(f"Total inventory value: ${total_value:.2f}")
    print()

    # --- 4. User + Orders ---
    print("=" * 50)
    print("4. User with Orders")
    print("=" * 50)
    alice = User("Alice", "alice@example.com")
    order1 = alice.place_order([
        OrderItem("Widget", 9.99, 2),
        OrderItem("Gadget", 24.99, 1),
    ])
    order2 = alice.place_order([
        OrderItem("Bolt", 0.50, 100),
    ])
    print(f"User: {alice.name} ({alice.email})")
    for order in alice.orders:
        print(f"  {order}")
    print(f"Total spent: ${alice.total_spent:.2f}")

    # Validation demo
    try:
        bad_user = User("Bob", "not-an-email")
    except ValueError as e:
        print(f"Validation error: {e}")
