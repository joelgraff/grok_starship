# src/simulation.py
import json
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from datetime import datetime, timedelta
import pygame
from ship import Ship
from simulation_controller import SimulationController
from modules.navigation import Navigation
from modules.crew import CrewBehavior
from modules.deck_layout import DeckLayout
from modules.combat import Combat
from modules.engineering import Engineering
from gui.layout import setup_gui

class StarShipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STAR SHIP Simulation")
        self.setGeometry(100, 100, 1200, 600)
        self.ship = Ship()
        self.start_time = datetime.now()
        self.tick_count = 0
        self.common_data = {
            "simulation": {"tick_count": 0, "sim_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S')},
            "engineering": {
                "energy": 1000,
                "max_energy": 2000,
                "warp_energy": 1500,
                "max_warp_energy": 1500,
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
        self.clock = pygame.time.Clock()
        self.log_colors = {
            "Ship Status": QColor("black"),
            "Navigation": QColor("blue"),
            "Crew Behavior": QColor("green"),
            "Deck Layout": QColor("purple"),
            "Combat": QColor("red"),
            "Engineering": QColor("orange"),
        }
        self.module_bars = {}
        self.module_labels = {}
        setup_gui(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(1000)
        self.common_data["debug"].append({"source": "sim", "msg": "Tick rate set to 1/second",
                                         "timestamp": self.start_time.strftime('%Y-%m-%d %H:%M:%S')})
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
        self.ship_status_label.setText(f"Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            status = module.get_status()
            if module.name == "Engineering":
                eng_data = {k.split(': ')[0]: k.split(': ')[1] for k in status.split('|')}
                if "engineering" in self.module_bars:
                    bars = self.module_bars["engineering"]
                    bars["energy"].setValue(int(eng_data["Energy"].split('/')[0]))
                    bars["energy"].setCustomText(f"Energy: {eng_data['Energy']}")
                    bars["warp_energy"].setValue(int(eng_data["Warp Energy"].split('/')[0]))
                    bars["warp_energy"].setMaximum(int(eng_data["Warp Energy"].split('/')[1]))
                    bars["warp_energy"].setCustomText(f"Warp Energy: {eng_data['Warp Energy']}")
                    bars["shields"].setValue(int(float(eng_data["Shields"].rstrip('%'))))
                    bars["shields"].setCustomText(f"Shields: {eng_data['Shields']}")
                    bars["health_shields"].setValue(int(float(eng_data['Health-Shields'].rstrip('%'))))
                    bars["health_shields"].setCustomText(f"Shields Health: {eng_data['Health-Shields']}")
                    bars["health_shields"].setMarkerPosition(int(float(eng_data['Alloc-Shields'].rstrip('%'))))
                    bars["health_weapons"].setValue(int(float(eng_data['Health-Weapons'].rstrip('%'))))
                    bars["health_weapons"].setCustomText(f"Weapons Health: {eng_data['Health-Weapons']}")
                    bars["health_weapons"].setMarkerPosition(int(float(eng_data['Alloc-Weapons'].rstrip('%'))))
                    bars["health_propulsion"].setValue(int(float(eng_data['Health-Propulsion'].rstrip('%'))))
                    bars["health_propulsion"].setCustomText(f"Propulsion Health: {eng_data['Health-Propulsion']}")
                    bars["health_propulsion"].setMarkerPosition(int(float(eng_data['Alloc-Propulsion'].rstrip('%'))))
                    bars["alloc_reserve"].setValue(int(float(eng_data['Alloc-Reserve'].rstrip('%'))))
                    bars["alloc_reserve"].setCustomText(f"Reserve Alloc: {eng_data['Alloc-Reserve']}")
                    impulse_val = int(float(eng_data['Impulse'].rstrip('%')))
                    bars["impulse"].setValue(impulse_val)
                    bars["impulse"].setCustomText(f"Impulse: {impulse_val}%")
                    warp_val = int(float(eng_data['Warp']))
                    bars["warp"].setValue(warp_val)
                    bars["warp"].setCustomText(f"Warp: {warp_val}")
            else:
                self.module_labels[module.name].setText(status)

        self.nav_widget.update_surface(self.ship.position, self.ship.targets)
        self.deck_widget.update_surface(deck_paths=self.ship.deck_paths)

        timestamp = self.common_data["simulation"]["sim_time"]
        if self.log_filters["Ship Status"].isChecked():
            self.debug_log.setTextColor(self.log_colors["Ship Status"])
            self.debug_log.append(f"[{timestamp}] Ship Status: {self.ship.status}")
        for module in self.controller.modules:
            if self.log_filters[module.name].isChecked() and module.name != "Engineering":
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