# visuals.py
import pygame
from config import SHIP_ZONES

class ShipWindow:
    def __init__(self, model):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 500))
        pygame.display.set_caption("Starship - Interior")
        self.model = model
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((50, 50, 50))
            for x in range(0, 1001, 50):
                pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, 500))
            for y in range(0, 501, 50):
                pygame.draw.line(self.screen, (100, 100, 100), (0, y), (1000, y))
            for zone, ((x1, y1), (x2, y2)) in SHIP_ZONES.items():
                pygame.draw.rect(self.screen, (80, 80, 80), (x1 * 50, y1 * 50, (x2 - x1 + 1) * 50, (y2 - y1 + 1) * 50), 2)
                font = pygame.font.SysFont(None, 20)
                text = font.render(zone, True, (200, 200, 200))
                self.screen.blit(text, (x1 * 50 + 5, y1 * 50 + 5))
            for agent in self.model.schedule.agents:
                x, y = agent.pos
                color = {"Captain": (255, 0, 0), "Navigator": (0, 255, 0), "Engineer": (0, 0, 255),
                         "Communicator": (255, 255, 0), "Scientist": (255, 0, 255), "Crew": (150, 150, 150)}[agent.role]
                pygame.draw.circle(self.screen, color, (x * 50 + 25, y * 50 + 25), 5)
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()