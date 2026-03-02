"""
Library Management System
===========================
Difficulty: 4/5
Estimated time: 30 minutes

Problem:
--------
Design a library system with multiple interacting classes:
1. Author - name, nationality, list of books.
2. Book - title, author, ISBN, genre, available copies.
3. Member - name, member_id, borrowed books (with due dates).
4. Library - collection of books and members, borrow/return logic.

Features:
- Add books and members to the library.
- Borrow a book (with availability check and due date).
- Return a book (with optional late fee calculation).
- Search books by title, author, or genre.
- View a member's currently borrowed books.
- Display library statistics.

Concepts practiced:
- Multi-class design with relationships
- Composition and aggregation
- Date/time manipulation
- Search and filtering
- Encapsulation

Expected output (example):
--------------------------
# Library 'City Library' created.
# Added book: 'The Great Gatsby' by F. Scott Fitzgerald (3 copies)
# Added member: Alice (M001)
#
# Alice borrows 'The Great Gatsby' - Due: 2024-02-14
# Available copies of 'The Great Gatsby': 2
#
# Alice returns 'The Great Gatsby' - On time!
# Available copies of 'The Great Gatsby': 3
#
# Search 'gatsby': [The Great Gatsby by F. Scott Fitzgerald]
"""

from datetime import datetime, timedelta


class Author:
    """Represents a book author."""

    def __init__(self, name, nationality="Unknown"):
        self.name = name
        self.nationality = nationality
        self.books = []

    def add_book(self, book):
        """Associate a book with this author."""
        if book not in self.books:
            self.books.append(book)

    def __repr__(self):
        return f"Author({self.name!r})"

    def __str__(self):
        return self.name


class Book:
    """Represents a book in the library."""

    def __init__(self, title, author, isbn, genre="General", total_copies=1):
        """
        Parameters:
            title (str): Book title.
            author (Author): The book's author.
            isbn (str): ISBN identifier.
            genre (str): Genre/category.
            total_copies (int): Total number of copies owned by the library.
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies

        # Register with author
        author.add_book(self)

    def is_available(self):
        """Check if at least one copy is available."""
        return self.available_copies > 0

    def __repr__(self):
        return f"Book({self.title!r}, by {self.author.name})"

    def __str__(self):
        return f"'{self.title}' by {self.author.name}"


class Member:
    """Represents a library member."""

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # list of {"book": Book, "due_date": datetime}
        self.borrow_history = []  # completed borrows

    def current_borrows(self):
        """Return list of currently borrowed books with due dates."""
        return list(self.borrowed_books)

    def has_book(self, book):
        """Check if this member currently has a specific book."""
        return any(b["book"] is book for b in self.borrowed_books)

    def __repr__(self):
        return f"Member({self.name!r}, {self.member_id!r})"

    def __str__(self):
        return f"{self.name} ({self.member_id})"


class Library:
    """A library managing books and members."""

    LOAN_PERIOD_DAYS = 14
    LATE_FEE_PER_DAY = 0.50

    def __init__(self, name):
        self.name = name
        self.books = []
        self.members = []
        print(f"Library '{self.name}' created.")

    # ---- Management ----

    def add_book(self, book):
        """Add a book to the library collection."""
        self.books.append(book)
        print(f"Added book: {book} ({book.total_copies} copies)")

    def add_member(self, member):
        """Register a member."""
        self.members.append(member)
        print(f"Added member: {member}")

    # ---- Borrow / Return ----

    def borrow_book(self, member, book, borrow_date=None):
        """
        Let a member borrow a book.

        Parameters:
            member (Member): The borrower.
            book (Book): The book to borrow.
            borrow_date (datetime, optional): Override borrow date (for testing).

        Returns:
            bool: True if borrow succeeded.
        """
        if not book.is_available():
            print(f"Sorry, '{book.title}' has no available copies.")
            return False

        if member.has_book(book):
            print(f"{member.name} already has a copy of '{book.title}'.")
            return False

        borrow_date = borrow_date or datetime.now()
        due_date = borrow_date + timedelta(days=self.LOAN_PERIOD_DAYS)

        book.available_copies -= 1
        member.borrowed_books.append({
            "book": book,
            "borrow_date": borrow_date,
            "due_date": due_date,
        })

        print(
            f"{member.name} borrows {book} - "
            f"Due: {due_date.strftime('%Y-%m-%d')}"
        )
        return True

    def return_book(self, member, book, return_date=None):
        """
        Process a book return.

        Parameters:
            member (Member): The returner.
            book (Book): The book being returned.
            return_date (datetime, optional): Override return date (for testing).

        Returns:
            float: Late fee (0.0 if on time), or -1 if the book was not borrowed.
        """
        record = None
        for i, b in enumerate(member.borrowed_books):
            if b["book"] is book:
                record = member.borrowed_books.pop(i)
                break

        if record is None:
            print(f"{member.name} does not have '{book.title}'.")
            return -1

        return_date = return_date or datetime.now()
        book.available_copies += 1

        # Calculate late fee
        late_fee = 0.0
        if return_date > record["due_date"]:
            days_late = (return_date - record["due_date"]).days
            late_fee = days_late * self.LATE_FEE_PER_DAY
            print(
                f"{member.name} returns {book} - "
                f"{days_late} days late! Fee: ${late_fee:.2f}"
            )
        else:
            print(f"{member.name} returns {book} - On time!")

        # Add to history
        record["return_date"] = return_date
        record["late_fee"] = late_fee
        member.borrow_history.append(record)

        return late_fee

    # ---- Search ----

    def search_by_title(self, query):
        """Search books by title (case-insensitive partial match)."""
        return [b for b in self.books if query.lower() in b.title.lower()]

    def search_by_author(self, query):
        """Search books by author name."""
        return [b for b in self.books if query.lower() in b.author.name.lower()]

    def search_by_genre(self, genre):
        """Search books by genre."""
        return [b for b in self.books if b.genre.lower() == genre.lower()]

    # ---- Display ----

    def show_member_borrows(self, member):
        """Display a member's currently borrowed books."""
        borrows = member.current_borrows()
        print(f"\n{member.name}'s borrowed books ({len(borrows)}):")
        if not borrows:
            print("  (none)")
        for b in borrows:
            due = b["due_date"].strftime("%Y-%m-%d")
            print(f"  - {b['book']} (due {due})")

    def statistics(self):
        """Display library statistics."""
        total_books = sum(b.total_copies for b in self.books)
        available = sum(b.available_copies for b in self.books)
        borrowed = total_books - available

        print(f"\n=== {self.name} Statistics ===")
        print(f"  Unique titles: {len(self.books)}")
        print(f"  Total copies:  {total_books}")
        print(f"  Available:     {available}")
        print(f"  Borrowed:      {borrowed}")
        print(f"  Members:       {len(self.members)}")


if __name__ == "__main__":
    print("--- Library System Demo ---\n")

    # Create library
    lib = Library("City Library")
    print()

    # Create authors
    fitzgerald = Author("F. Scott Fitzgerald", "American")
    orwell = Author("George Orwell", "British")
    tolkien = Author("J.R.R. Tolkien", "British")

    # Create books
    gatsby = Book("The Great Gatsby", fitzgerald, "978-0-7432-7356-5", "Fiction", 3)
    nineteen84 = Book("1984", orwell, "978-0-451-52493-5", "Dystopian", 2)
    hobbit = Book("The Hobbit", tolkien, "978-0-547-92822-7", "Fantasy", 4)
    farm = Book("Animal Farm", orwell, "978-0-451-52634-2", "Satire", 2)

    # Add books to library
    for book in [gatsby, nineteen84, hobbit, farm]:
        lib.add_book(book)
    print()

    # Create and add members
    alice = Member("Alice", "M001")
    bob = Member("Bob", "M002")
    lib.add_member(alice)
    lib.add_member(bob)
    print()

    # Borrow books
    today = datetime(2024, 1, 15)
    lib.borrow_book(alice, gatsby, borrow_date=today)
    lib.borrow_book(alice, nineteen84, borrow_date=today)
    lib.borrow_book(bob, hobbit, borrow_date=today)
    print(f"\nAvailable copies of 'The Great Gatsby': {gatsby.available_copies}")

    # Show member borrows
    lib.show_member_borrows(alice)
    lib.show_member_borrows(bob)

    # Return on time
    print()
    return_date_ontime = today + timedelta(days=10)
    lib.return_book(alice, gatsby, return_date=return_date_ontime)

    # Return late
    return_date_late = today + timedelta(days=20)
    lib.return_book(alice, nineteen84, return_date=return_date_late)
    print(f"Available copies of 'The Great Gatsby': {gatsby.available_copies}")

    # Search
    print("\n--- Search ---")
    results = lib.search_by_title("gatsby")
    print(f"Search 'gatsby': {results}")

    results = lib.search_by_author("orwell")
    print(f"Search author 'orwell': {results}")

    results = lib.search_by_genre("fantasy")
    print(f"Search genre 'fantasy': {results}")

    # Author's books
    print(f"\nOrwell's books: {[str(b) for b in orwell.books]}")

    # Statistics
    lib.statistics()

    # Edge case: borrow unavailable
    print()
    lib.borrow_book(bob, gatsby)
    lib.borrow_book(bob, gatsby)  # already borrowed
