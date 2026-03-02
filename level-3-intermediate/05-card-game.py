"""
Card Deck Simulation
=====================
Difficulty: 3/5
Estimated time: 25 minutes

Problem:
--------
Simulate a standard 52-card deck:
1. Card class representing a single playing card (suit + rank).
2. Deck class that creates a full 52-card deck, shuffles, and deals cards.
3. Deal hands to multiple players.
4. Compare two cards (by rank value).
5. Play a simple "War" round between two hands.

Concepts practiced:
- Classes (Card, Deck)
- Operator overloading (__lt__, __eq__, __repr__)
- Random module (shuffle)
- List operations
- Enum-like constants

Expected output (example):
--------------------------
# Deck created with 52 cards.
# Deck shuffled.
#
# Dealt 5 cards to Player 1: [Q of Hearts, 3 of Spades, ...]
# Dealt 5 cards to Player 2: [K of Diamonds, 7 of Clubs, ...]
# Cards remaining in deck: 42
#
# --- War Round ---
# Player 1 plays: Q of Hearts (value 12)
# Player 2 plays: K of Diamonds (value 13)
# Player 2 wins this round!
#
# --- Hand Evaluation ---
# Player 1 highest card: Q of Hearts
# Player 2 highest card: K of Diamonds
"""

import random


class Card:
    """Represents a single playing card."""

    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = [
        "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "Jack", "Queen", "King", "Ace",
    ]
    RANK_VALUES = {rank: i + 2 for i, rank in enumerate(RANKS)}  # 2=2 ... Ace=14

    def __init__(self, rank, suit):
        """
        Initialize a card.

        Parameters:
            rank (str): Card rank (e.g. '2', 'Jack', 'Ace').
            suit (str): Card suit (e.g. 'Hearts').
        """
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")

        self.rank = rank
        self.suit = suit
        self.value = self.RANK_VALUES[rank]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value


class Deck:
    """Represents a standard 52-card deck."""

    def __init__(self):
        """Create a new 52-card deck in order."""
        self.cards = [
            Card(rank, suit)
            for suit in Card.SUITS
            for rank in Card.RANKS
        ]
        print(f"Deck created with {len(self.cards)} cards.")

    def shuffle(self):
        """Shuffle the deck in place."""
        random.shuffle(self.cards)
        print("Deck shuffled.")

    def deal(self, count=1):
        """
        Deal cards from the top of the deck.

        Parameters:
            count (int): Number of cards to deal.

        Returns:
            list[Card]: Dealt cards.

        Raises:
            ValueError: If not enough cards remain.
        """
        if count > len(self.cards):
            raise ValueError(
                f"Cannot deal {count} cards; only {len(self.cards)} remain."
            )
        dealt = self.cards[:count]
        self.cards = self.cards[count:]
        return dealt

    def deal_hands(self, num_players, cards_per_hand):
        """
        Deal hands to multiple players.

        Parameters:
            num_players (int): Number of players.
            cards_per_hand (int): Cards per player.

        Returns:
            list[list[Card]]: A list of hands.
        """
        total_needed = num_players * cards_per_hand
        if total_needed > len(self.cards):
            raise ValueError(
                f"Need {total_needed} cards but only {len(self.cards)} remain."
            )

        hands = []
        for _ in range(num_players):
            hands.append(self.deal(cards_per_hand))
        return hands

    @property
    def remaining(self):
        """Number of cards still in the deck."""
        return len(self.cards)

    def __repr__(self):
        return f"Deck({self.remaining} cards remaining)"


def war_round(card1, card2, name1="Player 1", name2="Player 2"):
    """
    Play a War-style round: compare two cards, highest wins.

    Parameters:
        card1 (Card): First player's card.
        card2 (Card): Second player's card.
        name1 (str): First player's name.
        name2 (str): Second player's name.
    """
    print(f"\n--- War Round ---")
    print(f"{name1} plays: {card1} (value {card1.value})")
    print(f"{name2} plays: {card2} (value {card2.value})")

    if card1 > card2:
        print(f"{name1} wins this round!")
    elif card2 > card1:
        print(f"{name2} wins this round!")
    else:
        print("It's a tie!")


def hand_highest(hand):
    """Return the highest-value card in a hand."""
    return max(hand)


if __name__ == "__main__":
    print("--- Card Game Demo ---\n")

    # Create and shuffle
    deck = Deck()
    deck.shuffle()
    print()

    # Deal hands
    hands = deck.deal_hands(num_players=2, cards_per_hand=5)
    for i, hand in enumerate(hands, start=1):
        cards_str = ", ".join(str(c) for c in hand)
        print(f"Dealt 5 cards to Player {i}: [{cards_str}]")
    print(f"Cards remaining in deck: {deck.remaining}")

    # War round (first card from each hand)
    war_round(hands[0][0], hands[1][0])

    # Hand evaluation
    print(f"\n--- Hand Evaluation ---")
    for i, hand in enumerate(hands, start=1):
        highest = hand_highest(hand)
        print(f"Player {i} highest card: {highest}")

    # Sort and display a hand
    print(f"\n--- Sorted Hands (low to high) ---")
    for i, hand in enumerate(hands, start=1):
        sorted_hand = sorted(hand)
        cards_str = ", ".join(str(c) for c in sorted_hand)
        print(f"Player {i}: [{cards_str}]")

    # Card comparison demo
    print(f"\n--- Card Comparisons ---")
    c1 = Card("Ace", "Spades")
    c2 = Card("King", "Hearts")
    c3 = Card("Ace", "Diamonds")
    print(f"{c1} > {c2}? {c1 > c2}")
    print(f"{c1} == {c3}? {c1 == c3}")
    print(f"{c2} < {c3}? {c2 < c3}")
