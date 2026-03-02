"""
Level 6 - Exercise 04: Web Scraper (Stdlib Only)
==================================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Build a web scraper using ONLY the Python standard library.
Uses html.parser.HTMLParser instead of BeautifulSoup.
Works entirely on inline HTML strings, so no network access is needed.

Features
--------
- Custom HTMLParser subclass that extracts structured data.
- Extract links, headings, tables, and metadata from HTML.
- Demonstrate parsing of a realistic product-listing page.

Expected output (approximate):
------------------------------
    Found 4 products:
    1. Python Crash Course - $29.99 (4.7 stars)
    2. Clean Code          - $34.50 (4.5 stars)
    ...

    Links found: 6
    Headings: ['Online Bookstore', 'Featured Books', 'About Us']
"""

from html.parser import HTMLParser
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Sample inline HTML (no network needed)
# ---------------------------------------------------------------------------
SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Best online bookstore for developers">
    <meta name="keywords" content="books, programming, python, coding">
    <title>Online Bookstore</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/books">Books</a>
            <a href="/authors">Authors</a>
            <a href="/cart">Cart (0)</a>
        </nav>
    </header>

    <main>
        <h1>Online Bookstore</h1>
        <h2>Featured Books</h2>

        <div class="product-list">
            <div class="product" data-id="1">
                <h3 class="product-name">Python Crash Course</h3>
                <span class="author">Eric Matthes</span>
                <span class="price">$29.99</span>
                <span class="rating">4.7</span>
                <p class="description">A hands-on, project-based introduction to programming.</p>
                <a href="/books/1">View Details</a>
            </div>

            <div class="product" data-id="2">
                <h3 class="product-name">Clean Code</h3>
                <span class="author">Robert C. Martin</span>
                <span class="price">$34.50</span>
                <span class="rating">4.5</span>
                <p class="description">A handbook of agile software craftsmanship.</p>
                <a href="/books/2">View Details</a>
            </div>

            <div class="product" data-id="3">
                <h3 class="product-name">Design Patterns</h3>
                <span class="author">Gang of Four</span>
                <span class="price">$42.00</span>
                <span class="rating">4.3</span>
                <p class="description">Elements of reusable object-oriented software.</p>
                <a href="/books/3">View Details</a>
            </div>

            <div class="product" data-id="4">
                <h3 class="product-name">The Pragmatic Programmer</h3>
                <span class="author">David Thomas, Andrew Hunt</span>
                <span class="price">$39.95</span>
                <span class="rating">4.8</span>
                <p class="description">Your journey to mastery, 20th Anniversary Edition.</p>
                <a href="/books/4">View Details</a>
            </div>
        </div>
    </main>

    <footer>
        <h2>About Us</h2>
        <p>We are a developer-focused bookstore since 2020.</p>
        <a href="/contact">Contact Us</a>
    </footer>
</body>
</html>
"""

TABLE_HTML = """
<table id="sales">
    <thead>
        <tr><th>Month</th><th>Revenue</th><th>Units</th></tr>
    </thead>
    <tbody>
        <tr><td>January</td><td>$12,500</td><td>350</td></tr>
        <tr><td>February</td><td>$14,200</td><td>410</td></tr>
        <tr><td>March</td><td>$11,800</td><td>320</td></tr>
        <tr><td>April</td><td>$15,600</td><td>445</td></tr>
    </tbody>
</table>
"""


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------
@dataclass
class Product:
    name: str = ""
    author: str = ""
    price: str = ""
    rating: str = ""
    description: str = ""
    url: str = ""


@dataclass
class PageData:
    title: str = ""
    meta: dict = field(default_factory=dict)
    headings: list = field(default_factory=list)
    links: list = field(default_factory=list)
    products: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# 1. Link Extractor
# ---------------------------------------------------------------------------
class LinkExtractor(HTMLParser):
    """Extract all <a href="..."> links and their text.

    >>> parser = LinkExtractor()
    >>> parser.feed('<a href="/about">About</a>')
    >>> parser.links
    [{'href': '/about', 'text': 'About'}]
    """

    def __init__(self):
        super().__init__()
        self.links: list[dict] = []
        self._current_href: str | None = None
        self._current_text: str = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attr_dict = dict(attrs)
            self._current_href = attr_dict.get("href", "")
            self._current_text = ""

    def handle_data(self, data):
        if self._current_href is not None:
            self._current_text += data.strip()

    def handle_endtag(self, tag):
        if tag == "a" and self._current_href is not None:
            self.links.append({
                "href": self._current_href,
                "text": self._current_text,
            })
            self._current_href = None


# ---------------------------------------------------------------------------
# 2. Heading Extractor
# ---------------------------------------------------------------------------
class HeadingExtractor(HTMLParser):
    """Extract all heading tags (h1-h6) and their text.

    >>> parser = HeadingExtractor()
    >>> parser.feed('<h1>Title</h1><h2>Subtitle</h2>')
    >>> parser.headings
    [{'level': 1, 'text': 'Title'}, {'level': 2, 'text': 'Subtitle'}]
    """

    HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self):
        super().__init__()
        self.headings: list[dict] = []
        self._in_heading: str | None = None
        self._text: str = ""

    def handle_starttag(self, tag, attrs):
        if tag in self.HEADING_TAGS:
            self._in_heading = tag
            self._text = ""

    def handle_data(self, data):
        if self._in_heading:
            self._text += data.strip()

    def handle_endtag(self, tag):
        if tag == self._in_heading:
            self.headings.append({
                "level": int(self._in_heading[1]),
                "text": self._text,
            })
            self._in_heading = None


# ---------------------------------------------------------------------------
# 3. Product Scraper (domain-specific)
# ---------------------------------------------------------------------------
class ProductScraper(HTMLParser):
    """Scrape product data from the bookstore HTML.

    Tracks CSS classes to extract name, author, price, rating, etc.
    """

    def __init__(self):
        super().__init__()
        self.products: list[Product] = []
        self._current_product: Product | None = None
        self._current_class: str = ""
        self._capture: bool = False
        self._current_tag: str = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        css_class = attr_dict.get("class", "")
        self._current_tag = tag

        if tag == "div" and "product" in css_class and "product-list" not in css_class:
            self._current_product = Product()

        if self._current_product is not None:
            if css_class in ("product-name", "author", "price", "rating", "description"):
                self._current_class = css_class
                self._capture = True

            if tag == "a" and self._current_product is not None:
                href = attr_dict.get("href", "")
                if href.startswith("/books/"):
                    self._current_product.url = href

    def handle_data(self, data):
        if self._capture and self._current_product is not None:
            text = data.strip()
            if self._current_class == "product-name":
                self._current_product.name = text
            elif self._current_class == "author":
                self._current_product.author = text
            elif self._current_class == "price":
                self._current_product.price = text
            elif self._current_class == "rating":
                self._current_product.rating = text
            elif self._current_class == "description":
                self._current_product.description = text

    def handle_endtag(self, tag):
        self._capture = False
        self._current_class = ""

        if tag == "div" and self._current_product is not None:
            if self._current_product.name:  # only save if we got data
                self.products.append(self._current_product)
            self._current_product = None


# ---------------------------------------------------------------------------
# 4. Table Extractor
# ---------------------------------------------------------------------------
class TableExtractor(HTMLParser):
    """Extract tabular data from <table> elements.

    Returns a list of rows, where each row is a list of cell strings.

    >>> parser = TableExtractor()
    >>> parser.feed('<table><tr><td>A</td><td>B</td></tr></table>')
    >>> parser.rows
    [['A', 'B']]
    """

    def __init__(self):
        super().__init__()
        self.headers: list[str] = []
        self.rows: list[list[str]] = []
        self._in_cell: bool = False
        self._in_header: bool = False
        self._current_row: list[str] = []
        self._cell_text: str = ""

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._current_row = []
        elif tag == "th":
            self._in_header = True
            self._in_cell = True
            self._cell_text = ""
        elif tag == "td":
            self._in_cell = True
            self._cell_text = ""

    def handle_data(self, data):
        if self._in_cell:
            self._cell_text += data.strip()

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._in_cell:
            self._current_row.append(self._cell_text)
            self._in_cell = False
            if tag == "th":
                self._in_header = False
        elif tag == "tr":
            if self._current_row:
                # Determine if this is a header row
                if all(c == "" for c in self._current_row):
                    pass
                elif self._current_row and len(self.rows) == 0 and len(self.headers) == 0:
                    # Heuristic: first row from <thead> is headers
                    self.headers = self._current_row
                else:
                    self.rows.append(self._current_row)


# ---------------------------------------------------------------------------
# 5. Meta / Title Extractor
# ---------------------------------------------------------------------------
class MetaExtractor(HTMLParser):
    """Extract <title> and <meta> tags."""

    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.meta: dict[str, str] = {}
        self._in_title: bool = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            attr_dict = dict(attrs)
            name = attr_dict.get("name", "")
            content = attr_dict.get("content", "")
            if name and content:
                self.meta[name] = content

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


# ---------------------------------------------------------------------------
# Convenience: scrape everything at once
# ---------------------------------------------------------------------------
def scrape_page(html: str) -> PageData:
    """Run all extractors on the given HTML and return a PageData object."""
    meta_ext = MetaExtractor()
    meta_ext.feed(html)

    link_ext = LinkExtractor()
    link_ext.feed(html)

    heading_ext = HeadingExtractor()
    heading_ext.feed(html)

    product_ext = ProductScraper()
    product_ext.feed(html)

    return PageData(
        title=meta_ext.title,
        meta=meta_ext.meta,
        headings=[h["text"] for h in heading_ext.headings],
        links=link_ext.links,
        products=product_ext.products,
    )


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":

    # --- Full page scrape ---
    print("=" * 60)
    print("Full Page Scrape")
    print("=" * 60)
    page = scrape_page(SAMPLE_HTML)

    print(f"\nPage title: {page.title}")
    print(f"Meta description: {page.meta.get('description', 'N/A')}")
    print(f"Meta keywords: {page.meta.get('keywords', 'N/A')}")

    print(f"\nHeadings ({len(page.headings)}):")
    for h in page.headings:
        print(f"  - {h}")

    print(f"\nLinks ({len(page.links)}):")
    for link in page.links:
        print(f"  [{link['text']}] -> {link['href']}")

    print(f"\nProducts ({len(page.products)}):")
    for i, p in enumerate(page.products, 1):
        print(f"  {i}. {p.name} by {p.author}")
        print(f"     Price: {p.price}  |  Rating: {p.rating} stars")
        print(f"     {p.description}")
        print(f"     URL: {p.url}")
    print()

    # --- Table scrape ---
    print("=" * 60)
    print("Table Extraction")
    print("=" * 60)
    table_parser = TableExtractor()
    table_parser.feed(TABLE_HTML)

    print(f"\nHeaders: {table_parser.headers}")
    print("Rows:")
    for row in table_parser.rows:
        print(f"  {row}")

    # Format as aligned table
    print("\nFormatted:")
    all_rows = [table_parser.headers] + table_parser.rows
    col_widths = [
        max(len(str(row[i])) for row in all_rows)
        for i in range(len(table_parser.headers))
    ]
    for j, row in enumerate(all_rows):
        formatted = "  ".join(
            str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
        )
        print(f"  {formatted}")
        if j == 0:
            print(f"  {'  '.join('-' * w for w in col_widths)}")
