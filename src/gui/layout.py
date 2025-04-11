# src/gui/layout.py
from PyQt5.QtWidgets import QWidget, QGridLayout
from .panels.command_status import setup_command_status_panel
from .panels.navigation_view import setup_navigation_view_panel
from .panels.deck_view import setup_deck_view_panel
from .panels.debug_log import setup_debug_log_panel

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