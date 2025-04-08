# ship.py
class Ship:
    def __init__(self):
        self.energy = 1000
        self.shields = 100
        self.position = (0, 0)
        self.crew_fatigue = 0
        self.deck_paths = {"corridor_a": "open"}
        self.targets = []
        self.status = "Operational"

    def update_status(self):
        if self.energy <= 0:
            self.status = "Disabled"
        elif self.shields <= 0:
            self.status = "Vulnerable"