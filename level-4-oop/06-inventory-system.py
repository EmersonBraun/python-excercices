"""
Inventory Management System
==============================
Difficulty: 3/5
Estimated time: 25 minutes

Problem:
--------
Build an inventory system with the following classes:
1. Product (base) - name, sku, price, quantity.
2. PerishableProduct(Product) - adds expiry_date, is_expired().
3. DigitalProduct(Product) - adds file_size, download_link (infinite quantity).
4. Category - name, description, list of products.
5. Inventory - manages categories and products, supports search, stock alerts, reports.

Features:
- Add/remove products and categories.
- Restock and sell (adjust quantities).
- Search products by name, SKU, or price range.
- Low stock alerts.
- Inventory valuation report.

Concepts practiced:
- Inheritance and method overriding
- Composition (Inventory has Categories, Categories have Products)
- Property decorators
- Searching and filtering
- Formatted reporting

Expected output (example):
--------------------------
# === Inventory Report ===
# Category: Electronics (3 products)
#   SKU-001  Laptop          $999.99  x10  = $9999.90
#   SKU-002  Mouse           $29.99   x50  = $1499.50
#
# Total inventory value: $11,499.40
# Low stock items (< 5): [Keyboard (3 left)]
"""

from datetime import date, timedelta


class Product:
    """Base class for a product in inventory."""

    def __init__(self, name, sku, price, quantity=0):
        """
        Parameters:
            name (str): Product name.
            sku (str): Stock Keeping Unit identifier.
            price (float): Unit price.
            quantity (int): Current stock quantity.
        """
        self.name = name
        self.sku = sku
        self._price = price
        self._quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value

    @property
    def total_value(self):
        """Total value of this product's stock."""
        return self._price * self._quantity

    def restock(self, amount):
        """Add stock."""
        if amount <= 0:
            raise ValueError("Restock amount must be positive.")
        self._quantity += amount
        return self._quantity

    def sell(self, amount):
        """
        Sell units from stock.

        Returns:
            int: Number of units actually sold.
        """
        if amount <= 0:
            raise ValueError("Sell amount must be positive.")
        sold = min(amount, self._quantity)
        self._quantity -= sold
        return sold

    def __repr__(self):
        return f"Product({self.name!r}, sku={self.sku!r}, ${self.price:.2f}, qty={self.quantity})"

    def __str__(self):
        return f"{self.name} (${self.price:.2f})"


class PerishableProduct(Product):
    """A product with an expiry date."""

    def __init__(self, name, sku, price, quantity=0, expiry_date=None):
        """
        Parameters:
            expiry_date (date): The date the product expires.
        """
        super().__init__(name, sku, price, quantity)
        self.expiry_date = expiry_date

    @property
    def is_expired(self):
        """Check if the product has expired."""
        if self.expiry_date is None:
            return False
        return date.today() > self.expiry_date

    @property
    def days_until_expiry(self):
        """Days remaining until expiry (negative if expired)."""
        if self.expiry_date is None:
            return None
        return (self.expiry_date - date.today()).days

    def __repr__(self):
        exp = self.expiry_date.isoformat() if self.expiry_date else "N/A"
        return (
            f"PerishableProduct({self.name!r}, sku={self.sku!r}, "
            f"${self.price:.2f}, qty={self.quantity}, expires={exp})"
        )


class DigitalProduct(Product):
    """A digital product with unlimited stock."""

    def __init__(self, name, sku, price, file_size_mb=0, download_link=""):
        # Digital products have effectively infinite quantity
        super().__init__(name, sku, price, quantity=999999)
        self.file_size_mb = file_size_mb
        self.download_link = download_link

    def sell(self, amount):
        """Digital products never run out."""
        return amount  # always fulfills the full order

    @property
    def total_value(self):
        """Digital products don't have physical stock value in the same way."""
        return 0.0  # or could be price * licenses_sold

    def __repr__(self):
        return (
            f"DigitalProduct({self.name!r}, sku={self.sku!r}, "
            f"${self.price:.2f}, {self.file_size_mb}MB)"
        )


class Category:
    """A category containing products."""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.products = []

    def add_product(self, product):
        """Add a product to this category."""
        if any(p.sku == product.sku for p in self.products):
            print(f"Warning: SKU {product.sku} already in category '{self.name}'.")
            return False
        self.products.append(product)
        return True

    def remove_product(self, sku):
        """Remove a product by SKU."""
        for i, p in enumerate(self.products):
            if p.sku == sku:
                return self.products.pop(i)
        return None

    @property
    def total_value(self):
        """Total value of all products in this category."""
        return sum(p.total_value for p in self.products)

    @property
    def product_count(self):
        return len(self.products)

    def __repr__(self):
        return f"Category({self.name!r}, {self.product_count} products)"


class Inventory:
    """Main inventory manager."""

    def __init__(self, name="Inventory"):
        self.name = name
        self.categories = []

    def add_category(self, category):
        """Add a category."""
        self.categories.append(category)

    def find_category(self, name):
        """Find a category by name."""
        for c in self.categories:
            if c.name.lower() == name.lower():
                return c
        return None

    @property
    def all_products(self):
        """Flat list of all products across all categories."""
        products = []
        for cat in self.categories:
            products.extend(cat.products)
        return products

    # ---- Search ----

    def search_by_name(self, query):
        """Search products by name (case-insensitive partial match)."""
        return [p for p in self.all_products if query.lower() in p.name.lower()]

    def search_by_sku(self, sku):
        """Find a product by exact SKU."""
        for p in self.all_products:
            if p.sku == sku:
                return p
        return None

    def search_by_price_range(self, min_price, max_price):
        """Find products within a price range."""
        return [
            p for p in self.all_products
            if min_price <= p.price <= max_price
        ]

    # ---- Stock management ----

    def low_stock_items(self, threshold=5):
        """Return products with quantity below the threshold."""
        return [
            p for p in self.all_products
            if p.quantity < threshold and not isinstance(p, DigitalProduct)
        ]

    def expired_items(self):
        """Return expired perishable products."""
        return [
            p for p in self.all_products
            if isinstance(p, PerishableProduct) and p.is_expired
        ]

    # ---- Reports ----

    def report(self):
        """Print a full inventory report."""
        print(f"\n{'=' * 60}")
        print(f"  INVENTORY REPORT: {self.name}")
        print(f"{'=' * 60}")

        grand_total = 0.0

        for cat in self.categories:
            print(f"\n  Category: {cat.name} ({cat.product_count} products)")
            print(f"  {'-' * 54}")

            for p in cat.products:
                value = p.total_value
                grand_total += value
                extra = ""
                if isinstance(p, PerishableProduct):
                    days = p.days_until_expiry
                    if days is not None:
                        extra = f" [expires in {days}d]" if days > 0 else " [EXPIRED]"
                elif isinstance(p, DigitalProduct):
                    extra = f" [digital, {p.file_size_mb}MB]"

                print(
                    f"    {p.sku:10s} {p.name:20s} "
                    f"${p.price:>8.2f}  x{p.quantity:<5d} = ${value:>10.2f}{extra}"
                )

        print(f"\n  {'=' * 54}")
        print(f"  Total inventory value: ${grand_total:,.2f}")

        # Low stock alerts
        low = self.low_stock_items()
        if low:
            print(f"\n  Low stock alerts (< 5 units):")
            for p in low:
                print(f"    - {p.name}: {p.quantity} remaining")

        # Expired items
        expired = self.expired_items()
        if expired:
            print(f"\n  Expired items:")
            for p in expired:
                print(f"    - {p.name} (expired {p.expiry_date})")

        print(f"{'=' * 60}\n")


if __name__ == "__main__":
    print("--- Inventory System Demo ---\n")

    # Create inventory
    inv = Inventory("Tech Store")

    # Create categories
    electronics = Category("Electronics", "Electronic devices and accessories")
    software = Category("Software", "Digital software products")
    food = Category("Snacks", "Perishable food items")

    inv.add_category(electronics)
    inv.add_category(software)
    inv.add_category(food)

    # Add products
    laptop = Product("Laptop", "ELEC-001", 999.99, 10)
    mouse = Product("Wireless Mouse", "ELEC-002", 29.99, 50)
    keyboard = Product("Keyboard", "ELEC-003", 59.99, 3)  # low stock

    electronics.add_product(laptop)
    electronics.add_product(mouse)
    electronics.add_product(keyboard)

    # Digital products
    ide = DigitalProduct("Python IDE Pro", "SOFT-001", 49.99, file_size_mb=250,
                         download_link="https://example.com/ide")
    ebook = DigitalProduct("Python Ebook", "SOFT-002", 19.99, file_size_mb=15,
                           download_link="https://example.com/ebook")
    software.add_product(ide)
    software.add_product(ebook)

    # Perishable products
    chips = PerishableProduct("Chips", "FOOD-001", 3.99, 20,
                              expiry_date=date.today() + timedelta(days=30))
    expired_bar = PerishableProduct("Energy Bar", "FOOD-002", 2.49, 5,
                                    expiry_date=date.today() - timedelta(days=10))
    food.add_product(chips)
    food.add_product(expired_bar)

    # Full report
    inv.report()

    # Sell some items
    print("--- Sales ---")
    sold = laptop.sell(2)
    print(f"Sold {sold} laptops. Remaining: {laptop.quantity}")

    sold = ide.sell(5)
    print(f"Sold {sold} IDE licenses. (Digital: unlimited)")

    sold = keyboard.sell(10)  # only 3 available
    print(f"Tried to sell 10 keyboards, sold {sold}. Remaining: {keyboard.quantity}")
    print()

    # Restock
    print("--- Restock ---")
    keyboard.restock(20)
    print(f"Restocked keyboards: {keyboard.quantity}")
    print()

    # Search
    print("--- Search ---")
    results = inv.search_by_name("python")
    print(f"Search 'python': {[str(p) for p in results]}")

    result = inv.search_by_sku("ELEC-001")
    print(f"Search SKU 'ELEC-001': {result}")

    results = inv.search_by_price_range(10, 50)
    print(f"Price range $10-$50: {[str(p) for p in results]}")
    print()

    # Check perishable status
    print("--- Perishable Status ---")
    print(f"Chips expired? {chips.is_expired} (days left: {chips.days_until_expiry})")
    print(f"Energy Bar expired? {expired_bar.is_expired} (days: {expired_bar.days_until_expiry})")
