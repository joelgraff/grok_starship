# simulation.py
import json
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from datetime import datetime, timedelta
import pygame
from ship import Ship
from simulation_controller import SimulationController
from modules.navigation import Navigation
from modules.crew_behavior import CrewBehavior
from modules.deck_layout import DeckLayout
from modules.combat import Combat
from modules.engineering import Engineering
from gui.tabs import setup_gui

class StarShipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STAR SHIP Simulation")
        self.setGeometry(100, 100, 1200, 600)

        # Initialize core components
        self.ship = Ship()
        self.start_time = datetime.now()  # Sim start time
        self.tick_count = 0
        self.common_data = {
            "simulation": {"tick_count": 0, "sim_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S')},
            "engineering": {
                "energy": 1000,
                "max_energy": 2000,
                "allocations": {"shields": 30, "weapons": 20, "propulsion": 40, "reserve": 10},
                "shields": 100,
                "system_health": {"shields": 100, "weapons": 100, "propulsion": 100},
                "impulse_speed": 50,
                "warp_factor": 0,
            },
            "combat": {},
            "navigation": {},
            "crew_tasks": [],
            "debug": []
        }
        self.ship.common_data = self.common_data
        self.controller = SimulationController(self.ship, self.common_data)
        self.setup_modules()

        # PyGame clock
        self.clock = pygame.time.Clock()

        # Color mapping for logs
        self.log_colors = {
            "Ship Status": QColor("black"),
            "Navigation": QColor("blue"),
            "Crew Behavior": QColor("green"),
            "Deck Layout": QColor("purple"),
            "Combat": QColor("red"),
            "Engineering": QColor("orange"),
        }

        # Initialize UI-related attributes
        self.module_bars = {}  # Added to prevent attribute error

        # GUI setup
        setup_gui(self)

        # Set up QTimer (1 tick/second) - Moved after GUI setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(1000)
        self.common_data["debug"].append({"source": "sim", "msg": "Tick rate set to 1/second",
                                         "timestamp": self.start_time.strftime('%Y-%m-%d %H:%M:%S')})

        # Start simulation
        self.controller.start()

    def setup_modules(self):
        self.controller.add_module(Navigation(self.ship, self.common_data))
        self.controller.add_module(CrewBehavior(self.ship, self.common_data))
        self.controller.add_module(DeckLayout(self.ship, self.common_data))
        self.controller.add_module(Combat(self.ship, self.common_data))
        self.controller.add_module(Engineering(self.ship, self.common_data))

    def update_simulation(self):
        self.tick_count += 1
        self.common_data["simulation"]["tick_count"] = self.tick_count
        self.common_data["simulation"]["sim_time"] = (self.start_time +
            timedelta(seconds=self.tick_count)).strftime('%Y-%m-%d %H:%M:%S')
        self.controller.update()
        # Update GUI
        self.ship_status_label.setText(f"Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            status = module.get_status()
            self.module_labels[module.name].setText(status)
            if module.name == "Engineering" and "engineering" in self.module_bars:
                eng_data = {k.split(': ')[0]: float(k.split(': ')[1].rstrip('%')) if '%' in k else k.split(': ')[1]
                           for k in status.split('|')}
                self.module_bars["engineering"]["energy"].setValue(int(eng_data["Energy"].split('/')[0]))
                self.module_bars["engineering"]["shields"].setValue(int(eng_data["Shields"]))

        # Update PyGame surfaces
        self.nav_widget.update_surface(self.ship.position, self.ship.targets)
        self.deck_widget.update_surface(deck_paths=self.ship.deck_paths)

        # Log to debug panel
        timestamp = self.common_data["simulation"]["sim_time"]
        if self.log_filters["Ship Status"].isChecked():
            self.debug_log.setTextColor(self.log_colors["Ship Status"])
            self.debug_log.append(f"[{timestamp}] Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            if self.log_filters[module.name].isChecked():
                self.debug_log.setTextColor(self.log_colors[module.name])
                self.debug_log.append(f"[{timestamp}] {module.get_status()}")
        debug_entries = self.common_data["debug"]
        for entry in debug_entries:
            source = entry.get("source", "Unknown")
            msg = entry.get("msg", "")
            time = entry.get("timestamp", timestamp)
            if source in self.log_filters and self.log_filters[source].isChecked():
                self.debug_log.setTextColor(self.log_colors.get(source, QColor("gray")))
                self.debug_log.append(f"[{time}] {source.upper()}: {msg}")
        # Prune debug log to last 100 entries
        if len(debug_entries) > 100:
            self.common_data["debug"] = debug_entries[-100:]
        else:
            self.common_data["debug"].clear()
        self.clock.tick(1)

    def process_command(self):
        command = self.command_input.text()
        result = self.controller.process_command(command)
        self.command_output.setText(f"Command output: {result}")
        if self.log_filters["Ship Status"].isChecked():
            self.debug_log.setTextColor(self.log_colors["Ship Status"])
            self.debug_log.append(f"[{self.common_data['simulation']['sim_time']}] Command: {command} -> {result}")
        self.command_input.clear()

    def save_filter_settings(self):
        settings = {name: button.isChecked() for name, button in self.log_filters.items()}
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
            for button in self.log_filters.values():
                button.setChecked(True)