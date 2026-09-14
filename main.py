from nicegui import ui
from models import Card


ranks = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

deck = []

for suit in suits:
    for rank in ranks:
        deck.append(Card(rank, suit))


hidden = False

@ui.refreshable
def cardGrid():
    with ui.element("div").props('id=card-container'):
        for card in deck:
            ui.image().props(
                f'data-id="{card.id}"'
            )

cardGrid()
ui.run()
print(len(deck))