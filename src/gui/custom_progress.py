# src/gui/custom_progress.py
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import logging

# Set up logging to file for silent crash debugging
logging.basicConfig(filename="custom_progress.log", level=logging.DEBUG, 
                    format="%(asctime)s:%(levelname)s:%(message)s")

class CustomProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_text = ""
        self.marker_position = None
        self.setFormat("")  # Disable default percentage text
        logging.debug("CustomProgressBar initialized")

    def setCustomText(self, text):
        self.custom_text = text
        self.update()
        logging.debug(f"Set custom text: {text}")

    def setMarkerPosition(self, percentage):
        self.marker_position = percentage
        self.update()
        logging.debug(f"Set marker position: {percentage}")

    def paintEvent(self, event):
        logging.debug("Starting paintEvent")
        # Draw base progress bar
        super().paintEvent(event)
        
        # Create painter for custom rendering
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        logging.debug("Painter created")

        # Draw custom text
        if self.custom_text:
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            painter.setPen(Qt.white)
            rect = self.rect()
            painter.drawText(rect, Qt.AlignCenter, self.custom_text)
            logging.debug(f"Drew text: {self.custom_text}")

        # Draw marker if set
        if self.marker_position is not None:
            marker_x = (self.marker_position / 100.0) * self.width()
            painter.setPen(QPen(Qt.white, 2))
            painter.drawLine(int(marker_x), 0, int(marker_x), self.height())
            logging.debug(f"Drew marker at: {marker_x}")

        painter.end()  # Explicitly end painter
        logging.debug("paintEvent completed")