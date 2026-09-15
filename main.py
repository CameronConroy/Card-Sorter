from nicegui import ui
import pydealer


deck = pydealer.Deck()

hidden = False

@ui.refreshable
def cardGrid():
    with ui.element("div").props('id=card-container'):
        for card in deck:
            print(card.name)
            


ui.run()

cardGrid()