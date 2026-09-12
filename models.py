class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    @property
    def id (self):
        return f"{self.rank}-{self.suit}"
RANK_ORDER = [
    "A",
    "K",
    "Q",
    "J",
    "10",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2"
]


card = Card("A", "Spades")

print(card.rank)
print(card.suit)
print(card.id)