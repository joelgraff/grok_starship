# tabs.py
import json
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QTabWidget
from PyQt5.QtGui import QColor
from .widgets import PygameWidget

def setup_ship_status_tab(app):
    ship_tab = QWidget()
    ship_layout = QVBoxLayout()
    app.ship_status_label = QLabel(f"Ship Status: {app.ship.status}")
    ship_layout.addWidget(app.ship_status_label)

    app.command_input = QLineEdit()
    app.command_input.setPlaceholderText("Enter command (e.g., nav set_course 10 20)")
    app.command_input.returnPressed.connect(app.process_command)
    ship_layout.addWidget(app.command_input)

    app.command_output = QLabel("Command output: None")
    ship_layout.addWidget(app.command_output)

    ship_tab.setLayout(ship_layout)
    return ship_tab, "Ship Status"

def setup_module_tabs(app, tabs):
    app.module_labels = {}
    for module in app.controller.modules:
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel(module.get_status())
        layout.addWidget(label)
        tab.setLayout(layout)
        tabs.addTab(tab, module.name)
        app.module_labels[module.name] = label

def setup_navigation_view_tab(app):
    nav_view_tab = QWidget()
    nav_view_layout = QVBoxLayout()
    app.nav_view_label = QLabel("Navigation View (PyGame)")
    nav_view_layout.addWidget(app.nav_view_label)
    app.nav_widget = PygameWidget(app)
    nav_view_layout.addWidget(app.nav_widget)
    nav_view_tab.setLayout(nav_view_layout)
    return nav_view_tab, "Navigation View"

def setup_debug_log_tab(app):
    debug_tab = QWidget()
    debug_layout = QVBoxLayout()

    app.log_filters = {}
    filter_layout = QHBoxLayout()
    app.log_filters["Ship Status"] = QCheckBox("Ship Status")
    app.log_filters["Ship Status"].stateChanged.connect(app.save_filter_settings)
    filter_layout.addWidget(app.log_filters["Ship Status"])
    for module in app.controller.modules:
        app.log_filters[module.name] = QCheckBox(module.name)
        app.log_filters[module.name].stateChanged.connect(app.save_filter_settings)
        filter_layout.addWidget(app.log_filters[module.name])
    debug_layout.addLayout(filter_layout)

    app.load_filter_settings()

    app.debug_log = QTextEdit()
    app.debug_log.setReadOnly(True)
    app.debug_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] Simulation initialized")
    debug_layout.addWidget(app.debug_log)

    clear_button = QPushButton("Clear Log")
    clear_button.clicked.connect(app.debug_log.clear)
    debug_layout.addWidget(clear_button)

    debug_tab.setLayout(debug_layout)
    return debug_tab, "Debug Log"

def setup_gui(app):
    app.tabs = QTabWidget()
    app.setCentralWidget(app.tabs)

    # Ship Status tab
    ship_tab, ship_title = setup_ship_status_tab(app)
    app.tabs.addTab(ship_tab, ship_title)

    # Module tabs
    setup_module_tabs(app, app.tabs)

    # Navigation View tab
    nav_view_tab, nav_title = setup_navigation_view_tab(app)
    app.tabs.addTab(nav_view_tab, nav_title)

    # Debug Log tab
    debug_tab, debug_title = setup_debug_log_tab(app)
    app.tabs.addTab(debug_tab, debug_title)