# engineering.py
from modules.module import Module

class Engineering(Module):
    def __init__(self, ship):
        super().__init__(ship)
        self.name = "Engineering"

    def update(self):
        # Placeholder: Regenerate a bit of energy
        if self.ship.energy < 1000:
            self.ship.energy += 5

    def get_status(self):
        return f"Engineering: Energy {self.ship.energy}, Shields {self.ship.shields}%"

    def handle_command(self, command):
        if command == "status":
            return f"Energy at {self.ship.energy}, Shields at {self.ship.shields}%"
        return super().handle_command(command)