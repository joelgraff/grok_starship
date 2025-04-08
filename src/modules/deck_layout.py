# deck_layout.py
import random
from module import Module

class DeckLayout(Module):
    def __init__(self, ship):
        super().__init__(ship)
        self.name = "Deck Layout"

    def update(self):
        if random.random() < 0.1:
            self.ship.deck_paths["corridor_a"] = "blocked"

    def get_status(self):
        return f"Deck Layout: Corridor A {self.ship.deck_paths['corridor_a']}"