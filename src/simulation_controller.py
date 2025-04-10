# simulation_controller.py
from datetime import datetime

class SimulationController:
    def __init__(self, ship, common_data):
        self.ship = ship
        self.common_data = common_data
        self.modules = []
        self.running = False
        self.module_abbrevs = {
            "nav": "navigation",
            "crew": "crew behavior",
            "deck": "deck layout",
            "com": "combat",
            "eng": "engineering",
        }

    def add_module(self, module):
        module.common_data = self.common_data
        self.modules.append(module)

    def start(self):
        self.running = True
        self.common_data["debug"].append({"source": "sim", "msg": "Simulation started",
                                         "timestamp": self.common_data["simulation"]["sim_time"]})

    def stop(self):
        self.running = False
        self.common_data["debug"].append({"source": "sim", "msg": "Simulation stopped",
                                         "timestamp": self.common_data["simulation"]["sim_time"]})

    def update(self):
        if self.running:
            sim_time = self.common_data["simulation"]["sim_time"]
            for module in self.modules:
                module.update(sim_time=sim_time)  # Pass sim_time to modules
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