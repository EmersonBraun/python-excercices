import sqlite3


def test_decorator():
    def timer(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @timer
    def add(a, b):
        return a + b

    assert add(1, 2) == 3


def test_generator():
    def fib_gen():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    gen = fib_gen()
    results = [next(gen) for _ in range(6)]
    assert results == [0, 1, 1, 2, 3, 5]


def test_sqlite_crud():
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
    cur.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
    conn.commit()
    cur.execute('SELECT name FROM users')
    assert cur.fetchone()[0] == 'Alice'
    conn.close()
