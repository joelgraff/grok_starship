# src/interface.py
import pygame
from src.simulation import StarshipSimulation

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

class StarshipInterface:
    def __init__(self, simulation):
        self.simulation = simulation
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))  # Wider for status panel
        pygame.display.set_caption("Starship Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 15)
        self.paused = False

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw decks
        deck_height = 500 // len(self.simulation.ship.layout["decks"])
        for i, deck in enumerate(self.simulation.ship.layout["decks"]):
            y_base = i * deck_height + 50  # Offset from top
            pygame.draw.rect(self.screen, GRAY, (0, y_base, 500, deck_height), 2)  # Deck outline
            label = self.font.render(deck["name"], True, WHITE)
            self.screen.blit(label, (10, y_base + 5))
            # Draw rooms
            for room in deck["grid"]:
                x, y = room["x"] * 30 + 20, y_base + room["y"] * 30
                pygame.draw.rect(self.screen, WHITE, (x, y, 20, 20))
                # Draw connections (simplified)
                for conn in room["connections"]:
                    cx, cy = conn["x"] * 30 + 30, y_base + conn["y"] * 30 + 10
                    pygame.draw.line(self.screen, GRAY, (x + 10, y + 10), (cx, cy), 1)

        # Draw crew
        for agent in self.simulation.crew:
            if agent.health > 0:
                deck_idx = agent.position[0] - 1  # Deck ID starts at 1
                x = agent.position[1] * 30 + 25  # Scale position
                y = deck_idx * deck_height + agent.position[2] * 30 + 60
                pygame.draw.circle(self.screen, GREEN, (int(x), int(y)), 5)
                # Task progress as text above crew
                if agent.task:
                    progress_text = self.font.render(f"{agent.task.progress}%", True, WHITE)
                    self.screen.blit(progress_text, (x - 10, y - 20))

        # Draw system status and crew info
        y = 10
        for system, data in self.simulation.ship.systems.items():
            color = GREEN if data["integrity"] > 50 else RED
            status = self.font.render(f"{system}: {data['status']} ({data['integrity']}%)", True, color)
            self.screen.blit(status, (520, y))
            y += 20

        # Crew status
        y += 20
        for agent in self.simulation.crew:
            if agent.health > 0:
                task_str = f"{agent.task.name} ({agent.task.progress}%)" if agent.task else "None"
                crew_text = self.font.render(
                    f"{agent.name}: H={agent.health}, M={agent.mood}, T={task_str}", True, WHITE
                )
                self.screen.blit(crew_text, (520, y))
                y += 20

        # Pause button
        pause_text = self.font.render("Pause" if not self.paused else "Resume", True, WHITE)
        pygame.draw.rect(self.screen, BLUE, (900, 550, 80, 30))
        self.screen.blit(pause_text, (910, 555))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 900 <= event.pos[0] <= 980 and 550 <= event.pos[1] <= 580:  # Pause button
                        self.paused = not self.paused

            if not self.paused:
                self.simulation.step()
            self.draw()
            self.clock.tick(30)  # 30 FPS

        pygame.quit()