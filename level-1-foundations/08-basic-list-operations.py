"""
Exercise 08 - Basic List Operations
=====================================
Level: 1 - Foundations
Difficulty: 2/5
Estimated Time: 15 minutes

Problem:
--------
Implement common list operations without using built-in shortcuts
(then show the Pythonic way too):
  1. Sort a list (manual + sorted())
  2. Filter elements based on a condition
  3. Find maximum and minimum values
  4. Calculate sum and average
  5. Remove duplicates while preserving order

Expected Input/Output:
----------------------
# manual_sort([3, 1, 4, 1, 5])        -> [1, 1, 3, 4, 5]
# filter_evens([1, 2, 3, 4, 5, 6])    -> [2, 4, 6]
# find_max([3, 1, 4, 1, 5, 9])        -> 9
# find_min([3, 1, 4, 1, 5, 9])        -> 1
# list_sum([1, 2, 3, 4, 5])           -> 15
# list_average([1, 2, 3, 4, 5])       -> 3.0
# remove_duplicates([1, 2, 2, 3, 3])  -> [1, 2, 3]
"""


def manual_sort(lst: list) -> list:
    """
    Sort a list using bubble sort (manual implementation).

    Args:
        lst: A list of comparable elements.

    Returns:
        A new sorted list in ascending order.
    """
    result = lst.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


def filter_evens(lst: list) -> list:
    """Return only even numbers from the list."""
    return [x for x in lst if x % 2 == 0]


def filter_odds(lst: list) -> list:
    """Return only odd numbers from the list."""
    return [x for x in lst if x % 2 != 0]


def filter_by_condition(lst: list, condition) -> list:
    """
    Filter a list using a custom condition function.

    Args:
        lst: The input list.
        condition: A function that returns True/False for each element.

    Returns:
        A filtered list containing only elements where condition is True.
    """
    return [x for x in lst if condition(x)]


def find_max(lst: list) -> int:
    """
    Find the maximum value in a list (manual implementation).

    Args:
        lst: A non-empty list of numbers.

    Returns:
        The maximum value.

    Raises:
        ValueError: If the list is empty.
    """
    if not lst:
        raise ValueError("Cannot find max of an empty list")
    maximum = lst[0]
    for item in lst[1:]:
        if item > maximum:
            maximum = item
    return maximum


def find_min(lst: list) -> int:
    """
    Find the minimum value in a list (manual implementation).

    Args:
        lst: A non-empty list of numbers.

    Returns:
        The minimum value.

    Raises:
        ValueError: If the list is empty.
    """
    if not lst:
        raise ValueError("Cannot find min of an empty list")
    minimum = lst[0]
    for item in lst[1:]:
        if item < minimum:
            minimum = item
    return minimum


def list_sum(lst: list) -> float:
    """
    Calculate the sum of all elements (manual implementation).

    Args:
        lst: A list of numbers.

    Returns:
        The sum of all elements.
    """
    total = 0
    for item in lst:
        total += item
    return total


def list_average(lst: list) -> float:
    """
    Calculate the average of all elements.

    Args:
        lst: A non-empty list of numbers.

    Returns:
        The average as a float.

    Raises:
        ValueError: If the list is empty.
    """
    if not lst:
        raise ValueError("Cannot calculate average of an empty list")
    return list_sum(lst) / len(lst)


def remove_duplicates(lst: list) -> list:
    """
    Remove duplicates while preserving original order.

    Args:
        lst: A list that may contain duplicate elements.

    Returns:
        A new list with duplicates removed, preserving first occurrence order.
    """
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def flatten_list(nested: list) -> list:
    """
    Flatten a nested list into a single-level list.

    Args:
        nested: A list that may contain sublists.

    Returns:
        A flat list with all elements.
    """
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat


def chunk_list(lst: list, size: int) -> list:
    """
    Split a list into chunks of a given size.

    Args:
        lst: The input list.
        size: The chunk size.

    Returns:
        A list of sublists, each of length up to 'size'.
    """
    return [lst[i:i + size] for i in range(0, len(lst), size)]


if __name__ == "__main__":
    print("=" * 50)
    print("  Basic List Operations Demo")
    print("=" * 50)

    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    # Sorting
    print("\n--- Sorting ---")
    print(f"  Original:     {numbers}")
    print(f"  Manual sort:  {manual_sort(numbers)}")
    print(f"  Built-in:     {sorted(numbers)}")

    # Filtering
    print("\n--- Filtering ---")
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"  Numbers:    {nums}")
    print(f"  Evens:      {filter_evens(nums)}")
    print(f"  Odds:       {filter_odds(nums)}")
    print(f"  Greater >5: {filter_by_condition(nums, lambda x: x > 5)}")

    # Max and Min
    print("\n--- Max & Min ---")
    print(f"  List: {numbers}")
    print(f"  Max (manual): {find_max(numbers)}")
    print(f"  Min (manual): {find_min(numbers)}")
    print(f"  Max (built-in): {max(numbers)}")
    print(f"  Min (built-in): {min(numbers)}")

    # Sum and Average
    print("\n--- Sum & Average ---")
    simple = [1, 2, 3, 4, 5]
    print(f"  List: {simple}")
    print(f"  Sum (manual):     {list_sum(simple)}")
    print(f"  Sum (built-in):   {sum(simple)}")
    print(f"  Average:          {list_average(simple)}")

    # Remove duplicates
    print("\n--- Remove Duplicates ---")
    with_dupes = [1, 2, 2, 3, 4, 4, 4, 5, 1, 3]
    print(f"  Original:        {with_dupes}")
    print(f"  No duplicates:   {remove_duplicates(with_dupes)}")

    # Flatten nested list
    print("\n--- Flatten Nested List ---")
    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    print(f"  Nested:    {nested}")
    print(f"  Flattened: {flatten_list(nested)}")

    # Chunk list
    print("\n--- Chunk List ---")
    items = list(range(1, 11))
    print(f"  Original:     {items}")
    print(f"  Chunks of 3:  {chunk_list(items, 3)}")
    print(f"  Chunks of 4:  {chunk_list(items, 4)}")

    # Error handling
    print("\n--- Error Handling ---")
    try:
        find_max([])
    except ValueError as e:
        print(f"  find_max([]) -> Error: {e}")

    try:
        list_average([])
    except ValueError as e:
        print(f"  list_average([]) -> Error: {e}")

    print("\nBasic list operations exercise complete!")
