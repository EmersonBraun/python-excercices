"""
Level 6 - Exercise 06: CLI Tool with argparse
===============================================

Difficulty: 3/5 stars
Estimated time: 20 minutes

Build a command-line tool with subcommands for file operations:
counting lines, searching text, and computing file statistics.

Uses only the Python standard library (argparse, os, pathlib).

Features
--------
- `count`  : Count lines, words, and characters in a file.
- `search` : Search for a pattern in a file (like simple grep).
- `stats`  : Show file metadata (size, modified date, etc.).
- `head`   : Show first N lines of a file.
- `tail`   : Show last N lines of a file.
- `tree`   : Show directory tree structure.

Usage:
    python3 06-cli-tool.py count myfile.txt
    python3 06-cli-tool.py search "pattern" myfile.txt --ignore-case
    python3 06-cli-tool.py stats myfile.txt
    python3 06-cli-tool.py head myfile.txt -n 5
    python3 06-cli-tool.py tree /some/directory --depth 2

Expected output:
----------------
    $ python3 06-cli-tool.py count sample.txt
    Lines:      42
    Words:      256
    Characters: 1,580

    $ python3 06-cli-tool.py search "def " sample.py
    sample.py:10: def hello():
    sample.py:15: def world():
    2 matches found
"""

import argparse
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Subcommand Implementations
# ---------------------------------------------------------------------------

def cmd_count(filepath: str, **kwargs) -> None:
    """Count lines, words, and characters in a file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    lines = content.count("\n")
    words = len(content.split())
    chars = len(content)

    print(f"File: {filepath}")
    print(f"  Lines:      {lines:,}")
    print(f"  Words:      {words:,}")
    print(f"  Characters: {chars:,}")


def cmd_search(filepath: str, pattern: str, ignore_case: bool = False,
               line_numbers: bool = True, count_only: bool = False,
               **kwargs) -> None:
    """Search for a pattern in a file (simple grep)."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    flags = re.IGNORECASE if ignore_case else 0
    matches = []

    for i, line in enumerate(lines, 1):
        if re.search(pattern, line, flags):
            matches.append((i, line.rstrip("\n")))

    if count_only:
        print(f"{len(matches)} matches found in {filepath}")
        return

    for lineno, text in matches:
        if line_numbers:
            print(f"  {filepath}:{lineno}: {text}")
        else:
            print(f"  {text}")
    print(f"\n{len(matches)} match(es) found.")


def cmd_stats(filepath: str, **kwargs) -> None:
    """Show file metadata and statistics."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    stat = path.stat()
    size = stat.st_size
    modified = datetime.fromtimestamp(stat.st_mtime)
    created = datetime.fromtimestamp(stat.st_ctime)

    # Human-readable size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            size_str = f"{size:.1f} {unit}"
            break
        size /= 1024
    else:
        size_str = f"{size:.1f} TB"

    print(f"File: {filepath}")
    print(f"  Type:        {'directory' if path.is_dir() else path.suffix or 'file'}")
    print(f"  Size:        {size_str} ({stat.st_size:,} bytes)")
    print(f"  Modified:    {modified:%Y-%m-%d %H:%M:%S}")
    print(f"  Created:     {created:%Y-%m-%d %H:%M:%S}")
    print(f"  Permissions: {oct(stat.st_mode)[-3:]}")
    print(f"  Absolute:    {path.resolve()}")

    if path.is_file():
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        print(f"  Lines:       {content.count(chr(10)):,}")
        print(f"  Words:       {len(content.split()):,}")


def cmd_head(filepath: str, n: int = 10, **kwargs) -> None:
    """Show first N lines of a file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i >= n:
                    break
                print(line.rstrip("\n"))
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)


def cmd_tail(filepath: str, n: int = 10, **kwargs) -> None:
    """Show last N lines of a file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    for line in lines[-n:]:
        print(line.rstrip("\n"))


def cmd_tree(directory: str, depth: int = 3, _prefix: str = "",
             _current_depth: int = 0, **kwargs) -> None:
    """Show directory tree structure."""
    path = Path(directory)
    if not path.is_dir():
        print(f"Error: Not a directory: {directory}")
        sys.exit(1)

    if _current_depth == 0:
        print(f"{path.name}/")

    if _current_depth >= depth:
        return

    try:
        entries = sorted(path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        print(f"{_prefix}[Permission denied]")
        return

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "--- " if is_last else "|-- "
        child_prefix = "    " if is_last else "|   "

        if entry.is_dir():
            print(f"{_prefix}{connector}{entry.name}/")
            cmd_tree(
                str(entry),
                depth=depth,
                _prefix=_prefix + child_prefix,
                _current_depth=_current_depth + 1,
            )
        else:
            size = entry.stat().st_size
            print(f"{_prefix}{connector}{entry.name}  ({size:,} bytes)")


# ---------------------------------------------------------------------------
# CLI Setup
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="filetool",
        description="CLI tool for file operations: count, search, stats, etc.",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # count
    p_count = sub.add_parser("count", help="Count lines, words, characters")
    p_count.add_argument("filepath", help="Path to the file")

    # search
    p_search = sub.add_parser("search", help="Search for a pattern (regex)")
    p_search.add_argument("pattern", help="Regex pattern to search for")
    p_search.add_argument("filepath", help="Path to the file")
    p_search.add_argument("-i", "--ignore-case", action="store_true",
                          help="Case-insensitive search")
    p_search.add_argument("-c", "--count-only", action="store_true",
                          help="Only print match count")

    # stats
    p_stats = sub.add_parser("stats", help="Show file metadata")
    p_stats.add_argument("filepath", help="Path to the file")

    # head
    p_head = sub.add_parser("head", help="Show first N lines")
    p_head.add_argument("filepath", help="Path to the file")
    p_head.add_argument("-n", type=int, default=10, help="Number of lines (default: 10)")

    # tail
    p_tail = sub.add_parser("tail", help="Show last N lines")
    p_tail.add_argument("filepath", help="Path to the file")
    p_tail.add_argument("-n", type=int, default=10, help="Number of lines (default: 10)")

    # tree
    p_tree = sub.add_parser("tree", help="Show directory tree")
    p_tree.add_argument("directory", nargs="?", default=".",
                        help="Directory to display (default: current)")
    p_tree.add_argument("--depth", type=int, default=3,
                        help="Max depth (default: 3)")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    commands = {
        "count": cmd_count,
        "search": cmd_search,
        "stats": cmd_stats,
        "head": cmd_head,
        "tail": cmd_tail,
        "tree": cmd_tree,
    }

    if args.command in commands:
        commands[args.command](**vars(args))
    else:
        parser.print_help()


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No command provided. Running interactive demo...\n")

        # Create a sample file for demonstration
        sample_content = """#!/usr/bin/env python3
\"\"\"Sample Python file for CLI tool demo.\"\"\"

import os
import sys

def hello(name):
    \"\"\"Greet someone.\"\"\"
    print(f"Hello, {name}!")

def goodbye(name):
    \"\"\"Say goodbye.\"\"\"
    print(f"Goodbye, {name}!")

def main():
    hello("World")
    goodbye("World")

if __name__ == "__main__":
    main()
"""
        fd, sample_path = tempfile.mkstemp(suffix=".py", prefix="sample_")
        with os.fdopen(fd, "w") as f:
            f.write(sample_content)

        try:
            print("=" * 60)
            print("1. COUNT - Line/word/character counts")
            print("=" * 60)
            cmd_count(sample_path)
            print()

            print("=" * 60)
            print('2. SEARCH - Find "def " in the file')
            print("=" * 60)
            cmd_search(sample_path, pattern=r"def \w+")
            print()

            print("=" * 60)
            print("3. STATS - File metadata")
            print("=" * 60)
            cmd_stats(sample_path)
            print()

            print("=" * 60)
            print("4. HEAD - First 5 lines")
            print("=" * 60)
            cmd_head(sample_path, n=5)
            print()

            print("=" * 60)
            print("5. TAIL - Last 5 lines")
            print("=" * 60)
            cmd_tail(sample_path, n=5)
            print()

            print("=" * 60)
            print("6. TREE - Current directory (depth 1)")
            print("=" * 60)
            cmd_tree(os.path.dirname(sample_path) or ".", depth=1)

        finally:
            os.unlink(sample_path)
    else:
        main()
