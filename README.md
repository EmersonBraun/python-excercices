# Python Exercises

A collection of **45 hands-on Python exercises** organized into 6 progressive difficulty levels — from "Hello World" to building REST APIs and data pipelines.

Every exercise is a **standalone, runnable file** (`python3 filename.py`) that includes:

- A docstring explaining the problem
- Difficulty rating and estimated completion time
- Expected input/output examples
- A complete working implementation with a demo in `__main__`

No external dependencies required — everything runs on the Python 3.10+ standard library.

---

## Quick Start

```bash
git clone https://github.com/EmersonBraun/python-excercices.git
cd python-excercices

# Run any exercise directly
python3 level-1-foundations/03-fizzbuzz.py
python3 level-4-oop/05-design-patterns.py
```

---

## Exercises

### Level 1 — Foundations

> Variables, data types, I/O, conditionals, loops, strings, lists

| # | Exercise | Difficulty | Time |
|---|----------|-----------|------|
| 01 | [Hello World](level-1-foundations/01-hello-world.py) — print, f-strings, format variants | ⭐ | 5 min |
| 02 | [Temperature Converter](level-1-foundations/02-temperature-converter.py) — Celsius, Fahrenheit, Kelvin | ⭐ | 10 min |
| 03 | [FizzBuzz](level-1-foundations/03-fizzbuzz.py) — classic 1–100 challenge | ⭐ | 10 min |
| 04 | [Simple Calculator](level-1-foundations/04-simple-calculator.py) — arithmetic with history | ⭐⭐ | 15 min |
| 05 | [Number Guessing Game](level-1-foundations/05-number-guessing-game.py) — random numbers, hints, scoring | ⭐⭐ | 15 min |
| 06 | [String Reversal & Palindrome](level-1-foundations/06-string-reversal-palindrome.py) — slicing, recursion | ⭐ | 10 min |
| 07 | [Count Vowels & Consonants](level-1-foundations/07-count-vowels-consonants.py) — frequency analysis | ⭐ | 10 min |
| 08 | [Basic List Operations](level-1-foundations/08-basic-list-operations.py) — sort, filter, max/min, flatten | ⭐⭐ | 15 min |

### Level 2 — Functions & Collections

> Functions, recursion, dictionaries, sets, comprehensions

| # | Exercise | Difficulty | Time |
|---|----------|-----------|------|
| 01 | [Fibonacci](level-2-functions/01-fibonacci.py) — iterative, recursive, memoized, generator | ⭐⭐ | 15 min |
| 02 | [Factorial](level-2-functions/02-factorial.py) — iterative, recursive, combinations, permutations | ⭐⭐ | 10 min |
| 03 | [Prime Numbers](level-2-functions/03-prime-numbers.py) — checker, Sieve of Eratosthenes, factorization | ⭐⭐ | 20 min |
| 04 | [Word Frequency](level-2-functions/04-word-frequency.py) — Counter, text cleaning, statistics | ⭐⭐ | 15 min |
| 05 | [Shopping Cart](level-2-functions/05-shopping-cart.py) — add/remove, totals, discounts, receipt | ⭐⭐⭐ | 20 min |
| 06 | [Stack & Queue](level-2-functions/06-stack-queue.py) — LIFO/FIFO, balanced parentheses, Hot Potato | ⭐⭐ | 15 min |
| 07 | [Anagram Checker](level-2-functions/07-anagram-checker.py) — sorting, counting, grouping | ⭐⭐ | 10 min |
| 08 | [Caesar Cipher](level-2-functions/08-caesar-cipher.py) — encrypt, decrypt, brute force, frequency analysis | ⭐⭐ | 15 min |

### Level 3 — Intermediate

> File I/O, exception handling, modules, OOP basics

| # | Exercise | Difficulty | Time |
|---|----------|-----------|------|
| 01 | [CSV Reader/Writer](level-3-intermediate/01-csv-reader-writer.py) — generate, parse, filter CSV data | ⭐⭐ | 15 min |
| 02 | [JSON Config Manager](level-3-intermediate/02-json-config-manager.py) — load, save, nested dot-notation access | ⭐⭐ | 15 min |
| 03 | [Contact Book](level-3-intermediate/03-contact-book.py) — full CRUD with JSON persistence and search | ⭐⭐⭐ | 30 min |
| 04 | [Bank Account](level-3-intermediate/04-bank-account.py) — deposit, withdraw, transfer, statement | ⭐⭐⭐ | 25 min |
| 05 | [Card Game](level-3-intermediate/05-card-game.py) — deck, shuffle, deal, hand comparison | ⭐⭐⭐ | 25 min |
| 06 | [Custom Exceptions](level-3-intermediate/06-custom-exceptions.py) — exception hierarchy, validation | ⭐⭐ | 15 min |
| 07 | [Logger](level-3-intermediate/07-logger.py) — levels, colored output, file logging | ⭐⭐⭐ | 20 min |
| 08 | [Text Statistics](level-3-intermediate/08-text-statistics.py) — word count, reading time, common words | ⭐⭐ | 20 min |

### Level 4 — Object-Oriented Programming

> Classes, inheritance, polymorphism, encapsulation, magic methods, design patterns

| # | Exercise | Difficulty | Time |
|---|----------|-----------|------|
| 01 | [Shape Hierarchy](level-4-oop/01-shape-hierarchy.py) — ABC, Circle, Rectangle, Triangle | ⭐⭐⭐ | 20 min |
| 02 | [Animal Hierarchy](level-4-oop/02-animal-hierarchy.py) — polymorphic speak/eat, tricks | ⭐⭐ | 15 min |
| 03 | [Custom List](level-4-oop/03-custom-list.py) — 12+ dunder methods, slicing, iteration | ⭐⭐⭐ | 25 min |
| 04 | [Library System](level-4-oop/04-library-system.py) — Book, Author, Member, borrow/return | ⭐⭐⭐⭐ | 30 min |
| 05 | [Design Patterns](level-4-oop/05-design-patterns.py) — Singleton, Observer, Factory | ⭐⭐⭐⭐ | 30 min |
| 06 | [Inventory System](level-4-oop/06-inventory-system.py) — products, categories, stock, perishables | ⭐⭐⭐ | 25 min |

### Level 5 — Advanced Python

> Decorators, generators, context managers, async/await, type hints, metaclasses

| # | Exercise | Difficulty | Time |
|---|----------|-----------|------|
| 01 | [Decorators](level-5-advanced/01-decorators.py) — timing, retry, memoize, logging | ⭐⭐⭐ | 20 min |
| 02 | [Generators](level-5-advanced/02-generators.py) — infinite Fibonacci, prime generator, pipelines | ⭐⭐⭐ | 20 min |
| 03 | [Context Managers](level-5-advanced/03-context-managers.py) — temp files, timer, DB mock | ⭐⭐⭐ | 20 min |
| 04 | [Async Scraper](level-5-advanced/04-async-scraper.py) — asyncio, concurrent fetching | ⭐⭐⭐⭐ | 25 min |
| 05 | [Type Annotations](level-5-advanced/05-type-annotations.py) — dataclasses, runtime validation | ⭐⭐⭐ | 20 min |
| 06 | [Metaclasses](level-5-advanced/06-metaclasses.py) — auto properties, validation, singleton | ⭐⭐⭐⭐⭐ | 30 min |
| 07 | [Coroutine Pipeline](level-5-advanced/07-coroutine-pipeline.py) — producer, filter, transform, consumer | ⭐⭐⭐⭐ | 25 min |

### Level 6 — Practical Applications

> REST APIs, databases, testing, CLI tools, web scraping, data processing

| # | Exercise | Difficulty | Time |
|---|----------|-----------|------|
| 01 | [Weather CLI](level-6-practical/01-weather-cli.py) — OpenWeatherMap API with mock fallback | ⭐⭐⭐ | 25 min |
| 02 | [GitHub Stats](level-6-practical/02-github-stats.py) — fetch repo/user stats via GitHub API | ⭐⭐⭐ | 20 min |
| 03 | [SQLite Task Manager](level-6-practical/03-sqlite-task-manager.py) — CRUD, priorities, due dates | ⭐⭐⭐ | 25 min |
| 04 | [Web Scraper](level-6-practical/04-web-scraper.py) — HTML parsing with stdlib | ⭐⭐⭐ | 20 min |
| 05 | [Pytest Examples](level-6-practical/05-pytest-examples.py) — unit tests, parameterized, fixtures | ⭐⭐⭐ | 20 min |
| 06 | [CLI Tool](level-6-practical/06-cli-tool.py) — argparse with subcommands | ⭐⭐⭐ | 20 min |
| 07 | [REST API](level-6-practical/07-rest-api.py) — http.server in-memory CRUD | ⭐⭐⭐⭐ | 30 min |
| 08 | [Data Pipeline](level-6-practical/08-data-pipeline.py) — CSV generate, transform, aggregate, report | ⭐⭐⭐ | 25 min |

---

## Requirements

- **Python 3.10+** (no external packages needed)
- All exercises use only the standard library

## License

MIT
