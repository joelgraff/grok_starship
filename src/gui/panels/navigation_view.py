# src/gui/panels/navigation_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from ..widgets import PygameWidget

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