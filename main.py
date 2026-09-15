from nicegui import app, ui
import pydealer


originalOrder = list(reversed(pydealer.Deck()))

deck = pydealer.Deck()
deck.set_cards(originalOrder.copy())
submittedDeck = []
hidden = False
hiddenLocked = False

app.add_static_files("/static", "static")

# CSS for website
ui.add_css("""
    body, .q-page, .nicegui-content {
        background: #050505 !important;
        color: #f5f5f5;
    }

    body {
        margin: 0;
        min-height: 100vh;
        font-family: Inter, Arial, sans-serif;
    }

    .card-container {
        overflow-x: auto;
        overflow-y: hidden;
        min-height: 240px;
        padding: 32px 20px 24px;
        margin-top: 20px;
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #252525;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgb(0 0 0 / 55%);
    }

    .playing-card {
        position: relative;
        flex: 0 0 140px;
        width: 140px;
        margin-left: calc((100% - 140px) / 51 - 140px);
        border-radius: 10px;
        filter: drop-shadow(0 4px 5px rgb(0 0 0 / 55%));
        transition: transform 160ms ease, filter 160ms ease;
        cursor: grab;
        user-select: none;
    }

    .playing-card:first-child {
        margin-left: 0;
    }

    .playing-card:hover {
        z-index: 1000 !important;
        transform: translateY(-20px) scale(1.07);
        filter: drop-shadow(0 12px 10px rgb(0 0 0 / 70%));
    }

    .card-placeholder {
        opacity: 0.35;
        outline: 3px solid #22d3ee;
        outline-offset: -3px;
    }

    .toolbar {
        padding: 12px 14px;
        gap: 9px;
        background: #0d0d0d;
        border: 1px solid #252525;
        border-radius: 14px;
        box-shadow: 0 6px 20px rgb(0 0 0 / 35%);
    }

    .q-btn {
        background: #171717 !important;
        color: #eee !important;
        border: 1px solid #333;
        border-radius: 9px;
        padding: 7px 15px;
        font-weight: 600;
        box-shadow: 0 3px 8px rgb(0 0 0 / 35%);
    }

    .q-btn:hover {
        background: #222 !important;
        border-color: #22d3ee;
    }

    .q-btn .q-icon {
        color: #22d3ee;
    }

    .card-container::-webkit-scrollbar {
        height: 9px;
    }

    .card-container::-webkit-scrollbar-track {
        background: #0c0c0c;
    }

    .card-container::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 10px;
    }

    .card-container::-webkit-scrollbar-thumb:hover {
        background: #22d3ee;
    }
""")


# Image path generator
def cardImage(card):
    filename = f"{card.value.lower()}_of_{card.suit.lower()}.png"
    return f"/static/cards/{filename}"


# Drag and drop cards
def moveCard(event):
    cards = list(deck)
    cards.insert(event.new_index, cards.pop(event.old_index))
    deck.set_cards(cards)


# Hide cards
def toggleHidden():
    global hidden

    if hiddenLocked:
        ui.notify("Reset the order before revealing the cards")
        return

    hidden = not hidden
    cardsList.refresh()


# Randomize deck order
def randomizeDeck():
    deck.shuffle()
    cardsList.refresh()


# Randomize cards and force hidden till reset
def randomizeHidden():
    global hidden, hiddenLocked

    deck.shuffle()
    hidden = True
    hiddenLocked = True
    cardsList.refresh()


# Reset deck to original state
def resetDeck():
    global hidden, hiddenLocked

    deck.set_cards(originalOrder.copy())
    hidden = False
    hiddenLocked = False
    cardsList.refresh()


# Submit deck order to api
def submitDeck():
    submittedDeck[:] = [card.name for card in deck]
    ui.notify("Deck submitted", color="positive")


# Call deck order api
@app.get("/api/deck")
def getSubmittedDeck():
    return {"cards": submittedDeck}


@ui.refreshable

# Display cards in website
def cardsList():
    with ui.row().classes("card-container w-full no-wrap gap-0") as container:
        for card in deck:
            source = "/static/cards/back.png" if hidden else cardImage(card)
            ui.image(source).props(f'alt="{card.name}"').classes("playing-card")

        container.make_sortable(
            {"direction": "horizontal", "swapThreshold": 0.3, "invertSwap": True},
            on_end=moveCard,
            animation=0.12,
            ghost_class="card-placeholder",
        )


# Website buttons
with ui.row().classes("w-full items-center"):
    ui.button("Toggle hidden", on_click=toggleHidden, icon="visibility")
    ui.button("Randomize", on_click=randomizeDeck, icon="shuffle")
    ui.button("Randomize hidden", on_click=randomizeHidden, icon="visibility_off")
    ui.button("Reset order", on_click=resetDeck, icon="restart_alt")
    ui.space()
    ui.button("Submit", on_click=submitDeck, icon="send")

cardsList()
ui.run(port=2222)