"""
Exercise 05 - Shopping Cart
=============================
Level: 2 - Functions & Collections
Difficulty: 3/5
Estimated Time: 20 minutes

Problem:
--------
Implement a shopping cart system using dictionaries that supports:
  1. Add items with name, price, and quantity
  2. Remove items from the cart
  3. Update item quantity
  4. Calculate subtotal, tax, and grand total
  5. Apply discount codes
  6. Display a formatted receipt

Expected Input/Output:
----------------------
# cart = ShoppingCart()
# cart.add_item("Apple", 0.99, 3)
# cart.add_item("Bread", 2.49, 1)
# cart.get_total()          -> 5.46
# cart.remove_item("Apple")
# cart.get_total()          -> 2.49
# cart.item_count()         -> 1
# cart.apply_discount(10)   -> applies 10% off
"""


class ShoppingCart:
    """A shopping cart that manages items, quantities, and pricing."""

    def __init__(self, tax_rate: float = 0.0):
        """
        Initialize an empty shopping cart.

        Args:
            tax_rate: Tax rate as a percentage (e.g., 8.5 for 8.5%).
        """
        self.items = {}  # {name: {"price": float, "quantity": int}}
        self.tax_rate = tax_rate
        self.discount_percent = 0.0

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        """
        Add an item to the cart. If it already exists, increase quantity.

        Args:
            name: Item name.
            price: Price per unit.
            quantity: Number of units to add.

        Raises:
            ValueError: If price < 0 or quantity < 1.
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name: str) -> None:
        """
        Remove an item completely from the cart.

        Args:
            name: Item name to remove.

        Raises:
            KeyError: If item is not in the cart.
        """
        if name not in self.items:
            raise KeyError(f"Item '{name}' not found in cart")
        del self.items[name]

    def update_quantity(self, name: str, quantity: int) -> None:
        """
        Update the quantity of an item. Remove if quantity is 0.

        Args:
            name: Item name.
            quantity: New quantity (0 removes the item).

        Raises:
            KeyError: If item is not in the cart.
            ValueError: If quantity is negative.
        """
        if name not in self.items:
            raise KeyError(f"Item '{name}' not found in cart")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if quantity == 0:
            self.remove_item(name)
        else:
            self.items[name]["quantity"] = quantity

    def get_subtotal(self) -> float:
        """Calculate the subtotal before tax and discounts."""
        return sum(
            item["price"] * item["quantity"]
            for item in self.items.values()
        )

    def get_discount_amount(self) -> float:
        """Calculate the discount amount based on the current discount percent."""
        return self.get_subtotal() * (self.discount_percent / 100)

    def get_tax_amount(self) -> float:
        """Calculate tax on the discounted subtotal."""
        discounted = self.get_subtotal() - self.get_discount_amount()
        return discounted * (self.tax_rate / 100)

    def get_total(self) -> float:
        """Calculate the grand total (subtotal - discount + tax)."""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        return round(subtotal - discount + tax, 2)

    def apply_discount(self, percent: float) -> None:
        """
        Apply a percentage discount to the cart.

        Args:
            percent: Discount percentage (0-100).

        Raises:
            ValueError: If percent is not between 0 and 100.
        """
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount_percent = percent

    def item_count(self) -> int:
        """Return the total number of items (sum of all quantities)."""
        return sum(item["quantity"] for item in self.items.values())

    def is_empty(self) -> bool:
        """Check if the cart is empty."""
        return len(self.items) == 0

    def clear(self) -> None:
        """Remove all items from the cart."""
        self.items.clear()
        self.discount_percent = 0.0

    def get_item(self, name: str) -> dict:
        """
        Get details of a specific item.

        Args:
            name: Item name.

        Returns:
            Dict with price and quantity.

        Raises:
            KeyError: If item not found.
        """
        if name not in self.items:
            raise KeyError(f"Item '{name}' not found in cart")
        return self.items[name].copy()

    def list_items(self) -> list:
        """
        Return a list of all items with their details.

        Returns:
            List of dicts with name, price, quantity, and line_total.
        """
        return [
            {
                "name": name,
                "price": info["price"],
                "quantity": info["quantity"],
                "line_total": round(info["price"] * info["quantity"], 2),
            }
            for name, info in self.items.items()
        ]

    def receipt(self) -> str:
        """Generate a formatted receipt string."""
        lines = []
        lines.append("=" * 45)
        lines.append("           SHOPPING RECEIPT")
        lines.append("=" * 45)
        lines.append(f"{'Item':<20} {'Qty':>4} {'Price':>8} {'Total':>8}")
        lines.append("-" * 45)

        for name, info in self.items.items():
            qty = info["quantity"]
            price = info["price"]
            total = price * qty
            lines.append(f"{name:<20} {qty:>4} ${price:>7.2f} ${total:>7.2f}")

        lines.append("-" * 45)

        subtotal = self.get_subtotal()
        lines.append(f"{'Subtotal:':<34} ${subtotal:>7.2f}")

        if self.discount_percent > 0:
            discount = self.get_discount_amount()
            lines.append(f"{'Discount (' + str(self.discount_percent) + '%):':<34} -${discount:>6.2f}")

        if self.tax_rate > 0:
            tax = self.get_tax_amount()
            lines.append(f"{'Tax (' + str(self.tax_rate) + '%):':<34} ${tax:>7.2f}")

        lines.append("=" * 45)
        total = self.get_total()
        lines.append(f"{'TOTAL:':<34} ${total:>7.2f}")
        lines.append("=" * 45)
        lines.append(f"  Items in cart: {self.item_count()}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"ShoppingCart(items={len(self.items)}, total=${self.get_total():.2f})"


if __name__ == "__main__":
    print("=" * 50)
    print("  Shopping Cart Demo")
    print("=" * 50)

    # Create cart with 8.5% tax
    cart = ShoppingCart(tax_rate=8.5)

    # Add items
    print("\n--- Adding Items ---")
    cart.add_item("Apple", 0.99, 5)
    cart.add_item("Bread", 2.49, 2)
    cart.add_item("Milk", 3.99, 1)
    cart.add_item("Cheese", 4.99, 1)
    cart.add_item("Eggs", 3.49, 2)

    for item in cart.list_items():
        print(f"  {item['name']}: {item['quantity']}x ${item['price']:.2f} = ${item['line_total']:.2f}")

    print(f"\n  Cart: {cart}")

    # Update quantity
    print("\n--- Update Quantity ---")
    cart.update_quantity("Apple", 3)
    apple = cart.get_item("Apple")
    print(f"  Apple quantity updated to {apple['quantity']}")

    # Remove item
    print("\n--- Remove Item ---")
    cart.remove_item("Cheese")
    print(f"  Cheese removed. Items: {cart.item_count()}")

    # Apply discount
    print("\n--- Apply 15% Discount ---")
    cart.apply_discount(15)

    # Print receipt
    print("\n" + cart.receipt())

    # Error handling
    print("\n--- Error Handling ---")
    try:
        cart.remove_item("Pizza")
    except KeyError as e:
        print(f"  Remove 'Pizza': {e}")

    try:
        cart.add_item("Bad", -5.0)
    except ValueError as e:
        print(f"  Negative price: {e}")

    try:
        cart.apply_discount(150)
    except ValueError as e:
        print(f"  Invalid discount: {e}")

    # Clear cart
    print("\n--- Clear Cart ---")
    cart.clear()
    print(f"  Cart empty: {cart.is_empty()}")
    print(f"  Item count: {cart.item_count()}")

    print("\nShopping cart exercise complete!")
