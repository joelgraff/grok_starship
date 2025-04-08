import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication
import pygame

# Centralized ship state
class Ship:
    def __init__(self):
        self.energy = 1000
        self.shields = 100
        self.position = (0, 0)
        self.crew_fatigue = 0  # Crew behavior example
        self.deck_paths = {"corridor_a": "open"}  # Deck layout example
        self.targets = []
        self.status = "Operational"

    def update_status(self):
        if self.energy <= 0:
            self.status = "Disabled"
        elif self.shields <= 0:
            self.status = "Vulnerable"

# Base Module Template
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

# Example Modules
class Navigation(Module):
    def __init__(self, ship):
        super().__init__(ship)
        self.name = "Navigation"

    def update(self):
        # Simulate movement
        self.ship.position = (self.ship.position[0] + 1, self.ship.position[1])

    def get_status(self):
        return f"Navigation: Position {self.ship.position}"

    def handle_command(self, command):
        if command.startswith("set_course"):
            x, y = map(int, command.split()[1:])
            self.ship.position = (x, y)
            return "Course set successfully"
        return super().handle_command(command)

class CrewBehavior(Module):
    def __init__(self, ship):
        super().__init__(ship)
        self.name = "Crew Behavior"

    def update(self):
        # Simulate crew fatigue increasing
        self.ship.crew_fatigue += random.randint(0, 2)
        if self.ship.crew_fatigue > 50:
            self.ship.status = "Crew Fatigued"

    def get_status(self):
        return f"Crew Behavior: Fatigue {self.ship.crew_fatigue}"

class DeckLayout(Module):
    def __init__(self, ship):
        super().__init__(ship)
        self.name = "Deck Layout"

    def update(self):
        # Simulate a random blockage
        if random.random() < 0.1:
            self.ship.deck_paths["corridor_a"] = "blocked"

    def get_status(self):
        return f"Deck Layout: Corridor A {self.ship.deck_paths['corridor_a']}"

# Simulation Controller
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
                module.update()  # Poll each module
            self.ship.update_status()

    def process_command(self, command):
        # Simple command routing based on first word
        target_module = command.split()[0].lower()
        for module in self.modules:
            if target_module in module.name.lower():
                return module.handle_command(command)
        return "Command not recognized"

# GUI with PyQt5 and PyGame
class StarShipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STAR SHIP Simulation")
        self.setGeometry(100, 100, 800, 600)

        # Initialize ship and controller
        self.ship = Ship()
        self.controller = SimulationController(self.ship)
        self.setup_modules()

        # PyGame setup for graphics (embedded later)
        pygame.init()
        self.clock = pygame.time.Clock()

        # Start simulation
        self.controller.start()
        self.update_simulation()

    def setup_modules(self):
        self.controller.add_module(Navigation(self.ship))
        self.controller.add_module(CrewBehavior(self.ship))
        self.controller.add_module(DeckLayout(self.ship))

    def update_simulation(self):
        self.controller.update()
        # Placeholder for GUI updates (e.g., status display)
        print(f"Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            print(module.get_status())

        # Schedule next update (simulating PyQt timer)
        QApplication.processEvents()
        self.clock.tick(1)  # 1 FPS for simplicity
        if self.controller.running:
            self.after(1000, self.update_simulation)  # PyQt equivalent

    def after(self, ms, func):
        # Simplified timer for this example
        QApplication.instance().processEvents()
        func()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StarShipApp()
    window.show()
    sys.exit(app.exec_())