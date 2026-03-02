"""
Bank Account System
====================
Difficulty: 3/5
Estimated time: 25 minutes

Problem:
--------
Create a BankAccount class that supports:
1. Deposit money (with validation).
2. Withdraw money (with overdraft protection).
3. Transfer money between accounts.
4. Print a statement showing all transactions.
5. Track balance and transaction history.

Concepts practiced:
- Classes and encapsulation
- Instance methods and properties
- Input validation and error handling
- Transaction history tracking
- String formatting

Expected output (example):
--------------------------
# Account A-001 (Alice) created with balance $1000.00
# Account A-002 (Bob) created with balance $500.00
#
# Alice deposits $250.00 -> Balance: $1250.00
# Alice withdraws $100.00 -> Balance: $1150.00
# Alice transfers $300.00 to Bob
#
# === Statement for A-001 (Alice) ===
# Date                | Type       | Amount     | Balance
# --------------------------------------------------------
# 2024-01-15 10:00:00 | DEPOSIT    | +$250.00   | $1250.00
# 2024-01-15 10:00:00 | WITHDRAWAL | -$100.00   | $1150.00
# 2024-01-15 10:00:00 | TRANSFER   | -$300.00   | $850.00
# --------------------------------------------------------
# Current balance: $850.00
"""

from datetime import datetime


class BankAccount:
    """A bank account with transaction tracking."""

    def __init__(self, account_id, owner, balance=0.0):
        """
        Initialize a bank account.

        Parameters:
            account_id (str): Unique account identifier.
            owner (str): Account owner's name.
            balance (float): Initial balance (must be >= 0).
        """
        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.account_id = account_id
        self.owner = owner
        self._balance = float(balance)
        self._transactions = []

        if balance > 0:
            self._record("OPENING", balance)

        print(f"Account {account_id} ({owner}) created with balance ${balance:.2f}")

    @property
    def balance(self):
        """Return the current balance."""
        return self._balance

    def _record(self, trans_type, amount):
        """Record a transaction in the history."""
        self._transactions.append({
            "date": datetime.now(),
            "type": trans_type,
            "amount": amount,
            "balance": self._balance,
        })

    def deposit(self, amount):
        """
        Deposit money into the account.

        Parameters:
            amount (float): Amount to deposit (must be > 0).

        Returns:
            float: New balance.

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self._balance += amount
        self._record("DEPOSIT", amount)
        print(f"{self.owner} deposits ${amount:.2f} -> Balance: ${self._balance:.2f}")
        return self._balance

    def withdraw(self, amount):
        """
        Withdraw money from the account.

        Parameters:
            amount (float): Amount to withdraw (must be > 0).

        Returns:
            float: New balance.

        Raises:
            ValueError: If amount is not positive or exceeds balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds. Balance: ${self._balance:.2f}, "
                f"requested: ${amount:.2f}"
            )

        self._balance -= amount
        self._record("WITHDRAWAL", -amount)
        print(f"{self.owner} withdraws ${amount:.2f} -> Balance: ${self._balance:.2f}")
        return self._balance

    def transfer(self, other, amount):
        """
        Transfer money to another account.

        Parameters:
            other (BankAccount): Destination account.
            amount (float): Amount to transfer.

        Returns:
            tuple: (sender_balance, receiver_balance)
        """
        if not isinstance(other, BankAccount):
            raise TypeError("Can only transfer to another BankAccount.")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds. Balance: ${self._balance:.2f}, "
                f"requested: ${amount:.2f}"
            )

        self._balance -= amount
        self._record("TRANSFER_OUT", -amount)

        other._balance += amount
        other._record("TRANSFER_IN", amount)

        print(f"{self.owner} transfers ${amount:.2f} to {other.owner}")
        return self._balance, other._balance

    def statement(self):
        """Print a formatted account statement."""
        header = f"Statement for {self.account_id} ({self.owner})"
        print(f"\n{'=' * 3} {header} {'=' * 3}")
        print(f"{'Date':22s}| {'Type':14s}| {'Amount':12s}| {'Balance':>10s}")
        print("-" * 64)

        for t in self._transactions:
            date_str = t["date"].strftime("%Y-%m-%d %H:%M:%S")
            amt = t["amount"]
            sign = "+" if amt >= 0 else ""
            print(
                f"{date_str:22s}| {t['type']:14s}| "
                f"{sign}${abs(amt):<10.2f}| ${t['balance']:>9.2f}"
            )

        print("-" * 64)
        print(f"Current balance: ${self._balance:.2f}\n")

    def __repr__(self):
        return f"BankAccount({self.account_id!r}, {self.owner!r}, balance={self._balance:.2f})"


if __name__ == "__main__":
    print("--- Bank Account Demo ---\n")

    # Create accounts
    alice = BankAccount("A-001", "Alice", 1000.00)
    bob = BankAccount("A-002", "Bob", 500.00)
    print()

    # Deposit and withdraw
    alice.deposit(250.00)
    alice.withdraw(100.00)
    print()

    # Transfer
    alice.transfer(bob, 300.00)

    # Statements
    alice.statement()
    bob.statement()

    # Error handling demos
    print("--- Error Handling ---")
    try:
        alice.withdraw(5000)
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        alice.deposit(-100)
    except ValueError as e:
        print(f"Caught: {e}")

    try:
        alice.transfer(bob, 999999)
    except ValueError as e:
        print(f"Caught: {e}")

    print(f"\nFinal balances: Alice=${alice.balance:.2f}, Bob=${bob.balance:.2f}")
