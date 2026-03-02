"""
Custom List (Dunder Methods)
==============================
Difficulty: 3/5
Estimated time: 25 minutes

Problem:
--------
Create a CustomList class that behaves like a Python list by implementing
key dunder (magic) methods:
1. __init__      - Initialize from optional iterable.
2. __repr__      - Developer-friendly string.
3. __str__       - User-friendly string.
4. __len__       - Length.
5. __getitem__   - Index and slice access.
6. __setitem__   - Index and slice assignment.
7. __delitem__   - Delete by index.
8. __contains__  - `in` operator.
9. __iter__      - Iteration (for loop).
10. __add__      - Concatenation with +.
11. __eq__       - Equality comparison.
12. append, extend, insert, pop, reverse, sort methods.

Concepts practiced:
- Dunder/magic methods
- Making objects behave like built-in types
- Slicing support
- Iterator protocol

Expected output (example):
--------------------------
# lst = CustomList([1, 2, 3, 4, 5])
# len(lst) = 5
# lst[0]   = 1
# lst[-1]  = 5
# lst[1:3] = CustomList([2, 3])
#
# 3 in lst? True
# for x in lst: 1 2 3 4 5
#
# lst + CustomList([6, 7]) = CustomList([1, 2, 3, 4, 5, 6, 7])
"""


class CustomList:
    """A custom list implementation demonstrating Python dunder methods."""

    def __init__(self, iterable=None):
        """
        Initialize the custom list.

        Parameters:
            iterable: Optional iterable to populate the list from.
        """
        if iterable is None:
            self._data = []
        else:
            self._data = list(iterable)

    # ---- Representation ----

    def __repr__(self):
        return f"CustomList({self._data!r})"

    def __str__(self):
        return f"[{', '.join(str(x) for x in self._data)}]"

    # ---- Length ----

    def __len__(self):
        return len(self._data)

    # ---- Item access ----

    def __getitem__(self, index):
        """Support indexing and slicing."""
        if isinstance(index, slice):
            return CustomList(self._data[index])
        return self._data[index]

    def __setitem__(self, index, value):
        """Support index and slice assignment."""
        if isinstance(index, slice):
            self._data[index] = value
        else:
            self._data[index] = value

    def __delitem__(self, index):
        """Delete an item by index."""
        del self._data[index]

    # ---- Membership ----

    def __contains__(self, item):
        """Support the 'in' operator."""
        return item in self._data

    # ---- Iteration ----

    def __iter__(self):
        """Return an iterator over the items."""
        return iter(self._data)

    # ---- Arithmetic / Concatenation ----

    def __add__(self, other):
        """Concatenate two CustomLists using +."""
        if isinstance(other, CustomList):
            return CustomList(self._data + other._data)
        if isinstance(other, list):
            return CustomList(self._data + other)
        return NotImplemented

    def __iadd__(self, other):
        """Support += operator."""
        if isinstance(other, (CustomList, list)):
            items = other._data if isinstance(other, CustomList) else other
            self._data.extend(items)
            return self
        return NotImplemented

    def __mul__(self, times):
        """Support * operator for repetition."""
        if isinstance(times, int):
            return CustomList(self._data * times)
        return NotImplemented

    # ---- Comparison ----

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return self._data == other._data
        if isinstance(other, list):
            return self._data == other
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    # ---- Boolean ----

    def __bool__(self):
        """Empty list is falsy."""
        return len(self._data) > 0

    # ---- List methods ----

    def append(self, item):
        """Append an item to the end."""
        self._data.append(item)

    def extend(self, iterable):
        """Extend the list by appending items from the iterable."""
        self._data.extend(iterable)

    def insert(self, index, item):
        """Insert an item at a given position."""
        self._data.insert(index, item)

    def pop(self, index=-1):
        """Remove and return item at index (default: last)."""
        return self._data.pop(index)

    def remove(self, item):
        """Remove the first occurrence of item."""
        self._data.remove(item)

    def reverse(self):
        """Reverse the list in place."""
        self._data.reverse()

    def sort(self, key=None, reverse=False):
        """Sort the list in place."""
        self._data.sort(key=key, reverse=reverse)

    def index(self, item):
        """Return the index of the first occurrence of item."""
        return self._data.index(item)

    def count(self, item):
        """Return the number of occurrences of item."""
        return self._data.count(item)

    def copy(self):
        """Return a shallow copy."""
        return CustomList(self._data.copy())

    def clear(self):
        """Remove all items."""
        self._data.clear()


if __name__ == "__main__":
    print("--- Custom List Demo ---\n")

    # Creation
    lst = CustomList([1, 2, 3, 4, 5])
    print(f"Created:  {lst!r}")
    print(f"str():    {lst}")
    print(f"len():    {len(lst)}")
    print()

    # Indexing
    print("--- Indexing ---")
    print(f"lst[0]   = {lst[0]}")
    print(f"lst[-1]  = {lst[-1]}")
    print(f"lst[1:3] = {lst[1:3]!r}")
    print(f"lst[::2] = {lst[::2]!r}")
    print()

    # Assignment
    print("--- Assignment ---")
    lst[0] = 10
    print(f"lst[0] = 10  -> {lst}")
    lst[0] = 1  # restore
    print()

    # Membership
    print("--- Membership ---")
    print(f"3 in lst? {3 in lst}")
    print(f"9 in lst? {9 in lst}")
    print()

    # Iteration
    print("--- Iteration ---")
    print("for x in lst:", end=" ")
    for x in lst:
        print(x, end=" ")
    print("\n")

    # Concatenation
    print("--- Concatenation ---")
    lst2 = CustomList([6, 7, 8])
    combined = lst + lst2
    print(f"{lst!r} + {lst2!r} = {combined!r}")
    print()

    # Repetition
    print("--- Repetition ---")
    small = CustomList([0])
    print(f"{small!r} * 3 = {(small * 3)!r}")
    print()

    # In-place add
    print("--- In-place Add (+=) ---")
    lst3 = CustomList([1, 2])
    lst3 += CustomList([3, 4])
    print(f"After +=: {lst3!r}")
    print()

    # Comparison
    print("--- Comparison ---")
    a = CustomList([1, 2, 3])
    b = CustomList([1, 2, 3])
    c = CustomList([1, 2, 4])
    print(f"{a!r} == {b!r}? {a == b}")
    print(f"{a!r} == {c!r}? {a == c}")
    print(f"{a!r} == [1, 2, 3]? {a == [1, 2, 3]}")
    print()

    # Methods
    print("--- Methods ---")
    m = CustomList([3, 1, 4, 1, 5, 9])
    print(f"Original: {m}")

    m.append(2)
    print(f"append(2): {m}")

    m.insert(0, 0)
    print(f"insert(0, 0): {m}")

    popped = m.pop()
    print(f"pop(): returned {popped}, list = {m}")

    m.sort()
    print(f"sort(): {m}")

    m.reverse()
    print(f"reverse(): {m}")

    print(f"count(1): {m.count(1)}")
    print(f"index(5): {m.index(5)}")
    print()

    # Boolean
    print("--- Boolean ---")
    print(f"bool(CustomList([1])): {bool(CustomList([1]))}")
    print(f"bool(CustomList()):    {bool(CustomList())}")
    print()

    # Delete
    print("--- Delete ---")
    d = CustomList([10, 20, 30, 40])
    del d[1]
    print(f"del d[1]: {d}")
