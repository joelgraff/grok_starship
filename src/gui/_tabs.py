# gui/tabs.py
import json
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QFrame
from PyQt5.QtGui import QColor, QFont
from .widgets import PygameWidget
from .custom_progress import CustomProgressBar  # Clean import

def setup_command_status_panel(app):
    panel = QWidget()
    layout = QVBoxLayout()

    app.command_input = QLineEdit()
    app.command_input.setPlaceholderText("Enter command (e.g., nav set_course 10 20)")
    app.command_input.returnPressed.connect(app.process_command)
    layout.addWidget(app.command_input)

    app.command_output = QLabel("Command output: None")
    layout.addWidget(app.command_output)

    status_layout = QVBoxLayout()
    app.ship_status_label = QLabel(f"Ship Status: {app.ship.status}")
    ship_panel = QWidget()
    ship_panel.setStyleSheet("background-color: black; color: white;")
    ship_panel_layout = QVBoxLayout()
    ship_panel_layout.addWidget(app.ship_status_label)
    ship_panel.setLayout(ship_panel_layout)
    status_layout.addWidget(ship_panel)

    app.module_labels = {}
    app.module_bars = {}
    font = QFont("Arial", 10)  # Font size for readability
    for module in app.controller.modules:
        module_panel = QWidget()
        color = app.log_colors[module.name].name()
        module_panel.setStyleSheet(f"background-color: {color}; color: white;")
        module_panel_layout = QVBoxLayout()
        if module.name == "Engineering":
            # Parse structured status
            status = module.get_status()
            eng_data = {k.split(': ')[0]: k.split(': ')[1] for k in status.split('|')}
            # Energy
            energy_label = QLabel(f"Energy: {eng_data['Energy']}")
            energy_label.setFont(font)
            energy_bar = CustomProgressBar()
            energy_bar.setMaximum(app.common_data["engineering"]["max_energy"])
            energy_bar.setValue(int(eng_data["Energy"].split('/')[0]))
            energy_bar.setCustomText(f"Energy: {eng_data['Energy']}")
            energy_bar.setFont(font)
            # Shields
            shields_label = QLabel(f"Shields: {eng_data['Shields']}")
            shields_label.setFont(font)
            shields_bar = CustomProgressBar()
            shields_bar.setMaximum(100)
            shields_bar.setValue(int(float(eng_data["Shields"].rstrip('%'))))
            shields_bar.setCustomText(f"Shields: {eng_data['Shields']}")
            shields_bar.setFont(font)
            # Allocations group
            alloc_separator = QFrame()
            alloc_separator.setFrameShape(QFrame.HLine)
            alloc_separator.setFrameShadow(QFrame.Sunken)
            alloc_shields_bar = CustomProgressBar()
            alloc_shields_bar.setMaximum(100)
            alloc_shields_val = int(float(eng_data['Alloc-Shields'].rstrip('%')))
            alloc_shields_bar.setValue(alloc_shields_val)
            alloc_shields_bar.setCustomText(f"Shields Alloc: {alloc_shields_val}%")
            alloc_shields_bar.setFont(font)
            alloc_weapons_bar = CustomProgressBar()
            alloc_weapons_bar.setMaximum(100)
            alloc_weapons_val = int(float(eng_data['Alloc-Weapons'].rstrip('%')))
            alloc_weapons_bar.setValue(alloc_weapons_val)
            alloc_weapons_bar.setCustomText(f"Weapons Alloc: {alloc_weapons_val}%")
            alloc_weapons_bar.setFont(font)
            alloc_propulsion_bar = CustomProgressBar()
            alloc_propulsion_bar.setMaximum(100)
            alloc_propulsion_val = int(float(eng_data['Alloc-Propulsion'].rstrip('%')))
            alloc_propulsion_bar.setValue(alloc_propulsion_val)
            alloc_propulsion_bar.setCustomText(f"Propulsion Alloc: {alloc_propulsion_val}%")
            alloc_propulsion_bar.setFont(font)
            alloc_reserve_bar = CustomProgressBar()
            alloc_reserve_bar.setMaximum(100)
            alloc_reserve_val = int(float(eng_data['Alloc-Reserve'].rstrip('%')))
            alloc_reserve_bar.setValue(alloc_reserve_val)
            alloc_reserve_bar.setCustomText(f"Reserve Alloc: {alloc_reserve_val}%")
            alloc_reserve_bar.setFont(font)
            # Propulsion group (Impulse/Warp)
            propulsion_separator = QFrame()
            propulsion_separator.setFrameShape(QFrame.HLine)
            propulsion_separator.setFrameShadow(QFrame.Sunken)
            impulse_bar = CustomProgressBar()
            impulse_bar.setMaximum(100)
            impulse_val = int(float(eng_data['Impulse'].rstrip('%')))
            impulse_bar.setValue(impulse_val)
            impulse_bar.setCustomText(f"Impulse: {impulse_val}%")
            impulse_bar.setFont(font)
            impulse_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid gray;
                    background-color: #444444;
                    color: white;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #006400, stop:1 #FFD700);
                }
            """)
            warp_bar = CustomProgressBar()
            warp_bar.setMaximum(10)
            warp_val = int(float(eng_data['Warp']))
            warp_bar.setValue(warp_val)
            warp_bar.setCustomText(f"Warp: {warp_val}")
            warp_bar.setFont(font)
            warp_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid gray;
                    background-color: #444444;
                    color: white;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 blue, stop:1 red);
                }
            """)
            # System Health group
            health_separator = QFrame()
            health_separator.setFrameShape(QFrame.HLine)
            health_separator.setFrameShadow(QFrame.Sunken)
            health_shields_bar = CustomProgressBar()
            health_shields_bar.setMaximum(100)
            health_shields_val = int(float(eng_data['Health-Shields'].rstrip('%')))
            health_shields_bar.setValue(health_shields_val)
            health_shields_bar.setCustomText(f"Shields Health: {health_shields_val}%")
            health_shields_bar.setFont(font)
            health_weapons_bar = CustomProgressBar()
            health_weapons_bar.setMaximum(100)
            health_weapons_val = int(float(eng_data['Health-Weapons'].rstrip('%')))
            health_weapons_bar.setValue(health_weapons_val)
            health_weapons_bar.setCustomText(f"Weapons Health: {health_weapons_val}%")
            health_weapons_bar.setFont(font)
            health_propulsion_bar = CustomProgressBar()
            health_propulsion_bar.setMaximum(100)
            health_propulsion_val = int(float(eng_data['Health-Propulsion'].rstrip('%')))
            health_propulsion_bar.setValue(health_propulsion_val)
            health_propulsion_bar.setCustomText(f"Propulsion Health: {health_propulsion_val}%")
            health_propulsion_bar.setFont(font)
            # Apply solid color to non-gradient bars
            for bar in [energy_bar, shields_bar, alloc_shields_bar, alloc_weapons_bar,
                        alloc_propulsion_bar, alloc_reserve_bar, health_shields_bar,
                        health_weapons_bar, health_propulsion_bar]:
                bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid gray;
                        background-color: #444444;
                        color: white;
                        text-align: center;
                    }
                    QProgressBar::chunk {
                        background-color: #008080;
                    }
                """)
            # Add to main layout
            module_panel_layout.addWidget(energy_label)
            module_panel_layout.addWidget(energy_bar)
            module_panel_layout.addWidget(shields_label)
            module_panel_layout.addWidget(shields_bar)
            module_panel_layout.addWidget(alloc_separator)
            module_panel_layout.addWidget(alloc_shields_bar)
            module_panel_layout.addWidget(alloc_weapons_bar)
            module_panel_layout.addWidget(alloc_propulsion_bar)
            module_panel_layout.addWidget(alloc_reserve_bar)
            module_panel_layout.addWidget(propulsion_separator)
            module_panel_layout.addWidget(impulse_bar)
            module_panel_layout.addWidget(warp_bar)
            module_panel_layout.addWidget(health_separator)
            module_panel_layout.addWidget(health_shields_bar)
            module_panel_layout.addWidget(health_weapons_bar)
            module_panel_layout.addWidget(health_propulsion_bar)
            app.module_bars["engineering"] = {
                "energy": energy_bar,
                "shields": shields_bar,
                "alloc_shields": alloc_shields_bar,
                "alloc_weapons": alloc_weapons_bar,
                "alloc_propulsion": alloc_propulsion_bar,
                "alloc_reserve": alloc_reserve_bar,
                "impulse": impulse_bar,
                "warp": warp_bar,
                "health_shields": health_shields_bar,
                "health_weapons": health_weapons_bar,
                "health_propulsion": health_propulsion_bar
            }
            app.module_labels[module.name] = [
                energy_label, shields_label, None, None, None, None,  # None for allocation
                None, None, None, None, None  # None for impulse, warp, health
            ]
        else:
            label = QLabel(module.get_status())
            label.setFont(font)
            module_panel_layout.addWidget(label)
            app.module_labels[module.name] = label

        module_panel.setLayout(module_panel_layout)
        status_layout.addWidget(module_panel)

    status_layout.addStretch()
    layout.addLayout(status_layout)

    panel.setLayout(layout)
    panel.setMaximumWidth(300)
    return panel

def setup_navigation_view_panel(app):
    panel = QWidget()
    layout = QVBoxLayout()
    app.nav_view_label = QLabel("Navigation View (PyGame)")
    layout.addWidget(app.nav_view_label)
    app.nav_widget = PygameWidget(app)
    app.nav_widget.setMinimumSize(600, 400)
    app.nav_widget.set_mode("navigation")
    layout.addWidget(app.nav_widget)
    panel.setLayout(layout)
    return panel

def setup_deck_view_panel(app):
    panel = QWidget()
    layout = QVBoxLayout()
    app.deck_view_label = QLabel("Deck View (PyGame)")
    layout.addWidget(app.deck_view_label)
    app.deck_widget = PygameWidget(app)
    app.deck_widget.setMinimumSize(600, 400)
    app.deck_widget.set_mode("deck")
    layout.addWidget(app.deck_widget)
    panel.setLayout(layout)
    return panel

def setup_debug_log_panel(app):
    panel = QWidget()
    layout = QVBoxLayout()

    app.log_filters = {}
    filter_layout = QHBoxLayout()
    app.log_filters["Ship Status"] = QPushButton("Ship Status")
    app.log_filters["Ship Status"].setCheckable(True)
    app.log_filters["Ship Status"].setChecked(True)
    app.log_filters["Ship Status"].setStyleSheet("background-color: black; color: white; border: 1px solid gray;")
    app.log_filters["Ship Status"].toggled.connect(lambda checked: update_button_style(app.log_filters["Ship Status"], checked, "black"))
    app.log_filters["Ship Status"].toggled.connect(app.save_filter_settings)
    filter_layout.addWidget(app.log_filters["Ship Status"])

    for module in app.controller.modules:
        name = module.name
        color = app.log_colors[name].name()
        app.log_filters[name] = QPushButton(name)
        app.log_filters[name].setCheckable(True)
        app.log_filters[name].setChecked(True)
        app.log_filters[name].setStyleSheet(f"background-color: {color}; color: white; border: 1px solid gray;")
        app.log_filters[name].toggled.connect(lambda checked, n=name: update_button_style(app.log_filters[n], checked, app.log_colors[n].name()))
        app.log_filters[name].toggled.connect(app.save_filter_settings)
        filter_layout.addWidget(app.log_filters[name])
    layout.addLayout(filter_layout)

    app.load_filter_settings()

    app.debug_log = QTextEdit()
    app.debug_log.setReadOnly(True)
    app.debug_log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Simulation initialized")
    layout.addWidget(app.debug_log)

    clear_button = QPushButton("Clear Log")
    clear_button.clicked.connect(app.debug_log.clear)
    layout.addWidget(clear_button)

    panel.setLayout(layout)
    return panel

def update_button_style(button, checked, color):
    if checked:
        button.setStyleSheet(f"background-color: {color}; color: white; border: 1px solid gray;")
    else:
        button.setStyleSheet(f"background-color: gray; color: black; border: 1px solid gray;")

def setup_gui(app):
    main_widget = QWidget()
    grid = QGridLayout()

    command_status_panel = setup_command_status_panel(app)
    grid.addWidget(command_status_panel, 0, 0, 2, 1)

    nav_panel = setup_navigation_view_panel(app)
    deck_panel = setup_deck_view_panel(app)
    grid.addWidget(nav_panel, 0, 1)
    grid.addWidget(deck_panel, 1, 1)

    debug_panel = setup_debug_log_panel(app)
    grid.addWidget(debug_panel, 0, 2, 2, 1)

    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 4)
    grid.setColumnStretch(2, 2)

    main_widget.setLayout(grid)
    app.setCentralWidget(main_widget)