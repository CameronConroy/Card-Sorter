from nicegui import ui
from models import Card


deck = [
    Card("A", "Spades"),
]


hidden = False


@ui.refreshable
def cardGrid():
    with ui.element("div").props('id=card-container'):
        for card in deck:
            ui.image("https://static.vecteezy.com/system/resources/thumbnails/004/442/850/small/ace-of-spades-playing-card-isolated-free-vector.jpg").props(
                f'data-id="{card.id}"'
            )

cardGrid()

ui.run()