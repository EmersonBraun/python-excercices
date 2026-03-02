"""
CSV Reader & Writer
====================
Difficulty: 2/5
Estimated time: 15 minutes

Problem:
--------
Create functions to work with CSV files:
1. Generate sample CSV data (a list of employee records).
2. Write that data to a CSV file using the csv module.
3. Read the CSV file back and display the contents in a formatted table.
4. Provide a function to filter rows by a given column value.

Concepts practiced:
- csv module (reader, writer, DictReader, DictWriter)
- File I/O (open, with statement)
- String formatting

Expected output (example):
--------------------------
# Writing sample data to employees.csv ...
# Done! Wrote 5 records.
#
# --- All Employees ---
# Name             | Department   | Salary
# -----------------------------------------
# Alice Johnson    | Engineering  | 95000
# Bob Smith        | Marketing    | 72000
# Carol White      | Engineering  | 98000
# David Brown      | Sales        | 68000
# Eve Davis        | Marketing    | 75000
#
# --- Filtered: Department = Engineering ---
# Alice Johnson    | Engineering  | 95000
# Carol White      | Engineering  | 98000
"""

import csv
import os


def generate_sample_data():
    """Return a list of dictionaries representing employee records."""
    return [
        {"name": "Alice Johnson", "department": "Engineering", "salary": 95000},
        {"name": "Bob Smith", "department": "Marketing", "salary": 72000},
        {"name": "Carol White", "department": "Engineering", "salary": 98000},
        {"name": "David Brown", "department": "Sales", "salary": 68000},
        {"name": "Eve Davis", "department": "Marketing", "salary": 75000},
    ]


def write_csv(filepath, data):
    """
    Write a list of dictionaries to a CSV file.

    Parameters:
        filepath (str): Path to the output CSV file.
        data (list[dict]): Rows to write. Keys of the first dict are used as headers.

    Returns:
        int: Number of rows written (excluding the header).
    """
    if not data:
        return 0

    fieldnames = list(data[0].keys())

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return len(data)


def read_csv(filepath):
    """
    Read a CSV file and return its contents as a list of dictionaries.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        list[dict]: Rows from the CSV file.
    """
    with open(filepath, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def display_table(records, title="Records"):
    """Print records in a formatted table."""
    if not records:
        print(f"--- {title} ---")
        print("(no records)")
        return

    headers = list(records[0].keys())
    col_widths = {}
    for h in headers:
        col_widths[h] = max(len(h), max(len(str(row[h])) for row in records))

    header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
    separator = "-" * len(header_line)

    print(f"\n--- {title} ---")
    print(header_line)
    print(separator)
    for row in records:
        print(" | ".join(str(row[h]).ljust(col_widths[h]) for h in headers))


def filter_by_column(records, column, value):
    """
    Filter records where the given column matches the value (case-insensitive).

    Parameters:
        records (list[dict]): The data rows.
        column (str): Column name to filter on.
        value (str): Value to match.

    Returns:
        list[dict]: Filtered rows.
    """
    return [
        row for row in records
        if str(row.get(column, "")).lower() == str(value).lower()
    ]


if __name__ == "__main__":
    csv_path = "employees.csv"

    # Generate and write
    data = generate_sample_data()
    print(f"Writing sample data to {csv_path} ...")
    count = write_csv(csv_path, data)
    print(f"Done! Wrote {count} records.")

    # Read and display
    records = read_csv(csv_path)
    display_table(records, title="All Employees")

    # Filter
    engineering = filter_by_column(records, "department", "Engineering")
    display_table(engineering, title="Filtered: Department = Engineering")

    # Cleanup the generated file
    os.remove(csv_path)
    print(f"\nCleaned up {csv_path}.")
