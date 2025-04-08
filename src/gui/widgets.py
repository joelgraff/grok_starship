# gui/widgets.py
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

    def update_surface(self, ship_position, targets):
        self.surface.fill((255, 255, 255))  # Clear to white
        # Draw ship (blue dot)
        x, y = ship_position
        ship_x = x * 20 + self.width() // 2
        ship_y = y * 20 + self.height() // 2
        pygame.draw.circle(self.surface, (0, 0, 255), (ship_x, ship_y), 10)
        # Draw targets (red dots)
        for target in targets:
            tx, ty = target["position"]
            target_x = tx * 20 + self.width() // 2
            target_y = ty * 20 + self.height() // 2
            pygame.draw.circle(self.surface, (255, 0, 0), (target_x, target_y), 8)
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        image = QImage(self.surface.get_buffer().raw, self.width(), self.height(), QImage.Format_RGB32)
        painter.drawImage(0, 0, image)

    def resizeEvent(self, event):
        self.surface = pygame.Surface((self.width(), self.height()))
        self.surface.fill((255, 255, 255))
        super().resizeEvent(event)