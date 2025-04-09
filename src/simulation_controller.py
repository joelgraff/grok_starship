# simulation_controller.py
class SimulationController:
    def __init__(self, ship):
        self.ship = ship
        self.modules = []
        self.running = False
        self.module_abbrevs = {
            "nav": "navigation",
            "crew": "crew behavior",
            "deck": "deck layout",
            "com": "combat",
            "eng": "engineering",  # Added for Engineering
        }

    def add_module(self, module):
        self.modules.append(module)

    def start(self):
        self.running = True
        print("Simulation started")

    def stop(self):
        self.running = False
        print("Simulation stopped")

    def update(self):
        if self.running:
            for module in self.modules:
                module.update()
            self.ship.update_status()

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return "Command not recognized"
        abbrev = parts[0].lower()
        if abbrev in self.module_abbrevs:
            target_module = self.module_abbrevs[abbrev]
            for module in self.modules:
                if target_module in module.name.lower():
                    return module.handle_command(" ".join(parts[1:]) if len(parts) > 1 else "")
        return f"Command not recognized: Unknown module abbreviation '{abbrev}'"