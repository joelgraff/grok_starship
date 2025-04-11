# src/gui/panels/command_status.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QFont
from .engineering_status import setup_engineering_status

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
    font = QFont("Arial", 10)
    for module in app.controller.modules:
        module_panel = QWidget()
        color = app.log_colors[module.name].name()
        module_panel.setStyleSheet(f"background-color: {color}; color: white;")
        module_panel_layout = QVBoxLayout()
        if module.name == "Engineering":
            setup_engineering_status(app, module, module_panel_layout, font)
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