# gui/tabs.py
import json
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QColor
from .widgets import PygameWidget

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
    for module in app.controller.modules:
        label = QLabel(module.get_status())
        module_panel = QWidget()
        color = app.log_colors[module.name].name()
        module_panel.setStyleSheet(f"background-color: {color}; color: white;")
        module_panel_layout = QVBoxLayout()
        module_panel_layout.addWidget(label)
        module_panel.setLayout(module_panel_layout)
        status_layout.addWidget(module_panel)
        app.module_labels[module.name] = label

    status_layout.addStretch()
    layout.addLayout(status_layout)

    panel.setLayout(layout)
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
    app.debug_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] Simulation initialized")
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
    grid.setColumnStretch(1, 3)
    grid.setColumnStretch(2, 2)

    main_widget.setLayout(grid)
    app.setCentralWidget(main_widget)