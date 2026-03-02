"""
Design Patterns: Singleton, Observer, Factory
===============================================
Difficulty: 4/5
Estimated time: 30 minutes

Problem:
--------
Implement three classic design patterns in Python:

1. Singleton - Ensure a class has only one instance (e.g., AppConfig).
2. Observer  - Publish/subscribe pattern (e.g., EventSystem with listeners).
3. Factory   - Create objects without specifying exact classes (e.g., VehicleFactory).

Concepts practiced:
- Design patterns
- Metaclasses / __new__ override
- Callbacks and loose coupling
- Class registration and dynamic instantiation
- Abstract base classes

Expected output (example):
--------------------------
# === Singleton ===
# AppConfig instance 1: {'debug': False}
# AppConfig instance 2 is same object? True
#
# === Observer ===
# Logger received 'user_login': {'user': 'alice'}
# Dashboard received 'user_login': {'user': 'alice'}
#
# === Factory ===
# Created: Car(engine=V6, doors=4, fuel=gasoline)
# Created: Motorcycle(engine=V2, doors=0, fuel=gasoline)
"""

from abc import ABC, abstractmethod


# ============================================================
# PATTERN 1: Singleton
# ============================================================

class SingletonMeta(type):
    """
    Metaclass that ensures only one instance of a class is created.
    Thread-safe variant would use a lock, but this is kept simple.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    """Application configuration that uses the Singleton pattern."""

    def __init__(self):
        # Only runs once due to Singleton
        self.settings = {
            "debug": False,
            "log_level": "INFO",
            "max_connections": 10,
        }

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value

    def __repr__(self):
        return f"AppConfig({self.settings})"


# ============================================================
# PATTERN 2: Observer (Publish / Subscribe)
# ============================================================

class EventSystem:
    """
    A simple event system implementing the Observer pattern.
    Publishers emit events; subscribers listen for specific event types.
    """

    def __init__(self):
        self._listeners = {}  # event_type -> list of callback functions

    def subscribe(self, event_type, callback):
        """
        Subscribe a callback to an event type.

        Parameters:
            event_type (str): Name of the event (e.g., 'user_login').
            callback (callable): Function to call when event fires.
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        """Remove a callback from an event type."""
        if event_type in self._listeners:
            self._listeners[event_type] = [
                cb for cb in self._listeners[event_type] if cb != callback
            ]

    def emit(self, event_type, data=None):
        """
        Emit an event, calling all subscribed callbacks.

        Parameters:
            event_type (str): Name of the event.
            data: Data payload to pass to callbacks.
        """
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(event_type, data)


class LoggerObserver:
    """An observer that logs events to the console."""

    def __init__(self, name="Logger"):
        self.name = name

    def on_event(self, event_type, data):
        print(f"  [{self.name}] received '{event_type}': {data}")


class DashboardObserver:
    """An observer that updates a dashboard (simulated)."""

    def __init__(self):
        self.event_count = 0

    def on_event(self, event_type, data):
        self.event_count += 1
        print(f"  [Dashboard] received '{event_type}': {data} (total events: {self.event_count})")


# ============================================================
# PATTERN 3: Factory
# ============================================================

class Vehicle(ABC):
    """Abstract base class for vehicles."""

    @abstractmethod
    def describe(self):
        pass

    def __repr__(self):
        return self.describe()


class Car(Vehicle):
    def __init__(self, engine="V4", doors=4, fuel="gasoline"):
        self.engine = engine
        self.doors = doors
        self.fuel = fuel

    def describe(self):
        return f"Car(engine={self.engine}, doors={self.doors}, fuel={self.fuel})"


class Motorcycle(Vehicle):
    def __init__(self, engine="V2", fuel="gasoline"):
        self.engine = engine
        self.doors = 0
        self.fuel = fuel

    def describe(self):
        return f"Motorcycle(engine={self.engine}, doors={self.doors}, fuel={self.fuel})"


class Truck(Vehicle):
    def __init__(self, engine="V8", payload_tons=5, fuel="diesel"):
        self.engine = engine
        self.payload_tons = payload_tons
        self.fuel = fuel
        self.doors = 2

    def describe(self):
        return f"Truck(engine={self.engine}, payload={self.payload_tons}t, fuel={self.fuel})"


class ElectricCar(Vehicle):
    def __init__(self, battery_kwh=75, range_km=400):
        self.battery_kwh = battery_kwh
        self.range_km = range_km
        self.fuel = "electric"
        self.doors = 4

    def describe(self):
        return f"ElectricCar(battery={self.battery_kwh}kWh, range={self.range_km}km)"


class VehicleFactory:
    """
    Factory that creates Vehicle instances based on a type string.
    New vehicle types can be registered dynamically.
    """

    _registry = {}

    @classmethod
    def register(cls, vehicle_type, vehicle_class):
        """Register a new vehicle type."""
        cls._registry[vehicle_type.lower()] = vehicle_class

    @classmethod
    def create(cls, vehicle_type, **kwargs):
        """
        Create a vehicle by type name.

        Parameters:
            vehicle_type (str): Registered vehicle type (e.g., 'car', 'truck').
            **kwargs: Arguments passed to the vehicle constructor.

        Returns:
            Vehicle: A new vehicle instance.

        Raises:
            ValueError: If vehicle_type is not registered.
        """
        vehicle_type = vehicle_type.lower()
        if vehicle_type not in cls._registry:
            available = ", ".join(cls._registry.keys())
            raise ValueError(
                f"Unknown vehicle type '{vehicle_type}'. Available: {available}"
            )
        return cls._registry[vehicle_type](**kwargs)

    @classmethod
    def available_types(cls):
        """Return a list of registered vehicle types."""
        return list(cls._registry.keys())


# Register default vehicle types
VehicleFactory.register("car", Car)
VehicleFactory.register("motorcycle", Motorcycle)
VehicleFactory.register("truck", Truck)
VehicleFactory.register("electric_car", ElectricCar)


# ============================================================
# Demo
# ============================================================

if __name__ == "__main__":

    # ---- Singleton Demo ----
    print("=" * 50)
    print("  SINGLETON PATTERN")
    print("=" * 50)

    config1 = AppConfig()
    config2 = AppConfig()

    print(f"config1: {config1}")
    print(f"config1 is config2? {config1 is config2}")
    print(f"id(config1) == id(config2)? {id(config1) == id(config2)}")

    config1.set("debug", True)
    print(f"After config1.set('debug', True):")
    print(f"  config2.get('debug') = {config2.get('debug')}  (same object!)")
    print()

    # ---- Observer Demo ----
    print("=" * 50)
    print("  OBSERVER PATTERN")
    print("=" * 50)

    events = EventSystem()
    logger = LoggerObserver("AppLogger")
    dashboard = DashboardObserver()

    # Subscribe
    events.subscribe("user_login", logger.on_event)
    events.subscribe("user_login", dashboard.on_event)
    events.subscribe("user_logout", logger.on_event)
    events.subscribe("purchase", logger.on_event)
    events.subscribe("purchase", dashboard.on_event)

    # Emit events
    print("\nEmitting 'user_login':")
    events.emit("user_login", {"user": "alice"})

    print("\nEmitting 'purchase':")
    events.emit("purchase", {"item": "Python Book", "price": 29.99})

    print("\nEmitting 'user_logout':")
    events.emit("user_logout", {"user": "alice"})

    # Unsubscribe dashboard from user_login
    events.unsubscribe("user_login", dashboard.on_event)
    print("\nAfter unsubscribing Dashboard from 'user_login':")
    print("Emitting 'user_login':")
    events.emit("user_login", {"user": "bob"})
    print()

    # ---- Factory Demo ----
    print("=" * 50)
    print("  FACTORY PATTERN")
    print("=" * 50)

    print(f"\nAvailable vehicle types: {VehicleFactory.available_types()}")
    print()

    # Create vehicles
    car = VehicleFactory.create("car", engine="V6", doors=4)
    print(f"Created: {car}")

    moto = VehicleFactory.create("motorcycle", engine="V2")
    print(f"Created: {moto}")

    truck = VehicleFactory.create("truck", engine="V8", payload_tons=10)
    print(f"Created: {truck}")

    ev = VehicleFactory.create("electric_car", battery_kwh=100, range_km=500)
    print(f"Created: {ev}")

    # Unknown type
    print()
    try:
        VehicleFactory.create("helicopter")
    except ValueError as e:
        print(f"Error: {e}")

    # Dynamic registration
    print("\n--- Dynamic Registration ---")

    class Bicycle(Vehicle):
        def __init__(self, gears=21):
            self.gears = gears
            self.fuel = "human power"

        def describe(self):
            return f"Bicycle(gears={self.gears}, fuel={self.fuel})"

    VehicleFactory.register("bicycle", Bicycle)
    bike = VehicleFactory.create("bicycle", gears=18)
    print(f"Created: {bike}")
    print(f"Updated types: {VehicleFactory.available_types()}")
