# module.py
class Module:
    def __init__(self, ship, common_data=None):
        self.ship = ship
        self.name = "Unnamed Module"
        self.common_data = common_data

    def update(self, sim_time=None):
        pass

    def get_status(self):
        return f"{self.name}: Operational"

    def handle_command(self, command):
        return f"{self.name} received command: {command}"