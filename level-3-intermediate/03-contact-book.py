"""
Contact Book with File Persistence
====================================
Difficulty: 3/5
Estimated time: 30 minutes

Problem:
--------
Build a contact book application that supports full CRUD operations:
1. Add a contact (name, phone, email).
2. View all contacts.
3. Search contacts by name (partial match).
4. Update a contact's phone or email.
5. Delete a contact.
6. Persist contacts to a JSON file so they survive across runs.

Concepts practiced:
- JSON file persistence
- CRUD operations
- Dictionary manipulation
- Input validation
- Search / filtering

Expected output (example):
--------------------------
# --- Contact Book Demo ---
# Added: Alice Johnson
# Added: Bob Smith
# Added: Carol White
#
# All contacts (3):
#   1. Alice Johnson  | 555-0101 | alice@example.com
#   2. Bob Smith      | 555-0202 | bob@example.com
#   3. Carol White    | 555-0303 | carol@example.com
#
# Search 'ali':
#   1. Alice Johnson  | 555-0101 | alice@example.com
#
# Updated Alice Johnson's email to alice.j@newmail.com
# Deleted Bob Smith
#
# All contacts (2):
#   1. Alice Johnson  | 555-0101 | alice.j@newmail.com
#   2. Carol White    | 555-0303 | carol@example.com
"""

import json
import os
import re


class ContactBook:
    """A contact book with JSON file persistence."""

    def __init__(self, filepath="contacts.json"):
        """
        Initialize the contact book.

        Parameters:
            filepath (str): Path to the JSON file for persistence.
        """
        self.filepath = filepath
        self.contacts = []
        self._load()

    # ---- Persistence ----

    def _load(self):
        """Load contacts from the JSON file if it exists."""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.contacts = json.load(f)

    def _save(self):
        """Save contacts to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, indent=2)

    # ---- Validation helpers ----

    @staticmethod
    def _validate_email(email):
        """Return True if the email looks valid."""
        pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def _validate_phone(phone):
        """Return True if the phone contains only digits, dashes, spaces, or parentheses."""
        pattern = r"^[\d\s\-\(\)\+]+$"
        return re.match(pattern, phone) is not None

    # ---- CRUD ----

    def add(self, name, phone, email):
        """
        Add a new contact.

        Parameters:
            name (str): Full name.
            phone (str): Phone number.
            email (str): Email address.

        Returns:
            bool: True if added, False if validation failed or duplicate name.
        """
        if not name.strip():
            print("Error: Name cannot be empty.")
            return False
        if not self._validate_phone(phone):
            print(f"Error: Invalid phone number '{phone}'.")
            return False
        if not self._validate_email(email):
            print(f"Error: Invalid email '{email}'.")
            return False

        # Check for duplicate name
        if any(c["name"].lower() == name.lower() for c in self.contacts):
            print(f"Error: Contact '{name}' already exists.")
            return False

        self.contacts.append({
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        })
        self._save()
        print(f"Added: {name}")
        return True

    def list_all(self):
        """Display all contacts."""
        if not self.contacts:
            print("Contact book is empty.")
            return

        print(f"\nAll contacts ({len(self.contacts)}):")
        for i, c in enumerate(self.contacts, start=1):
            print(f"  {i}. {c['name']:18s} | {c['phone']:12s} | {c['email']}")

    def search(self, query):
        """
        Search contacts by name (case-insensitive partial match).

        Parameters:
            query (str): Search string.

        Returns:
            list[dict]: Matching contacts.
        """
        results = [
            c for c in self.contacts
            if query.lower() in c["name"].lower()
        ]
        print(f"\nSearch '{query}':")
        if results:
            for i, c in enumerate(results, start=1):
                print(f"  {i}. {c['name']:18s} | {c['phone']:12s} | {c['email']}")
        else:
            print("  No contacts found.")
        return results

    def update(self, name, phone=None, email=None):
        """
        Update a contact's phone and/or email.

        Parameters:
            name (str): Name of the contact to update.
            phone (str, optional): New phone number.
            email (str, optional): New email address.

        Returns:
            bool: True if updated, False if not found or validation failed.
        """
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                if phone is not None:
                    if not self._validate_phone(phone):
                        print(f"Error: Invalid phone number '{phone}'.")
                        return False
                    contact["phone"] = phone.strip()
                if email is not None:
                    if not self._validate_email(email):
                        print(f"Error: Invalid email '{email}'.")
                        return False
                    contact["email"] = email.strip()
                self._save()
                updates = []
                if phone is not None:
                    updates.append(f"phone to {phone}")
                if email is not None:
                    updates.append(f"email to {email}")
                print(f"Updated {contact['name']}'s {' and '.join(updates)}")
                return True

        print(f"Error: Contact '{name}' not found.")
        return False

    def delete(self, name):
        """
        Delete a contact by name.

        Parameters:
            name (str): Name of the contact to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        for i, contact in enumerate(self.contacts):
            if contact["name"].lower() == name.lower():
                self.contacts.pop(i)
                self._save()
                print(f"Deleted {name}")
                return True

        print(f"Error: Contact '{name}' not found.")
        return False

    def cleanup(self):
        """Remove the persistence file (for demo/testing)."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


if __name__ == "__main__":
    print("--- Contact Book Demo ---")

    book = ContactBook("demo_contacts.json")

    # Add contacts
    book.add("Alice Johnson", "555-0101", "alice@example.com")
    book.add("Bob Smith", "555-0202", "bob@example.com")
    book.add("Carol White", "555-0303", "carol@example.com")

    # List all
    book.list_all()

    # Search
    book.search("ali")

    # Update
    book.update("Alice Johnson", email="alice.j@newmail.com")

    # Delete
    book.delete("Bob Smith")

    # Final listing
    book.list_all()

    # Test validation
    print("\n--- Validation Tests ---")
    book.add("", "123", "bad")            # empty name
    book.add("Test", "abc", "t@t.com")    # invalid phone
    book.add("Test", "555-0000", "bad")   # invalid email
    book.add("Alice Johnson", "555-9999", "dupe@test.com")  # duplicate

    # Cleanup
    book.cleanup()
    print("\nCleaned up demo file.")
