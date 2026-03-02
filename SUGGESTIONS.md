# Python Exercises — Curriculum Plan & Suggestions

## Current Exercise Inventory
[List all exercises found in the repo]

## Proposed Organization: Basic to Advanced

### Level 1 — Foundations (Beginner)
**Concepts:** Variables, data types, string manipulation, arithmetic, conditionals, loops, basic I/O

Suggested exercises:
1. Hello World variants
2. Temperature converter (Celsius <-> Fahrenheit <-> Kelvin)
3. FizzBuzz
4. Simple calculator
5. Number guessing game (input/output loop)
6. String reversal and palindrome check
7. Count vowels and consonants
8. Basic list operations (sort, filter, find max/min)

### Level 2 — Functions & Collections (Beginner-Intermediate)
**Concepts:** Functions, recursion, lists, tuples, dictionaries, sets, comprehensions

Suggested exercises:
1. Fibonacci sequence (iterative and recursive)
2. Factorial calculator
3. Prime number checker + sieve of Eratosthenes
4. Word frequency counter
5. Shopping cart simulation
6. Stack and Queue implementations with lists
7. Anagram checker
8. Caesar cipher

### Level 3 — Intermediate Python
**Concepts:** File I/O, exception handling, modules, OOP basics

Suggested exercises:
1. CSV file reader/writer
2. JSON configuration file manager
3. Simple contact book (CRUD with file persistence)
4. Bank account class with transactions
5. Card game simulation (deck, hand, shuffle)
6. Custom exception classes
7. Logger implementation
8. Text statistics analyzer

### Level 4 — Object-Oriented Programming
**Concepts:** Classes, inheritance, polymorphism, encapsulation, magic methods

Suggested exercises:
1. Shape hierarchy (Circle, Rectangle, Triangle with area/perimeter)
2. Animal hierarchy with polymorphic speak()
3. Custom list class implementing __iter__, __len__, __getitem__
4. Library management system (Book, Author, Library classes)
5. Design patterns: Singleton, Observer, Factory
6. Inventory system with inheritance

### Level 5 — Advanced Python
**Concepts:** Decorators, generators, context managers, async/await, type hints

Suggested exercises:
1. Timing decorator / retry decorator
2. Infinite Fibonacci generator
3. Custom context manager for temp files
4. Async web scraper with asyncio + aiohttp
5. Type-annotated data structures with validation
6. Metaclass for automatic property creation
7. Coroutine pipeline

### Level 6 — Practical Applications
**Concepts:** Web scraping, REST APIs, databases, testing, CLI tools

Suggested exercises:
1. Weather CLI using OpenWeatherMap API
2. GitHub repo stats fetcher
3. SQLite task manager (CRUD operations)
4. Web scraper with BeautifulSoup (news headlines)
5. Unit tests with pytest (TDD approach)
6. CLI tool with argparse + subcommands
7. Simple REST API with FastAPI
8. Data processing pipeline with pandas

## Repository Structure Recommendation

```
python-exercises/
├── README.md
├── SUGGESTIONS.md
├── level-1-foundations/
│   ├── 01-hello-world.py
│   ├── 02-temperature-converter.py
│   └── ...
├── level-2-functions/
│   ├── 01-fibonacci.py
│   └── ...
├── level-3-intermediate/
├── level-4-oop/
├── level-5-advanced/
└── level-6-practical/
```

## Quality Improvements
- Add docstrings to all exercise files explaining the problem
- Add expected input/output examples in comments
- Include solution files in a `solutions/` subfolder
- Add pytest test cases for each exercise
- Add difficulty rating (⭐ to ⭐⭐⭐⭐⭐)
- Add estimated completion time
