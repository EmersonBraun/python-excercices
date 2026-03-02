"""
Level 5 - Exercise 06: Metaclasses
====================================

Difficulty: 5/5 stars
Estimated time: 30 minutes

Explore Python metaclasses -- classes whose instances are themselves
classes.  Metaclasses let you customise class creation, enforce
constraints, and implement advanced patterns like singletons.

Exercises
---------
1. AutoPropertyMeta  - Automatically creates properties from _fields.
2. ValidatedMeta     - Enforces type annotations at attribute assignment.
3. SingletonMeta     - Ensures only one instance of a class exists.
4. RegistryMeta      - Auto-registers every subclass in a central dict.

Expected output (approximate):
------------------------------
# AutoPropertyMeta
# p.name -> 'Widget'  (auto-generated property)

# ValidatedMeta
# Setting price to "not a number" -> TypeError

# SingletonMeta
# db1 is db2 -> True

# RegistryMeta
# Registry: {'Circle': <class 'Circle'>, 'Square': <class 'Square'>}
"""


# ---------------------------------------------------------------------------
# 1. AutoPropertyMeta
#    Reads a class-level `_fields` tuple and creates read/write properties
#    backed by a private attribute for each field.
# ---------------------------------------------------------------------------
class AutoPropertyMeta(type):
    """Metaclass that auto-generates properties from a `_fields` tuple.

    Any class using this metaclass can declare::

        _fields = ("name", "price", "quantity")

    and the metaclass will create a property for each field that stores
    the value in ``self._<field>`` and provides a getter/setter.

    >>> class Item(metaclass=AutoPropertyMeta):
    ...     _fields = ("name", "price")
    >>> i = Item()
    >>> i.name = "Bolt"
    >>> i.name
    'Bolt'
    """

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        for field_name in namespace.get("_fields", ()):
            private = f"_{field_name}"

            def make_property(priv):
                def getter(self):
                    return getattr(self, priv, None)

                def setter(self, value):
                    setattr(self, priv, value)

                return property(getter, setter)

            setattr(cls, field_name, make_property(private))
        return cls


# ---------------------------------------------------------------------------
# 2. ValidatedMeta
#    Enforces that attribute assignments respect type annotations.
# ---------------------------------------------------------------------------
class ValidatedMeta(type):
    """Metaclass that enforces type annotations at assignment time.

    Classes using this metaclass will raise TypeError if you try to set
    an annotated attribute to a value of the wrong type.

    >>> class Config(metaclass=ValidatedMeta):
    ...     debug: bool = False
    ...     port: int = 8080
    >>> c = Config()
    >>> c.port = "abc"   # raises TypeError
    """

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        annotations = namespace.get("__annotations__", {})

        # Store annotations for the custom __setattr__
        cls.__field_types__ = dict(annotations)

        original_setattr = cls.__setattr__

        def validated_setattr(self, attr, value):
            expected = self.__class__.__field_types__.get(attr)
            if expected is not None and not isinstance(value, expected):
                raise TypeError(
                    f"Attribute '{attr}' expects {expected.__name__}, "
                    f"got {type(value).__name__}"
                )
            object.__setattr__(self, attr, value)

        cls.__setattr__ = validated_setattr
        return cls


# ---------------------------------------------------------------------------
# 3. SingletonMeta
#    Ensures that only one instance of a class is ever created.
# ---------------------------------------------------------------------------
class SingletonMeta(type):
    """Metaclass that implements the Singleton pattern.

    Repeated calls to the class constructor return the same instance.

    >>> class DB(metaclass=SingletonMeta):
    ...     pass
    >>> DB() is DB()
    True
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# ---------------------------------------------------------------------------
# 4. RegistryMeta
#    Auto-registers every subclass in a central dictionary.
# ---------------------------------------------------------------------------
class RegistryMeta(type):
    """Metaclass that keeps a registry of all subclasses.

    The base class gets a ``_registry`` dict mapping class names to classes.

    >>> class Shape(metaclass=RegistryMeta):
    ...     pass
    >>> class Circle(Shape):
    ...     pass
    >>> Shape._registry
    {'Circle': <class '__main__.Circle'>}
    """

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "_registry"):
            # This is the base class -- create the registry
            cls._registry = {}
        else:
            # This is a subclass -- register it
            cls._registry[name] = cls


# ===================================================================
# Demo classes that USE the metaclasses
# ===================================================================

# --- AutoPropertyMeta usage ---
class Product(metaclass=AutoPropertyMeta):
    _fields = ("name", "price", "quantity")

    def __init__(self, name="", price=0.0, quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, qty={self.quantity})"


# --- ValidatedMeta usage ---
class ServerConfig(metaclass=ValidatedMeta):
    host: str = "localhost"
    port: int = 8080
    debug: bool = False

    def __init__(self, host="localhost", port=8080, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    def __repr__(self):
        return f"ServerConfig(host={self.host!r}, port={self.port}, debug={self.debug})"


# --- SingletonMeta usage ---
class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, dsn="sqlite:///app.db"):
        self.dsn = dsn
        self.connected = False

    def connect(self):
        self.connected = True
        print(f"Connected to {self.dsn}")

    def __repr__(self):
        return f"DatabaseConnection(dsn={self.dsn!r}, connected={self.connected})"


# --- RegistryMeta usage ---
class Shape(metaclass=RegistryMeta):
    """Base shape class -- all subclasses are automatically registered."""

    def area(self):
        raise NotImplementedError


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def __repr__(self):
        return f"Circle(radius={self.radius})"


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def __repr__(self):
        return f"Square(side={self.side})"


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def __repr__(self):
        return f"Triangle(base={self.base}, height={self.height})"


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    # --- 1. AutoPropertyMeta ---
    print("=" * 50)
    print("1. AutoPropertyMeta")
    print("=" * 50)
    p = Product("Widget", 9.99, 100)
    print(f"Product: {p}")
    p.price = 12.50
    print(f"After price update: {p}")
    print()

    # --- 2. ValidatedMeta ---
    print("=" * 50)
    print("2. ValidatedMeta")
    print("=" * 50)
    cfg = ServerConfig("0.0.0.0", 3000, True)
    print(f"Config: {cfg}")
    cfg.port = 5000
    print(f"After port change: {cfg}")

    print("Attempting invalid assignment...")
    try:
        cfg.port = "not a number"
    except TypeError as e:
        print(f"  TypeError caught: {e}")

    try:
        cfg.debug = "yes"
    except TypeError as e:
        print(f"  TypeError caught: {e}")
    print()

    # --- 3. SingletonMeta ---
    print("=" * 50)
    print("3. SingletonMeta")
    print("=" * 50)
    db1 = DatabaseConnection("postgres://localhost/mydb")
    db1.connect()
    db2 = DatabaseConnection("mysql://other/db")  # ignored -- same instance
    print(f"db1: {db1}")
    print(f"db2: {db2}")
    print(f"db1 is db2: {db1 is db2}")
    print()

    # --- 4. RegistryMeta ---
    print("=" * 50)
    print("4. RegistryMeta")
    print("=" * 50)
    print(f"Shape registry: {Shape._registry}")
    print("\nCreating shapes from registry:")
    for name, cls in Shape._registry.items():
        if name == "Circle":
            shape = cls(5)
        elif name == "Square":
            shape = cls(4)
        elif name == "Triangle":
            shape = cls(6, 3)
        else:
            continue
        print(f"  {shape}  ->  area = {shape.area():.2f}")
