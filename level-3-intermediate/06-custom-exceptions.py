"""
Custom Exceptions for Validation
==================================
Difficulty: 2/5
Estimated time: 15 minutes

Problem:
--------
Create a set of custom exception classes for common validation scenarios:
1. ValidationError (base class for all validation errors).
2. AgeValidationError - for invalid age values.
3. EmailValidationError - for invalid email formats.
4. PasswordValidationError - for weak passwords (with specific reason).
5. RangeError - for values outside an allowed range.

Then create validator functions that raise these exceptions, and demonstrate
catching and handling them with try/except.

Concepts practiced:
- Custom exception classes (inheriting from Exception)
- Exception hierarchy
- raise keyword
- try / except / else / finally
- Exception attributes and messages

Expected output (example):
--------------------------
# --- Age Validation ---
# Age 25: Valid
# Age -5: AgeValidationError - Age must be between 0 and 150, got -5
# Age 'abc': AgeValidationError - Age must be an integer, got str
#
# --- Email Validation ---
# user@example.com: Valid
# not-an-email: EmailValidationError - Missing '@' symbol
#
# --- Password Validation ---
# 'Str0ng!Pass': Valid
# 'short': PasswordValidationError - Password must be at least 8 characters
#
# --- Range Validation ---
# 50 in [0, 100]: Valid
# 150 in [0, 100]: RangeError - Value 150 out of range [0, 100]
"""

import re


# ---- Custom Exception Hierarchy ----

class ValidationError(Exception):
    """Base class for all validation errors."""

    def __init__(self, message, field=None):
        self.field = field
        self.message = message
        super().__init__(self.message)


class AgeValidationError(ValidationError):
    """Raised when an age value is invalid."""

    def __init__(self, message, value=None):
        self.value = value
        super().__init__(message, field="age")


class EmailValidationError(ValidationError):
    """Raised when an email format is invalid."""

    def __init__(self, message, email=None):
        self.email = email
        super().__init__(message, field="email")


class PasswordValidationError(ValidationError):
    """Raised when a password does not meet strength requirements."""

    def __init__(self, message, requirements_met=None):
        self.requirements_met = requirements_met or {}
        super().__init__(message, field="password")


class RangeError(ValidationError):
    """Raised when a value is outside the allowed range."""

    def __init__(self, value, min_val, max_val):
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        message = f"Value {value} out of range [{min_val}, {max_val}]"
        super().__init__(message, field="range")


# ---- Validator Functions ----

def validate_age(age):
    """
    Validate that age is an integer between 0 and 150.

    Parameters:
        age: Value to validate.

    Raises:
        AgeValidationError: If age is invalid.
    """
    if not isinstance(age, int):
        raise AgeValidationError(
            f"Age must be an integer, got {type(age).__name__}", value=age
        )
    if age < 0 or age > 150:
        raise AgeValidationError(
            f"Age must be between 0 and 150, got {age}", value=age
        )


def validate_email(email):
    """
    Validate an email address format.

    Parameters:
        email (str): Email to validate.

    Raises:
        EmailValidationError: If format is invalid.
    """
    if not isinstance(email, str):
        raise EmailValidationError("Email must be a string", email=email)
    if "@" not in email:
        raise EmailValidationError("Missing '@' symbol", email=email)
    if "." not in email.split("@")[-1]:
        raise EmailValidationError("Missing domain extension (e.g. .com)", email=email)
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise EmailValidationError(f"Invalid email format: '{email}'", email=email)


def validate_password(password):
    """
    Validate password strength. Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character

    Parameters:
        password (str): Password to validate.

    Raises:
        PasswordValidationError: If password is weak.
    """
    checks = {
        "min_length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }

    messages = {
        "min_length": "Password must be at least 8 characters",
        "uppercase": "Password must contain at least one uppercase letter",
        "lowercase": "Password must contain at least one lowercase letter",
        "digit": "Password must contain at least one digit",
        "special": "Password must contain at least one special character",
    }

    for check_name, passed in checks.items():
        if not passed:
            raise PasswordValidationError(messages[check_name], requirements_met=checks)


def validate_range(value, min_val, max_val):
    """
    Validate that a numeric value falls within a range.

    Parameters:
        value (int or float): Value to check.
        min_val: Minimum allowed value (inclusive).
        max_val: Maximum allowed value (inclusive).

    Raises:
        RangeError: If value is out of range.
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Expected numeric value, got {type(value).__name__}")
    if value < min_val or value > max_val:
        raise RangeError(value, min_val, max_val)


# ---- Demo helper ----

def run_validation(label, func, *args):
    """Run a validation function and print the result or error."""
    try:
        func(*args)
        print(f"  {label}: Valid")
    except ValidationError as e:
        print(f"  {label}: {type(e).__name__} - {e}")


if __name__ == "__main__":
    print("--- Age Validation ---")
    run_validation("Age 25", validate_age, 25)
    run_validation("Age -5", validate_age, -5)
    run_validation("Age 200", validate_age, 200)
    run_validation("Age 'abc'", validate_age, "abc")

    print("\n--- Email Validation ---")
    run_validation("user@example.com", validate_email, "user@example.com")
    run_validation("not-an-email", validate_email, "not-an-email")
    run_validation("user@nodot", validate_email, "user@nodot")
    run_validation("@example.com", validate_email, "@example.com")

    print("\n--- Password Validation ---")
    run_validation("'Str0ng!Pass'", validate_password, "Str0ng!Pass")
    run_validation("'short'", validate_password, "short")
    run_validation("'alllowercase1!'", validate_password, "alllowercase1!")
    run_validation("'ALLUPPERCASE1!'", validate_password, "ALLUPPERCASE1!")
    run_validation("'NoDigits!!'", validate_password, "NoDigits!!")
    run_validation("'NoSpecial1A'", validate_password, "NoSpecial1A")

    print("\n--- Range Validation ---")
    run_validation("50 in [0, 100]", validate_range, 50, 0, 100)
    run_validation("150 in [0, 100]", validate_range, 150, 0, 100)
    run_validation("-10 in [0, 100]", validate_range, -10, 0, 100)
    run_validation("0 in [0, 100]", validate_range, 0, 0, 100)

    # Demonstrate exception hierarchy
    print("\n--- Exception Hierarchy ---")
    print(f"AgeValidationError bases: {AgeValidationError.__bases__}")
    print(f"ValidationError bases: {ValidationError.__bases__}")

    try:
        validate_age(-1)
    except Exception as e:
        print(f"\nCaught as Exception: {e}")
        print(f"Is ValidationError? {isinstance(e, ValidationError)}")
        print(f"Is AgeValidationError? {isinstance(e, AgeValidationError)}")
        print(f"Field: {e.field}")

    # Demonstrate try/except/else/finally
    print("\n--- try/except/else/finally Demo ---")
    for test_age in [25, -1]:
        print(f"\nValidating age={test_age}:")
        try:
            validate_age(test_age)
        except AgeValidationError as e:
            print(f"  except: Caught {e}")
        else:
            print(f"  else: Age {test_age} is valid!")
        finally:
            print(f"  finally: Validation attempt complete.")
