"""
Exercise 05 - Number Guessing Game
====================================
Level: 1 - Foundations
Difficulty: 2/5
Estimated Time: 15 minutes

Problem:
--------
Create a number guessing game where:
  1. The computer picks a random number in a given range.
  2. The player guesses the number.
  3. After each guess, the game provides hints ('Too high!' / 'Too low!').
  4. Track the number of attempts.
  5. Provide a score based on how quickly the number was guessed.

Expected Input/Output:
----------------------
# game = GuessingGame(1, 100)  # range 1-100
# game.check_guess(50)  -> "Too high!" or "Too low!" or "Correct!"
# game.attempts         -> number of guesses made
# game.is_over          -> True if correctly guessed

# auto_play demo runs a non-interactive simulation
"""

import random


class GuessingGame:
    """A number guessing game with configurable range and hints."""

    def __init__(self, low: int = 1, high: int = 100, secret: int = None):
        """
        Initialize the guessing game.

        Args:
            low: Lower bound of the range (inclusive).
            high: Upper bound of the range (inclusive).
            secret: Optional fixed secret number (for testing). If None, picked randomly.
        """
        self.low = low
        self.high = high
        self.secret = secret if secret is not None else random.randint(low, high)
        self.attempts = 0
        self.max_attempts = None
        self.is_over = False
        self.guesses = []

    def check_guess(self, guess: int) -> str:
        """
        Check a guess against the secret number.

        Args:
            guess: The player's guess.

        Returns:
            A hint string: 'Too low!', 'Too high!', or 'Correct! You got it in N attempts!'
        """
        if self.is_over:
            return "Game is already over. Start a new game."

        self.attempts += 1
        self.guesses.append(guess)

        if guess < self.secret:
            return "Too low!"
        elif guess > self.secret:
            return "Too high!"
        else:
            self.is_over = True
            return f"Correct! You got it in {self.attempts} attempt(s)!"

    def get_score(self) -> str:
        """
        Return a score based on the number of attempts for a 1-100 range.

        Returns:
            A string with the score rating.
        """
        if not self.is_over:
            return "Game not finished yet."

        range_size = self.high - self.low + 1
        optimal = len(bin(range_size)) - 2  # log2 approximation

        if self.attempts <= optimal:
            return f"Excellent! {self.attempts} attempts (optimal is ~{optimal})"
        elif self.attempts <= optimal + 3:
            return f"Good job! {self.attempts} attempts"
        elif self.attempts <= optimal + 7:
            return f"Not bad! {self.attempts} attempts"
        else:
            return f"Keep practicing! {self.attempts} attempts"


def auto_play(low: int = 1, high: int = 100, secret: int = None) -> list:
    """
    Simulate a game using binary search strategy (optimal play).

    Args:
        low: Lower bound of the range.
        high: Upper bound of the range.
        secret: Optional fixed secret number.

    Returns:
        List of (guess, hint) tuples showing the game progression.
    """
    game = GuessingGame(low, high, secret)
    current_low = low
    current_high = high
    log = []

    while not game.is_over:
        guess = (current_low + current_high) // 2
        hint = game.check_guess(guess)
        log.append((guess, hint))

        if "Too low" in hint:
            current_low = guess + 1
        elif "Too high" in hint:
            current_high = guess - 1

    return log


def interactive_game():
    """Run an interactive guessing game in the terminal."""
    print("\nI'm thinking of a number between 1 and 100.")
    print("Can you guess it?\n")

    game = GuessingGame(1, 100)

    while not game.is_over:
        try:
            guess = int(input("Your guess: "))
            hint = game.check_guess(guess)
            print(f"  -> {hint}")
        except ValueError:
            print("  -> Please enter a valid integer.")

    print(game.get_score())


if __name__ == "__main__":
    print("=" * 40)
    print("  Number Guessing Game Demo")
    print("=" * 40)

    # Auto-play simulation (non-interactive)
    print("\n--- Auto-Play Simulation (Binary Search) ---")
    print("Secret number: 73, Range: 1-100\n")

    log = auto_play(1, 100, secret=73)
    for i, (guess, hint) in enumerate(log, 1):
        print(f"  Attempt {i}: Guessed {guess:>3} -> {hint}")

    # Another simulation
    print("\n--- Auto-Play Simulation #2 ---")
    print("Secret number: 7, Range: 1-50\n")

    log = auto_play(1, 50, secret=7)
    for i, (guess, hint) in enumerate(log, 1):
        print(f"  Attempt {i}: Guessed {guess:>3} -> {hint}")

    # Manual game test
    print("\n--- Manual Game Test ---")
    game = GuessingGame(1, 10, secret=7)
    test_guesses = [5, 8, 6, 7]
    for guess in test_guesses:
        result = game.check_guess(guess)
        print(f"  Guess {guess}: {result}")
    print(f"  Score: {game.get_score()}")
    print(f"  Guesses made: {game.guesses}")

    # Uncomment the line below to play interactively:
    # interactive_game()

    print("\nGuessing game exercise complete!")
