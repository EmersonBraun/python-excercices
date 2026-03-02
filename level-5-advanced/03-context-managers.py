"""
Level 5 - Exercise 03: Context Managers
=========================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Learn to build custom context managers using both the class-based
protocol (__enter__ / __exit__) and the contextlib helper.

Exercises
---------
1. TempFileManager   - Creates a temp file on enter, deletes it on exit.
2. Timer             - Measures elapsed time inside a `with` block.
3. DatabaseMock      - Simulates a DB connection with commit / rollback.

Expected output (approximate):
------------------------------
# TempFileManager
# Created temp file: /tmp/xyz.txt
# ... use the file ...
# Temp file deleted.

# Timer
# Block took 0.3012 seconds

# DatabaseMock
# Connected to 'test.db'
# Executing: INSERT INTO users VALUES ('Alice')
# Transaction committed.
# Connection to 'test.db' closed.
"""

import os
import time
import tempfile
from contextlib import contextmanager


# ---------------------------------------------------------------------------
# 1. TempFileManager (class-based)
# ---------------------------------------------------------------------------
class TempFileManager:
    """Context manager that creates a temporary file and removes it on exit.

    Usage:
        with TempFileManager(suffix=".txt") as path:
            with open(path, "w") as f:
                f.write("hello")
            # path is a string pointing to the temp file
        # file is automatically deleted here

    >>> with TempFileManager(suffix=".txt") as path:
    ...     assert os.path.exists(path)
    >>> assert not os.path.exists(path)
    """

    def __init__(self, suffix=".tmp", prefix="ctx_"):
        self.suffix = suffix
        self.prefix = prefix
        self.path = None

    def __enter__(self):
        fd, self.path = tempfile.mkstemp(suffix=self.suffix, prefix=self.prefix)
        os.close(fd)  # close the low-level file descriptor
        print(f"Created temp file: {self.path}")
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path and os.path.exists(self.path):
            os.unlink(self.path)
            print(f"Temp file deleted: {self.path}")
        return False  # do not suppress exceptions


# ---------------------------------------------------------------------------
# 2. Timer (contextlib-based)
# ---------------------------------------------------------------------------
@contextmanager
def timer(label="Block"):
    """Context manager that measures wall-clock time of the enclosed block.

    Usage:
        with timer("my computation"):
            heavy_work()
        # prints: my computation took 1.2345 seconds

    >>> import time
    >>> with timer("sleep test"):
    ...     time.sleep(0.1)
    sleep test took ... seconds
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.4f} seconds")


# ---------------------------------------------------------------------------
# 3. DatabaseMock (class-based, simulates connection lifecycle)
# ---------------------------------------------------------------------------
class DatabaseMock:
    """Simulates a database connection context manager.

    On __enter__: opens a (fake) connection.
    On __exit__:  commits if no exception occurred, otherwise rolls back.
    Always closes the connection.

    Usage:
        with DatabaseMock("myapp.db") as db:
            db.execute("INSERT INTO users VALUES ('Alice')")
            db.execute("INSERT INTO users VALUES ('Bob')")
        # auto-commits on success, auto-rolls-back on exception

    >>> with DatabaseMock("test.db") as db:
    ...     db.execute("SELECT 1")
    Executing: SELECT 1
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False
        self.queries = []

    def __enter__(self):
        self.connected = True
        print(f"Connected to '{self.db_name}'")
        return self

    def execute(self, query):
        if not self.connected:
            raise RuntimeError("Not connected to the database")
        print(f"Executing: {query}")
        self.queries.append(query)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("Transaction committed.")
        else:
            print(f"Transaction rolled back due to: {exc_val}")
        self.connected = False
        self.queries.clear()
        print(f"Connection to '{self.db_name}' closed.")
        return False  # do not suppress exceptions


# ---------------------------------------------------------------------------
# Bonus: Nested / composed context manager
# ---------------------------------------------------------------------------
@contextmanager
def managed_temp_db(db_name="temp.db"):
    """Combines TempFileManager + DatabaseMock for a self-cleaning DB demo.

    Creates a temp file (simulating a DB file), opens a mock connection,
    and cleans everything up on exit.
    """
    with TempFileManager(suffix=".db") as db_path:
        with DatabaseMock(db_name) as db:
            db.db_path = db_path  # attach path for reference
            yield db


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    # --- 1. TempFileManager ---
    print("=" * 50)
    print("1. TempFileManager")
    print("=" * 50)
    with TempFileManager(suffix=".txt") as path:
        with open(path, "w") as f:
            f.write("Hello from context manager!")
        with open(path) as f:
            print(f"  File content: {f.read()}")
        print(f"  File exists inside block: {os.path.exists(path)}")
    print(f"  File exists after block:  {os.path.exists(path)}")
    print()

    # --- 2. Timer ---
    print("=" * 50)
    print("2. Timer")
    print("=" * 50)
    with timer("Sleep 0.2s"):
        time.sleep(0.2)
    with timer("Sum of squares"):
        total = sum(x * x for x in range(1_000_000))
        print(f"  Total: {total}")
    print()

    # --- 3. DatabaseMock ---
    print("=" * 50)
    print("3. DatabaseMock  (successful transaction)")
    print("=" * 50)
    with DatabaseMock("myapp.db") as db:
        db.execute("CREATE TABLE users (name TEXT)")
        db.execute("INSERT INTO users VALUES ('Alice')")
        db.execute("INSERT INTO users VALUES ('Bob')")
    print()

    print("=" * 50)
    print("3b. DatabaseMock (failed transaction)")
    print("=" * 50)
    try:
        with DatabaseMock("myapp.db") as db:
            db.execute("INSERT INTO users VALUES ('Charlie')")
            raise ValueError("Something went wrong!")
    except ValueError:
        print("  Exception caught outside the block.\n")

    # --- Bonus: nested ---
    print("=" * 50)
    print("Bonus: Nested context managers")
    print("=" * 50)
    with managed_temp_db("composed.db") as db:
        db.execute("INSERT INTO logs VALUES ('event_1')")
        print(f"  DB file path: {db.db_path}")
