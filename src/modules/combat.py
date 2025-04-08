# combat.py
import random
from modules.module import Module

class Combat(Module):
    def __init__(self, ship):
        super().__init__(ship)
        self.name = "Combat"

    def update(self):
        # Randomly spawn a target if fewer than 3 exist
        if len(self.ship.targets) < 3 and random.random() < 0.1:
            self.ship.targets.append({
                "position": (random.randint(-10, 10), random.randint(-10, 10)),
                "health": 100
            })

    def get_status(self):
        target_count = len(self.ship.targets)
        return f"Combat: {target_count} target{'s' if target_count != 1 else ''} detected"

    def handle_command(self, command):
        if command.startswith("fire_phasers") and self.ship.energy > 50:
            if self.ship.targets:
                target = self.ship.targets[0]  # Target the first one
                damage = random.randint(20, 50)
                target["health"] -= damage
                self.ship.energy -= 50
                if target["health"] <= 0:
                    self.ship.targets.pop(0)
                    return "Target destroyed!"
                return f"Phasers hit target for {damage} damage"
            return "No targets in range"
        return super().handle_command(command)