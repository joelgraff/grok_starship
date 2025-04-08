# widgets.py
import pygame
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter

class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        pygame.init()
        self.surface = pygame.Surface((self.width(), self.height()))
        self.surface.fill((255, 255, 255))  # White background

    def update_surface(self, ship_position):
        self.surface.fill((255, 255, 255))  # Clear to white
        x, y = ship_position
        pygame.draw.circle(self.surface, (0, 0, 255), (x * 20 + self.width() // 2, y * 20 + self.height() // 2), 10)
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        image = QImage(self.surface.get_buffer().raw, self.width(), self.height(), QImage.Format_RGB32)
        painter.drawImage(0, 0, image)

    def resizeEvent(self, event):
        self.surface = pygame.Surface((self.width(), self.height()))
        self.surface.fill((255, 255, 255))
        super().resizeEvent(event)