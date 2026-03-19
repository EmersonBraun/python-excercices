def test_bank_account():
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def deposit(self, amount):
            self.balance += amount

        def withdraw(self, amount):
            if amount > self.balance:
                raise ValueError("Insufficient funds")
            self.balance -= amount

    acc = BankAccount("Alice", 100)
    acc.deposit(50)
    assert acc.balance == 150
    acc.withdraw(30)
    assert acc.balance == 120


def test_bank_account_insufficient_funds():
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def withdraw(self, amount):
            if amount > self.balance:
                raise ValueError("Insufficient funds")
            self.balance -= amount

    import pytest
    acc = BankAccount("Bob", 50)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acc.withdraw(100)


def test_custom_exception():
    class ValidationError(Exception):
        def __init__(self, field, message):
            self.field = field
            super().__init__(message)

    try:
        raise ValidationError("email", "Invalid format")
    except ValidationError as e:
        assert e.field == "email"
        assert str(e) == "Invalid format"
