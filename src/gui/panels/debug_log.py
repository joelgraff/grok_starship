# src/gui/panels/debug_log.py
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from ..utils import update_button_style

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