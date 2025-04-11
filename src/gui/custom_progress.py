# custom_progress.py
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt

class CustomProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_text = ""
        self.setTextVisible(False)  # Disable default text rendering
        # Set default dark gray background for better text contrast
        self.setStyleSheet("""
            QProgressBar {
                border: 1px solid gray;
                background-color: #444444;
                color: white;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 green, stop:1 yellow);
            }
        """)

    def setCustomText(self, text):
        self.custom_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(self.font())
        painter.setPen(Qt.white)  # White text for contrast
        # Center text within the bar
        text_rect = painter.fontMetrics().boundingRect(self.custom_text)
        x = (self.width() - text_rect.width()) // 2
        y = (self.height() + text_rect.height() // 2) // 2
        painter.drawText(x, y, self.custom_text)