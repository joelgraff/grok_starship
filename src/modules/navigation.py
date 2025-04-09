# navigation.py
from modules.module import Module

class Navigation(Module):
    def __init__(self, ship, common_data=None):
        super().__init__(ship)
        self.name = "Navigation"

    def update(self, sim_time=None):
        self.ship.position = (self.ship.position[0] + 1, self.ship.position[1])

    def get_status(self):
        return f"Navigation: Position {self.ship.position}"

    def handle_command(self, command):
        if command.startswith("set_course"):
            x, y = map(int, command.split()[1:])
            self.ship.position = (x, y)
            return "Course set successfully"
        return super().handle_command(command)