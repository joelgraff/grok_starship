import pygame
import logging

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, position, color=(255, 0, 0)):
        self.position = position  # (x, y) in grid coordinates
        self.color = color
        self.path = []

    def update(self):
        """Placeholder for agent movement."""
        pass

    def draw(self, screen, cell_size):
        """Render the agent as a circle."""
        pixel_x = self.position[0] * cell_size + cell_size // 2
        pixel_y = self.position[1] * cell_size + cell_size // 2
        pygame.draw.circle(screen, self.color, (pixel_x, pixel_y), cell_size // 2)