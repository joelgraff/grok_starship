# custom_progress.py
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt

class CustomProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_text = ""
        self.setTextVisible(False)  # Disable default text rendering

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