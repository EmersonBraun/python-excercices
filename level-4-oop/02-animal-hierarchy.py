"""
Animal Hierarchy with Polymorphism
====================================
Difficulty: 2/5
Estimated time: 15 minutes

Problem:
--------
Create an animal class hierarchy demonstrating polymorphism:
1. Animal (base class) with name, species, age, and methods: speak(), eat(), info().
2. Dog - speaks "Woof!", eats "kibble", can fetch().
3. Cat - speaks "Meow!", eats "fish", can purr().
4. Bird - speaks "Tweet!", eats "seeds", can fly().
5. A function that takes any Animal and calls its methods polymorphically.

Concepts practiced:
- Inheritance
- Method overriding (polymorphism)
- super().__init__()
- isinstance() checks
- Polymorphic function calls

Expected output (example):
--------------------------
# === Animal Info ===
# Name: Rex, Species: Dog, Age: 3
# Rex says: Woof! Woof!
# Rex eats kibble
# Rex fetches the ball!
#
# Name: Whiskers, Species: Cat, Age: 5
# Whiskers says: Meow!
# Whiskers eats fish
# Whiskers purrs contentedly...
#
# Name: Tweety, Species: Bird, Age: 1
# Tweety says: Tweet! Tweet!
# Tweety eats seeds
# Tweety flies high in the sky!
"""


class Animal:
    """Base class for all animals."""

    def __init__(self, name, species, age):
        """
        Initialize an animal.

        Parameters:
            name (str): The animal's name.
            species (str): The species.
            age (int): Age in years.
        """
        self.name = name
        self.species = species
        self.age = age

    def speak(self):
        """Make the animal's sound. Override in subclasses."""
        return f"{self.name} makes a sound."

    def eat(self):
        """Describe what the animal eats. Override in subclasses."""
        return f"{self.name} eats food."

    def info(self):
        """Return a string with the animal's information."""
        return f"Name: {self.name}, Species: {self.species}, Age: {self.age}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, age={self.age})"

    def __str__(self):
        return f"{self.name} the {self.species}"


class Dog(Animal):
    """A dog that barks and fetches."""

    def __init__(self, name, age, breed="Mixed"):
        super().__init__(name, species="Dog", age=age)
        self.breed = breed
        self.tricks = []

    def speak(self):
        return f"{self.name} says: Woof! Woof!"

    def eat(self):
        return f"{self.name} eats kibble."

    def fetch(self, item="ball"):
        """Fetch an item."""
        return f"{self.name} fetches the {item}!"

    def learn_trick(self, trick):
        """Teach the dog a new trick."""
        self.tricks.append(trick)
        return f"{self.name} learned '{trick}'!"

    def show_tricks(self):
        """List all known tricks."""
        if not self.tricks:
            return f"{self.name} doesn't know any tricks yet."
        return f"{self.name}'s tricks: {', '.join(self.tricks)}"

    def info(self):
        base = super().info()
        return f"{base}, Breed: {self.breed}"


class Cat(Animal):
    """A cat that meows and purrs."""

    def __init__(self, name, age, indoor=True):
        super().__init__(name, species="Cat", age=age)
        self.indoor = indoor

    def speak(self):
        return f"{self.name} says: Meow!"

    def eat(self):
        return f"{self.name} eats fish."

    def purr(self):
        """The cat purrs."""
        return f"{self.name} purrs contentedly..."

    def info(self):
        base = super().info()
        status = "Indoor" if self.indoor else "Outdoor"
        return f"{base}, {status}"


class Bird(Animal):
    """A bird that tweets and flies."""

    def __init__(self, name, age, can_fly=True):
        super().__init__(name, species="Bird", age=age)
        self._can_fly = can_fly

    def speak(self):
        return f"{self.name} says: Tweet! Tweet!"

    def eat(self):
        return f"{self.name} eats seeds."

    def fly(self):
        """Attempt to fly."""
        if self._can_fly:
            return f"{self.name} flies high in the sky!"
        return f"{self.name} flaps but cannot fly."

    def info(self):
        base = super().info()
        flight = "Can fly" if self._can_fly else "Flightless"
        return f"{base}, {flight}"


def interact_with_animal(animal):
    """
    Demonstrate polymorphism: call the same methods on any animal.

    Parameters:
        animal (Animal): Any animal instance.
    """
    print(f"=== {animal} ===")
    print(f"  {animal.info()}")
    print(f"  {animal.speak()}")
    print(f"  {animal.eat()}")

    # Call species-specific abilities
    if isinstance(animal, Dog):
        print(f"  {animal.fetch()}")
    elif isinstance(animal, Cat):
        print(f"  {animal.purr()}")
    elif isinstance(animal, Bird):
        print(f"  {animal.fly()}")

    print()


def animal_roll_call(animals):
    """Print a roll call of all animals."""
    print("--- Roll Call ---")
    for a in animals:
        print(f"  {a!r}")
    print()


if __name__ == "__main__":
    print("--- Animal Hierarchy Demo ---\n")

    # Create animals
    rex = Dog("Rex", 3, breed="German Shepherd")
    whiskers = Cat("Whiskers", 5, indoor=True)
    tweety = Bird("Tweety", 1)
    penguin = Bird("Penny", 4, can_fly=False)

    animals = [rex, whiskers, tweety, penguin]

    # Roll call
    animal_roll_call(animals)

    # Polymorphic interaction
    for animal in animals:
        interact_with_animal(animal)

    # Dog tricks
    print("--- Dog Tricks ---")
    print(rex.learn_trick("sit"))
    print(rex.learn_trick("shake"))
    print(rex.learn_trick("roll over"))
    print(rex.show_tricks())
    print()

    # Demonstrate isinstance
    print("--- Type Checking ---")
    for animal in animals:
        print(
            f"  {animal.name:10s} -> "
            f"Animal: {isinstance(animal, Animal)}, "
            f"Dog: {isinstance(animal, Dog)}, "
            f"Cat: {isinstance(animal, Cat)}, "
            f"Bird: {isinstance(animal, Bird)}"
        )

    # Sorting animals by age
    print(f"\n--- Sorted by Age ---")
    for a in sorted(animals, key=lambda x: x.age):
        print(f"  {a.name} (age {a.age})")
