# gui/widgets.py
import pygame
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter

class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)  # Match new size
        pygame.init()
        self.surface = pygame.Surface((self.width(), self.height()), pygame.SRCALPHA)  # Use alpha for better compatibility
        self.surface.fill((255, 255, 255))  # White background
        self.mode = "navigation"

    def update_surface(self, ship_position=None, targets=None, deck_paths=None):
        self.surface.fill((255, 255, 255))  # Clear to white
        if self.mode == "navigation" and ship_position and targets is not None:
            x, y = ship_position
            ship_x = x * 20 + self.width() // 2
            ship_y = y * 20 + self.height() // 2
            pygame.draw.circle(self.surface, (0, 0, 255), (ship_x, ship_y), 10)
            for target in targets:
                tx, ty = target["position"]
                target_x = tx * 20 + self.width() // 2
                target_y = ty * 20 + self.height() // 2
                pygame.draw.circle(self.surface, (255, 0, 0), (target_x, target_y), 8)
        elif self.mode == "deck" and deck_paths:
            grid_size = self.height() // 5  # Fit height (400px)
            for i in range(6):
                pygame.draw.line(self.surface, (0, 0, 0), (0, i * grid_size), (self.width(), i * grid_size), 2)  # Rows
                pygame.draw.line(self.surface, (0, 0, 0), (i * grid_size, 0), (i * grid_size, self.height()), 2)  # Cols
            color = (0, 255, 0) if deck_paths["corridor_a"] == "open" else (255, 0, 0)
            pygame.draw.rect(self.surface, color, (grid_size, grid_size * 2, grid_size * 3, grid_size))
            print(f"Deck View updated: corridor_a = {deck_paths['corridor_a']}")  # Debug
        self.update()  # Trigger paintEvent

    def set_mode(self, mode):
        self.mode = mode

    def paintEvent(self, event):
        painter = QPainter(self)
        # Convert PyGame surface to QImage with proper format
        data = pygame.image.tostring(self.surface, "RGBA")
        image = QImage(data, self.width(), self.height(), QImage.Format_RGBA8888)
        painter.drawImage(0, 0, image)

    def resizeEvent(self, event):
        self.surface = pygame.Surface((self.width(), self.height()), pygame.SRCALPHA)
        self.surface.fill((255, 255, 255))
        super().resizeEvent(event)