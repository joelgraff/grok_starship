# simulation_controller.py
class SimulationController:
    def __init__(self, ship):
        self.ship = ship
        self.modules = []
        self.running = False

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
        target_module = command.split()[0].lower()
        for module in self.modules:
            if target_module in module.name.lower():
                return module.handle_command(command)
        return "Command not recognized"