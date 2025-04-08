# simulation.py
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from datetime import datetime
import pygame
from ship import Ship
from simulation_controller import SimulationController
from modules.navigation import Navigation
from modules.crew_behavior import CrewBehavior
from modules.deck_layout import DeckLayout
from gui.tabs import setup_gui
import json

class StarShipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STAR SHIP Simulation")
        self.setGeometry(100, 100, 800, 600)

        # Initialize core components
        self.ship = Ship()
        self.controller = SimulationController(self.ship)
        self.setup_modules()

        # PyGame clock
        self.clock = pygame.time.Clock()

        # Color mapping for logs
        self.log_colors = {
            "Ship Status": QColor("black"),
            "Navigation": QColor("blue"),
            "Crew Behavior": QColor("green"),
            "Deck Layout": QColor("purple"),
        }

        # GUI setup
        setup_gui(self)

        # Set up QTimer for simulation updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(1000)  # Update every 1000 ms

        # Start simulation
        self.controller.start()

    def setup_modules(self):
        self.controller.add_module(Navigation(self.ship))
        self.controller.add_module(CrewBehavior(self.ship))
        self.controller.add_module(DeckLayout(self.ship))

    def update_simulation(self):
        self.controller.update()
        # Update GUI
        self.ship_status_label.setText(f"Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            self.module_labels[module.name].setText(module.get_status())

        # Update PyGame surface
        self.nav_widget.update_surface(self.ship.position)

        # Log to debug tab with timestamps and colors
        timestamp = datetime.now().strftime('%H:%M:%S')
        if self.log_filters["Ship Status"].isChecked():
            self.debug_log.setTextColor(self.log_colors["Ship Status"])
            self.debug_log.append(f"[{timestamp}] Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            if self.log_filters[module.name].isChecked():
                self.debug_log.setTextColor(self.log_colors[module.name])
                self.debug_log.append(f"[{timestamp}] {module.get_status()}")
        self.clock.tick(1)

    def process_command(self):
        command = self.command_input.text()
        result = self.controller.process_command(command)
        self.command_output.setText(f"Command output: {result}")
        if self.log_filters["Ship Status"].isChecked():
            self.debug_log.setTextColor(self.log_colors["Ship Status"])
            self.debug_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] Command: {command} -> {result}")
        self.command_input.clear()

    def save_filter_settings(self):
        settings = {name: checkbox.isChecked() for name, checkbox in self.log_filters.items()}
        with open("filter_settings.json", "w") as f:
            json.dump(settings, f)

    def load_filter_settings(self):
        try:
            with open("filter_settings.json", "r") as f:
                settings = json.load(f)
                for name, checked in settings.items():
                    if name in self.log_filters:
                        self.log_filters[name].setChecked(checked)
        except FileNotFoundError:
            for checkbox in self.log_filters.values():
                checkbox.setChecked(True)