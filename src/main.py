# main.py
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
import pygame
from ship import Ship
from simulation_controller import SimulationController
from modules.navigation import Navigation
from modules.crew_behavior import CrewBehavior
from modules.deck_layout import DeckLayout

class StarShipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STAR SHIP Simulation")
        self.setGeometry(100, 100, 800, 600)

        # Initialize core components
        self.ship = Ship()
        self.controller = SimulationController(self.ship)
        self.setup_modules()

        # PyGame setup
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
        # Placeholder for GUI updates
        print(f"Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            print(module.get_status())

        # Simulate PyQt timer with PyGame clock
        QApplication.processEvents()
        self.clock.tick(1)  # 1 FPS for simplicity
        if self.controller.running:
            self.after(1000, self.update_simulation)

    def after(self, ms, func):
        # Simplified timer for this example
        QApplication.instance().processEvents()
        func()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StarShipApp()
    window.show()
    sys.exit(app.exec_())