"""
Level 5 - Exercise 07: Coroutine-Based Data Processing Pipeline
================================================================

Difficulty: 4/5 stars
Estimated time: 25 minutes

Build a data-processing pipeline using Python coroutines (generator-
based send/yield pattern) and an asyncio-based variant.

The pipeline follows the pattern:
    producer  ->  filter  ->  transform  ->  consumer

Exercises
---------
1. coroutine helper   - Decorator to auto-prime a coroutine.
2. consumer           - Coroutine that collects / prints results.
3. filter_stage       - Coroutine that forwards items matching a predicate.
4. transform_stage    - Coroutine that applies a function before forwarding.
5. producer           - Pushes items through the pipeline.
6. async pipeline     - Same concept using asyncio.Queue.

Expected output (approximate):
------------------------------
# Pipeline: numbers 1..20 -> keep evens -> square them -> collect
# Results: [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]
"""

import asyncio
import functools


# ---------------------------------------------------------------------------
# 1. Coroutine Primer Decorator
# ---------------------------------------------------------------------------
def coroutine(func):
    """Decorator that auto-advances a generator coroutine to its first yield.

    Without this, you would need to call next(gen) before the first .send().

    >>> @coroutine
    ... def printer():
    ...     while True:
    ...         item = yield
    ...         print(item)
    >>> p = printer()      # already primed -- ready for .send()
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # prime / advance to first yield
        return gen
    return wrapper


# ---------------------------------------------------------------------------
# 2. Consumer (end of pipeline)
# ---------------------------------------------------------------------------
@coroutine
def consumer(results: list):
    """Coroutine that appends every received item to *results*.

    This is the terminal stage of the pipeline.

    Usage:
        collected = []
        sink = consumer(collected)
        sink.send(42)
        # collected == [42]
    """
    try:
        while True:
            item = yield
            results.append(item)
    except GeneratorExit:
        pass


@coroutine
def printer(prefix=""):
    """Coroutine that prints every received item (useful for debugging)."""
    try:
        while True:
            item = yield
            print(f"{prefix}{item}")
    except GeneratorExit:
        pass


# ---------------------------------------------------------------------------
# 3. Filter Stage
# ---------------------------------------------------------------------------
@coroutine
def filter_stage(predicate, target):
    """Coroutine that forwards items to *target* only if predicate(item) is True.

    Usage:
        sink = consumer(results)
        even_filter = filter_stage(lambda x: x % 2 == 0, sink)
        even_filter.send(3)  # dropped
        even_filter.send(4)  # forwarded
    """
    try:
        while True:
            item = yield
            if predicate(item):
                target.send(item)
    except GeneratorExit:
        target.close()


# ---------------------------------------------------------------------------
# 4. Transform Stage
# ---------------------------------------------------------------------------
@coroutine
def transform_stage(func, target):
    """Coroutine that applies *func* to each item and forwards the result.

    Usage:
        sink = consumer(results)
        doubler = transform_stage(lambda x: x * 2, sink)
        doubler.send(5)  # forwards 10
    """
    try:
        while True:
            item = yield
            target.send(func(item))
    except GeneratorExit:
        target.close()


# ---------------------------------------------------------------------------
# 5. Producer (beginning of pipeline)
# ---------------------------------------------------------------------------
def producer(iterable, pipeline):
    """Push every item from *iterable* into the coroutine *pipeline*.

    Closes the pipeline when done.

    Usage:
        producer(range(10), my_pipeline)
    """
    for item in iterable:
        pipeline.send(item)
    pipeline.close()


# ---------------------------------------------------------------------------
# 6. Broadcast (fan-out to multiple targets)
# ---------------------------------------------------------------------------
@coroutine
def broadcast(*targets):
    """Coroutine that sends each item to ALL targets.

    Usage:
        b = broadcast(pipeline_a, pipeline_b)
        b.send(42)  # both pipelines receive 42
    """
    try:
        while True:
            item = yield
            for target in targets:
                target.send(item)
    except GeneratorExit:
        for target in targets:
            target.close()


# ---------------------------------------------------------------------------
# 7. Async Pipeline Variant (asyncio.Queue based)
# ---------------------------------------------------------------------------
async def async_producer(queue: asyncio.Queue, iterable):
    """Push items into an asyncio.Queue."""
    for item in iterable:
        await queue.put(item)
    await queue.put(None)  # sentinel


async def async_filter(in_q: asyncio.Queue, out_q: asyncio.Queue, predicate):
    """Read from in_q, forward to out_q if predicate passes."""
    while True:
        item = await in_q.get()
        if item is None:
            await out_q.put(None)
            break
        if predicate(item):
            await out_q.put(item)


async def async_transform(in_q: asyncio.Queue, out_q: asyncio.Queue, func):
    """Read from in_q, apply func, put result in out_q."""
    while True:
        item = await in_q.get()
        if item is None:
            await out_q.put(None)
            break
        await out_q.put(func(item))


async def async_consumer(queue: asyncio.Queue, results: list):
    """Read from queue until sentinel, collecting into results."""
    while True:
        item = await queue.get()
        if item is None:
            break
        results.append(item)


async def run_async_pipeline(data, predicate, transform_func):
    """Wire up the full async pipeline and return collected results."""
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    q3 = asyncio.Queue()
    results = []

    await asyncio.gather(
        async_producer(q1, data),
        async_filter(q1, q2, predicate),
        async_transform(q2, q3, transform_func),
        async_consumer(q3, results),
    )
    return results


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Generator-based pipeline
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Generator-Based Coroutine Pipeline")
    print("=" * 60)

    # Pipeline: numbers 1..20 -> keep evens -> square -> collect
    results = []
    pipeline = filter_stage(
        lambda x: x % 2 == 0,
        transform_stage(
            lambda x: x ** 2,
            consumer(results),
        ),
    )
    producer(range(1, 21), pipeline)
    print(f"Evens squared (1..20): {results}")
    # Expected: [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

    # Pipeline: strings -> keep len > 3 -> uppercase -> collect
    results2 = []
    pipeline2 = filter_stage(
        lambda s: len(s) > 3,
        transform_stage(
            str.upper,
            consumer(results2),
        ),
    )
    words = ["hi", "hello", "hey", "world", "ok", "python", "go"]
    producer(words, pipeline2)
    print(f"Long words uppercased: {results2}")
    # Expected: ['HELLO', 'WORLD', 'PYTHON']

    print()

    # ------------------------------------------------------------------
    # Broadcast (fan-out) demo
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Broadcast (Fan-Out) Pipeline")
    print("=" * 60)

    evens = []
    odds = []
    fan = broadcast(
        filter_stage(lambda x: x % 2 == 0, consumer(evens)),
        filter_stage(lambda x: x % 2 != 0, consumer(odds)),
    )
    producer(range(1, 11), fan)
    print(f"Evens: {evens}")
    print(f"Odds:  {odds}")
    print()

    # ------------------------------------------------------------------
    # Async pipeline
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Async Pipeline (asyncio.Queue)")
    print("=" * 60)

    async_results = asyncio.run(
        run_async_pipeline(
            data=range(1, 21),
            predicate=lambda x: x % 2 == 0,
            transform_func=lambda x: x ** 2,
        )
    )
    print(f"Async evens squared (1..20): {async_results}")

    # Verify both pipelines give the same result
    assert results == async_results, "Mismatch between sync and async pipelines!"
    print("\nSync and async pipelines produce identical results.")
