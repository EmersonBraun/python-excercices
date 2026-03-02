"""
Level 6 - Exercise 07: Simple REST API (stdlib only)
=====================================================

Difficulty: 4/5 stars
Estimated time: 30 minutes

Build a REST API using ONLY http.server and json from the standard
library.  No Flask, FastAPI, or other frameworks required.

The API manages a collection of "books" with full CRUD operations.

Endpoints
---------
GET    /api/books          - List all books
GET    /api/books/<id>     - Get a single book
POST   /api/books          - Create a new book
PUT    /api/books/<id>     - Update a book
DELETE /api/books/<id>     - Delete a book
GET    /api/books/search?q=<query>  - Search books by title/author

Usage:
    python3 07-rest-api.py                   # Start server on port 8000
    python3 07-rest-api.py --port 3000       # Custom port
    python3 07-rest-api.py --demo            # Run demo client instead

Test with curl:
    curl http://localhost:8000/api/books
    curl -X POST http://localhost:8000/api/books \\
         -H "Content-Type: application/json" \\
         -d '{"title": "Python Crash Course", "author": "Eric Matthes"}'

Expected output (demo mode):
-----------------------------
    POST /api/books -> 201 {"id": 1, "title": "Python Crash Course", ...}
    GET  /api/books -> 200 [{"id": 1, ...}, {"id": 2, ...}]
    ...
"""

import argparse
import json
import re
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from urllib.error import URLError


# ---------------------------------------------------------------------------
# In-Memory Data Store
# ---------------------------------------------------------------------------
class BookStore:
    """Thread-safe in-memory storage for books."""

    def __init__(self):
        self._books: dict[int, dict] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    def list_all(self) -> list[dict]:
        with self._lock:
            return list(self._books.values())

    def get(self, book_id: int) -> dict | None:
        with self._lock:
            return self._books.get(book_id)

    def create(self, data: dict) -> dict:
        with self._lock:
            book = {
                "id": self._next_id,
                "title": data.get("title", "Untitled"),
                "author": data.get("author", "Unknown"),
                "year": data.get("year"),
                "genre": data.get("genre"),
                "pages": data.get("pages"),
            }
            self._books[self._next_id] = book
            self._next_id += 1
            return book

    def update(self, book_id: int, data: dict) -> dict | None:
        with self._lock:
            if book_id not in self._books:
                return None
            book = self._books[book_id]
            for key in ("title", "author", "year", "genre", "pages"):
                if key in data:
                    book[key] = data[key]
            return book

    def delete(self, book_id: int) -> bool:
        with self._lock:
            return self._books.pop(book_id, None) is not None

    def search(self, query: str) -> list[dict]:
        query_lower = query.lower()
        with self._lock:
            return [
                b for b in self._books.values()
                if query_lower in (b.get("title") or "").lower()
                or query_lower in (b.get("author") or "").lower()
            ]

    def seed(self):
        """Add sample data."""
        samples = [
            {"title": "Python Crash Course", "author": "Eric Matthes",
             "year": 2019, "genre": "Programming", "pages": 544},
            {"title": "Clean Code", "author": "Robert C. Martin",
             "year": 2008, "genre": "Programming", "pages": 464},
            {"title": "The Pragmatic Programmer", "author": "David Thomas",
             "year": 2019, "genre": "Programming", "pages": 352},
            {"title": "Dune", "author": "Frank Herbert",
             "year": 1965, "genre": "Science Fiction", "pages": 688},
        ]
        for s in samples:
            self.create(s)


# Global store instance
store = BookStore()


# ---------------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------------
class BookAPIHandler(BaseHTTPRequestHandler):
    """Handle REST API requests for the book collection."""

    # Route patterns
    BOOKS_LIST = re.compile(r"^/api/books/?$")
    BOOKS_DETAIL = re.compile(r"^/api/books/(\d+)/?$")
    BOOKS_SEARCH = re.compile(r"^/api/books/search/?$")

    def _send_json(self, data, status=200):
        """Send a JSON response."""
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status, message):
        self._send_json({"error": message}, status=status)

    def _read_body(self) -> dict:
        """Read and parse JSON request body."""
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    # --- GET ---
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Search
        match = self.BOOKS_SEARCH.match(path)
        if match:
            params = parse_qs(parsed.query)
            query = params.get("q", [""])[0]
            if not query:
                self._send_error(400, "Missing search query parameter 'q'")
                return
            results = store.search(query)
            self._send_json(results)
            return

        # List all
        if self.BOOKS_LIST.match(path):
            self._send_json(store.list_all())
            return

        # Get by ID
        match = self.BOOKS_DETAIL.match(path)
        if match:
            book_id = int(match.group(1))
            book = store.get(book_id)
            if book:
                self._send_json(book)
            else:
                self._send_error(404, f"Book {book_id} not found")
            return

        # Root / health check
        if path in ("/", "/api", "/api/"):
            self._send_json({
                "message": "Book API is running",
                "endpoints": {
                    "list":   "GET    /api/books",
                    "detail": "GET    /api/books/<id>",
                    "create": "POST   /api/books",
                    "update": "PUT    /api/books/<id>",
                    "delete": "DELETE /api/books/<id>",
                    "search": "GET    /api/books/search?q=<query>",
                },
            })
            return

        self._send_error(404, "Not found")

    # --- POST ---
    def do_POST(self):
        if self.BOOKS_LIST.match(self.path):
            try:
                data = self._read_body()
            except (json.JSONDecodeError, ValueError):
                self._send_error(400, "Invalid JSON body")
                return
            if not data.get("title"):
                self._send_error(400, "Field 'title' is required")
                return
            book = store.create(data)
            self._send_json(book, status=201)
        else:
            self._send_error(404, "Not found")

    # --- PUT ---
    def do_PUT(self):
        match = self.BOOKS_DETAIL.match(self.path)
        if match:
            book_id = int(match.group(1))
            try:
                data = self._read_body()
            except (json.JSONDecodeError, ValueError):
                self._send_error(400, "Invalid JSON body")
                return
            book = store.update(book_id, data)
            if book:
                self._send_json(book)
            else:
                self._send_error(404, f"Book {book_id} not found")
        else:
            self._send_error(404, "Not found")

    # --- DELETE ---
    def do_DELETE(self):
        match = self.BOOKS_DETAIL.match(self.path)
        if match:
            book_id = int(match.group(1))
            if store.delete(book_id):
                self._send_json({"message": f"Book {book_id} deleted"})
            else:
                self._send_error(404, f"Book {book_id} not found")
        else:
            self._send_error(404, "Not found")

    # --- OPTIONS (CORS) ---
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Override to customise log output."""
        print(f"  [{self.log_date_time_string()}] {format % args}")


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
def run_server(port: int = 8000):
    """Start the HTTP server."""
    store.seed()
    server = HTTPServer(("", port), BookAPIHandler)
    print(f"Book API server running on http://localhost:{port}")
    print(f"Endpoints: GET/POST /api/books, GET/PUT/DELETE /api/books/<id>")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


# ---------------------------------------------------------------------------
# Demo Client (tests the API without curl)
# ---------------------------------------------------------------------------
def api_request(base: str, method: str, path: str,
                data: dict | None = None) -> tuple[int, dict | list]:
    """Make an HTTP request and return (status_code, parsed_json)."""
    url = f"{base}{path}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        # Extract status from HTTPError if possible
        status = getattr(exc, "code", 0)
        try:
            body = json.loads(exc.read().decode("utf-8"))
        except Exception:
            body = {"error": str(exc)}
        return status, body


def run_demo(port: int = 8000):
    """Start server in background, run demo requests, then shut down."""
    store.seed()
    server = HTTPServer(("", port), BookAPIHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.3)  # let server spin up

    base = f"http://localhost:{port}"

    print("=" * 60)
    print("REST API Demo Client")
    print("=" * 60)

    def show(method, path, status, body):
        print(f"\n{method:6} {path}")
        print(f"  Status: {status}")
        formatted = json.dumps(body, indent=2)
        # Truncate long output
        if len(formatted) > 400:
            formatted = formatted[:400] + "\n  ... (truncated)"
        for line in formatted.split("\n"):
            print(f"  {line}")

    # 1. List all (seeded)
    status, body = api_request(base, "GET", "/api/books")
    show("GET", "/api/books", status, body)

    # 2. Create a new book
    new_book = {
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "year": 2022,
        "genre": "Programming",
        "pages": 1012,
    }
    status, body = api_request(base, "POST", "/api/books", new_book)
    show("POST", "/api/books", status, body)
    new_id = body.get("id")

    # 3. Get the new book
    status, body = api_request(base, "GET", f"/api/books/{new_id}")
    show("GET", f"/api/books/{new_id}", status, body)

    # 4. Update the book
    status, body = api_request(base, "PUT", f"/api/books/{new_id}",
                               {"pages": 1014})
    show("PUT", f"/api/books/{new_id}", status, body)

    # 5. Search
    status, body = api_request(base, "GET", "/api/books/search?q=python")
    show("GET", "/api/books/search?q=python", status, body)

    # 6. Delete
    status, body = api_request(base, "DELETE", f"/api/books/{new_id}")
    show("DELETE", f"/api/books/{new_id}", status, body)

    # 7. Verify deletion
    status, body = api_request(base, "GET", f"/api/books/{new_id}")
    show("GET", f"/api/books/{new_id} (after delete)", status, body)

    # 8. Error case
    status, body = api_request(base, "POST", "/api/books", {"author": "No title"})
    show("POST", "/api/books (missing title)", status, body)

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)

    server.shutdown()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple REST API for books")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--demo", action="store_true",
                        help="Run demo client (starts server, makes requests, stops)")
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.demo:
        run_demo(port=args.port)
    else:
        run_server(port=args.port)
