"""
Level 6 - Exercise 03: SQLite Task Manager
============================================

Difficulty: 3/5 stars
Estimated time: 25 minutes

Build a task manager backed by an SQLite database.  Supports full CRUD
operations, priorities, due dates, and a CLI interface.

Uses only the Python standard library (sqlite3, argparse).

Features
--------
- Create, read, update, delete tasks.
- Priority levels: low, medium, high, critical.
- Due dates with overdue detection.
- Filter by status, priority, or due date.
- Persistent storage in a local SQLite file.

Usage:
    python3 03-sqlite-task-manager.py add "Buy groceries" --priority high --due 2025-04-01
    python3 03-sqlite-task-manager.py list
    python3 03-sqlite-task-manager.py done 1
    python3 03-sqlite-task-manager.py delete 1

Expected output:
----------------
    ID  | Status | Priority | Due        | Task
    ----|--------|----------|------------|---------------------
     1  | [ ]    | high     | 2025-04-01 | Buy groceries
     2  | [x]    | medium   | None       | Write Python exercise
"""

import argparse
import sqlite3
import sys
from datetime import datetime, date


# ---------------------------------------------------------------------------
# Database Layer
# ---------------------------------------------------------------------------
class TaskDB:
    """SQLite-backed task storage.

    Creates the table on first use.  All public methods are self-contained
    transactions.
    """

    PRIORITIES = ("low", "medium", "high", "critical")

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                description TEXT    DEFAULT '',
                priority    TEXT    DEFAULT 'medium',
                due_date    TEXT,
                done        INTEGER DEFAULT 0,
                created_at  TEXT    DEFAULT (datetime('now')),
                updated_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        self.conn.commit()

    # -- CRUD ---------------------------------------------------------------

    def add(self, title: str, description: str = "",
            priority: str = "medium", due_date: str | None = None) -> int:
        """Insert a new task. Returns the new task ID."""
        if priority not in self.PRIORITIES:
            raise ValueError(f"priority must be one of {self.PRIORITIES}")
        if due_date:
            # Validate date format
            datetime.strptime(due_date, "%Y-%m-%d")
        cur = self.conn.execute(
            "INSERT INTO tasks (title, description, priority, due_date) "
            "VALUES (?, ?, ?, ?)",
            (title, description, priority, due_date),
        )
        self.conn.commit()
        return cur.lastrowid

    def get(self, task_id: int) -> dict | None:
        """Fetch a single task by ID."""
        row = self.conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None

    def list_all(self, status: str | None = None,
                 priority: str | None = None,
                 overdue_only: bool = False) -> list[dict]:
        """Return tasks with optional filters."""
        query = "SELECT * FROM tasks WHERE 1=1"
        params: list = []

        if status == "done":
            query += " AND done = 1"
        elif status == "pending":
            query += " AND done = 0"

        if priority:
            query += " AND priority = ?"
            params.append(priority)

        if overdue_only:
            today = date.today().isoformat()
            query += " AND due_date IS NOT NULL AND due_date < ? AND done = 0"
            params.append(today)

        query += " ORDER BY done ASC, due_date ASC NULLS LAST, id ASC"
        rows = self.conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def mark_done(self, task_id: int) -> bool:
        """Mark a task as done. Returns True if the task existed."""
        cur = self.conn.execute(
            "UPDATE tasks SET done = 1, updated_at = datetime('now') "
            "WHERE id = ?", (task_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def mark_undone(self, task_id: int) -> bool:
        """Mark a task as not done."""
        cur = self.conn.execute(
            "UPDATE tasks SET done = 0, updated_at = datetime('now') "
            "WHERE id = ?", (task_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def update(self, task_id: int, **kwargs) -> bool:
        """Update one or more fields of a task."""
        allowed = {"title", "description", "priority", "due_date"}
        fields = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not fields:
            return False
        if "priority" in fields and fields["priority"] not in self.PRIORITIES:
            raise ValueError(f"priority must be one of {self.PRIORITIES}")
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [task_id]
        cur = self.conn.execute(
            f"UPDATE tasks SET {set_clause}, updated_at = datetime('now') "
            f"WHERE id = ?", values,
        )
        self.conn.commit()
        return cur.rowcount > 0

    def delete(self, task_id: int) -> bool:
        """Delete a task. Returns True if it existed."""
        cur = self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def stats(self) -> dict:
        """Return summary statistics."""
        total = self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        done = self.conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE done = 1"
        ).fetchone()[0]
        today = date.today().isoformat()
        overdue = self.conn.execute(
            "SELECT COUNT(*) FROM tasks "
            "WHERE due_date IS NOT NULL AND due_date < ? AND done = 0",
            (today,),
        ).fetchone()[0]
        return {"total": total, "done": done, "pending": total - done, "overdue": overdue}

    def close(self):
        self.conn.close()


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------
def format_task_table(tasks: list[dict]) -> str:
    """Format tasks as a text table."""
    if not tasks:
        return "  (no tasks found)"

    today = date.today().isoformat()
    lines = []
    header = f"{'ID':>4}  {'Status':<8} {'Priority':<10} {'Due':<12} {'Title'}"
    lines.append(header)
    lines.append("-" * len(header))

    for t in tasks:
        status = "[x]" if t["done"] else "[ ]"
        due = t["due_date"] or "-"
        overdue = ""
        if not t["done"] and t["due_date"] and t["due_date"] < today:
            overdue = " OVERDUE!"
        lines.append(
            f"{t['id']:>4}  {status:<8} {t['priority']:<10} {due:<12} "
            f"{t['title']}{overdue}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SQLite Task Manager")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # add
    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task title")
    add_p.add_argument("--desc", default="", help="Description")
    add_p.add_argument("--priority", default="medium",
                       choices=TaskDB.PRIORITIES, help="Priority level")
    add_p.add_argument("--due", default=None, help="Due date (YYYY-MM-DD)")

    # list
    list_p = sub.add_parser("list", help="List tasks")
    list_p.add_argument("--status", choices=["done", "pending"])
    list_p.add_argument("--priority", choices=TaskDB.PRIORITIES)
    list_p.add_argument("--overdue", action="store_true")

    # done
    done_p = sub.add_parser("done", help="Mark task as done")
    done_p.add_argument("id", type=int, help="Task ID")

    # undone
    undone_p = sub.add_parser("undone", help="Mark task as not done")
    undone_p.add_argument("id", type=int, help="Task ID")

    # update
    upd_p = sub.add_parser("update", help="Update a task")
    upd_p.add_argument("id", type=int, help="Task ID")
    upd_p.add_argument("--title")
    upd_p.add_argument("--desc")
    upd_p.add_argument("--priority", choices=TaskDB.PRIORITIES)
    upd_p.add_argument("--due")

    # delete
    del_p = sub.add_parser("delete", help="Delete a task")
    del_p.add_argument("id", type=int, help="Task ID")

    # stats
    sub.add_parser("stats", help="Show summary statistics")

    return parser


def run_cli(argv=None, db_path=":memory:"):
    parser = build_parser()
    args = parser.parse_args(argv)
    db = TaskDB(db_path)

    try:
        if args.command == "add":
            tid = db.add(args.title, args.desc, args.priority, args.due)
            print(f"Task #{tid} created.")

        elif args.command == "list":
            tasks = db.list_all(
                status=args.status,
                priority=args.priority,
                overdue_only=args.overdue,
            )
            print(format_task_table(tasks))

        elif args.command == "done":
            if db.mark_done(args.id):
                print(f"Task #{args.id} marked as done.")
            else:
                print(f"Task #{args.id} not found.")

        elif args.command == "undone":
            if db.mark_undone(args.id):
                print(f"Task #{args.id} marked as pending.")
            else:
                print(f"Task #{args.id} not found.")

        elif args.command == "update":
            if db.update(args.id, title=args.title, description=args.desc,
                         priority=args.priority, due_date=args.due):
                print(f"Task #{args.id} updated.")
            else:
                print(f"Task #{args.id} not found or no changes.")

        elif args.command == "delete":
            if db.delete(args.id):
                print(f"Task #{args.id} deleted.")
            else:
                print(f"Task #{args.id} not found.")

        elif args.command == "stats":
            s = db.stats()
            print(f"Total: {s['total']}  |  Done: {s['done']}  |  "
                  f"Pending: {s['pending']}  |  Overdue: {s['overdue']}")

        else:
            parser.print_help()
    finally:
        db.close()


# ===================================================================
# Demo / self-test  (uses in-memory DB)
# ===================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No command provided. Running interactive demo...\n")
        db = TaskDB(":memory:")

        # Populate with sample tasks
        db.add("Buy groceries", priority="high", due_date="2025-03-15")
        db.add("Write Python exercises", priority="medium", due_date="2025-04-01")
        db.add("Call dentist", priority="low", due_date="2025-01-01")  # overdue
        db.add("Review pull request", priority="critical")
        db.add("Clean apartment", priority="medium", due_date="2025-03-20")

        # Mark one as done
        db.mark_done(2)

        print("=" * 60)
        print("All Tasks")
        print("=" * 60)
        print(format_task_table(db.list_all()))
        print()

        print("=" * 60)
        print("Pending Tasks Only")
        print("=" * 60)
        print(format_task_table(db.list_all(status="pending")))
        print()

        print("=" * 60)
        print("Overdue Tasks")
        print("=" * 60)
        print(format_task_table(db.list_all(overdue_only=True)))
        print()

        print("=" * 60)
        print("High Priority Tasks")
        print("=" * 60)
        print(format_task_table(db.list_all(priority="high")))
        print()

        print("=" * 60)
        print("Statistics")
        print("=" * 60)
        s = db.stats()
        print(f"Total: {s['total']}  |  Done: {s['done']}  |  "
              f"Pending: {s['pending']}  |  Overdue: {s['overdue']}")
        print()

        # Update demo
        print("=" * 60)
        print("Update Task #1")
        print("=" * 60)
        db.update(1, title="Buy organic groceries", priority="critical")
        task = db.get(1)
        print(f"Updated: {task['title']} (priority: {task['priority']})")
        print()

        # Delete demo
        print("=" * 60)
        print("Delete Task #3")
        print("=" * 60)
        db.delete(3)
        print(format_task_table(db.list_all()))

        db.close()
    else:
        run_cli()
