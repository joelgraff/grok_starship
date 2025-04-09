# modules/deck_layout.py
import random
from modules.module import Module

class DeckLayout(Module):
    def __init__(self, ship, common_data=None):
        super().__init__(ship)
        self.name = "Deck Layout"

    def update(self, sim_time=None):
        # Randomly toggle corridor status
        if random.random() < 0.1:
            current = self.ship.deck_paths["corridor_a"]
            self.ship.deck_paths["corridor_a"] = "blocked" if current == "open" else "open"

    def get_status(self):
        return f"Deck Layout: Corridor A {self.ship.deck_paths['corridor_a']}"