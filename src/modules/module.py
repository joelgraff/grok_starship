# module.py
class Module:
    def __init__(self, ship):
        self.ship = ship  # Reference to shared data
        self.name = "Generic Module"

    def update(self):
        """Called by the controller each time step to update module state."""
        pass

    def get_status(self):
        """Returns a string summarizing the module's current state."""
        return f"{self.name}: Operational"

    def handle_command(self, command):
        """Processes operator commands routed by the controller."""
        return f"{self.name} received command: {command}"