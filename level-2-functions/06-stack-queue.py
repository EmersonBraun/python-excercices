"""
Exercise 06 - Stack and Queue
===============================
Level: 2 - Functions & Collections
Difficulty: 2/5
Estimated Time: 15 minutes

Problem:
--------
Implement Stack and Queue data structures using Python lists.

Stack (LIFO - Last In, First Out):
  - push(item): Add item to top
  - pop(): Remove and return top item
  - peek(): View top item without removing
  - is_empty(): Check if stack is empty

Queue (FIFO - First In, First Out):
  - enqueue(item): Add item to back
  - dequeue(): Remove and return front item
  - peek(): View front item without removing
  - is_empty(): Check if queue is empty

Expected Input/Output:
----------------------
# Stack:
# s = Stack()
# s.push(1); s.push(2); s.push(3)
# s.pop()   -> 3
# s.peek()  -> 2
# s.size()  -> 2

# Queue:
# q = Queue()
# q.enqueue(1); q.enqueue(2); q.enqueue(3)
# q.dequeue() -> 1
# q.peek()    -> 2
# q.size()    -> 2
"""


class Stack:
    """
    Stack data structure (LIFO - Last In, First Out).
    Implemented using a Python list.
    """

    def __init__(self):
        """Initialize an empty stack."""
        self._items = []

    def push(self, item) -> None:
        """
        Push an item onto the top of the stack.

        Args:
            item: The item to push.
        """
        self._items.append(item)

    def pop(self):
        """
        Remove and return the top item from the stack.

        Returns:
            The top item.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """
        View the top item without removing it.

        Returns:
            The top item.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self._items)

    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items.clear()

    def __repr__(self) -> str:
        return f"Stack({self._items})"

    def __len__(self) -> int:
        return self.size()

    def __contains__(self, item) -> bool:
        return item in self._items


class Queue:
    """
    Queue data structure (FIFO - First In, First Out).
    Implemented using a Python list.
    """

    def __init__(self):
        """Initialize an empty queue."""
        self._items = []

    def enqueue(self, item) -> None:
        """
        Add an item to the back of the queue.

        Args:
            item: The item to enqueue.
        """
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the front item from the queue.

        Returns:
            The front item.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.pop(0)

    def peek(self):
        """
        View the front item without removing it.

        Returns:
            The front item.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek an empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self._items)

    def clear(self) -> None:
        """Remove all items from the queue."""
        self._items.clear()

    def __repr__(self) -> str:
        return f"Queue({self._items})"

    def __len__(self) -> int:
        return self.size()

    def __contains__(self, item) -> bool:
        return item in self._items


# --- Practical applications ---

def is_balanced_parentheses(expression: str) -> bool:
    """
    Check if parentheses/brackets/braces in an expression are balanced.
    Uses a Stack.

    Args:
        expression: A string potentially containing ()[]{}

    Returns:
        True if all brackets are properly matched and nested.
    """
    stack = Stack()
    matching = {")": "(", "]": "[", "}": "{"}
    opening = set(matching.values())

    for char in expression:
        if char in opening:
            stack.push(char)
        elif char in matching:
            if stack.is_empty() or stack.pop() != matching[char]:
                return False

    return stack.is_empty()


def reverse_string_with_stack(s: str) -> str:
    """
    Reverse a string using a Stack.

    Args:
        s: The string to reverse.

    Returns:
        The reversed string.
    """
    stack = Stack()
    for char in s:
        stack.push(char)

    reversed_chars = []
    while not stack.is_empty():
        reversed_chars.append(stack.pop())

    return "".join(reversed_chars)


def hot_potato(names: list, num: int) -> str:
    """
    Simulate the Hot Potato game using a Queue.

    Players stand in a circle and pass a 'potato'. After 'num' passes,
    the person holding it is eliminated. Last person standing wins.

    Args:
        names: List of player names.
        num: Number of passes before elimination.

    Returns:
        The name of the winner.
    """
    queue = Queue()
    for name in names:
        queue.enqueue(name)

    while queue.size() > 1:
        for _ in range(num):
            # Pass the potato: move front person to back
            queue.enqueue(queue.dequeue())
        # Eliminate the person holding the potato
        eliminated = queue.dequeue()

    return queue.dequeue()


if __name__ == "__main__":
    print("=" * 50)
    print("  Stack & Queue Demo")
    print("=" * 50)

    # --- Stack Demo ---
    print("\n--- Stack (LIFO) ---")
    stack = Stack()

    print("  Pushing: 10, 20, 30, 40")
    for val in [10, 20, 30, 40]:
        stack.push(val)
    print(f"  Stack: {stack}")
    print(f"  Size: {stack.size()}")
    print(f"  Peek: {stack.peek()}")

    print(f"  Pop: {stack.pop()}")
    print(f"  Pop: {stack.pop()}")
    print(f"  Stack after 2 pops: {stack}")
    print(f"  Contains 10? {10 in stack}")
    print(f"  Contains 30? {30 in stack}")

    # --- Queue Demo ---
    print("\n--- Queue (FIFO) ---")
    queue = Queue()

    print("  Enqueuing: A, B, C, D")
    for val in ["A", "B", "C", "D"]:
        queue.enqueue(val)
    print(f"  Queue: {queue}")
    print(f"  Size: {queue.size()}")
    print(f"  Peek: {queue.peek()}")

    print(f"  Dequeue: {queue.dequeue()}")
    print(f"  Dequeue: {queue.dequeue()}")
    print(f"  Queue after 2 dequeues: {queue}")

    # --- Balanced Parentheses ---
    print("\n--- Balanced Parentheses (Stack Application) ---")
    test_expressions = [
        ("(())", True),
        ("{[()]}", True),
        ("((())", False),
        ("{[(])}", False),
        ("", True),
        ("({[]})", True),
        (")(", False),
    ]
    for expr, expected in test_expressions:
        result = is_balanced_parentheses(expr)
        status = "PASS" if result == expected else "FAIL"
        display = f"'{expr}'" if expr else "''"
        print(f"  [{status}] {display:>12} -> {result}")

    # --- Reverse String with Stack ---
    print("\n--- Reverse String (Stack Application) ---")
    test_strings = ["hello", "Python", "12345"]
    for s in test_strings:
        reversed_s = reverse_string_with_stack(s)
        print(f"  '{s}' -> '{reversed_s}'")

    # --- Hot Potato Game ---
    print("\n--- Hot Potato Game (Queue Application) ---")
    players = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    winner = hot_potato(players, 7)
    print(f"  Players: {players}")
    print(f"  Passes per round: 7")
    print(f"  Winner: {winner}")

    # --- Error Handling ---
    print("\n--- Error Handling ---")
    empty_stack = Stack()
    try:
        empty_stack.pop()
    except IndexError as e:
        print(f"  Pop empty stack: {e}")

    empty_queue = Queue()
    try:
        empty_queue.dequeue()
    except IndexError as e:
        print(f"  Dequeue empty queue: {e}")

    print("\nStack & Queue exercise complete!")
