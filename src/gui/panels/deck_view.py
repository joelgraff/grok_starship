# src/gui/panels/deck_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from ..widgets import PygameWidget

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