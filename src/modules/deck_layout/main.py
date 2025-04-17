import pygame
import os
import json
import logging
from layout_generator import LayoutGenerator
from rendering import Renderer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path="config.json"):
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_path, config_path)
        with open(full_path, 'r') as f:
            config = json.load(f)
        logger.info("Configuration loaded successfully")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {full_path}")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in configuration file")
        raise

def main():
    config = load_config()
    pygame.init()
    cell_size_layout = config["rendering"]["cell_size_layout"]
    cell_size_map = config["rendering"]["cell_size_map"]

    layout_generator = LayoutGenerator(config)
    layout_grid, hull_points, core_points, center, internal_points = layout_generator.generate_hull()
    pathfinding_grid = layout_generator.generate_pathfinding_grid()
    rooms = layout_generator.place_rooms()

    screen_width = layout_grid.shape[1] * cell_size_layout
    screen_height = layout_grid.shape[0] * cell_size_layout
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Starship Layout Generator")
    clock = pygame.time.Clock()

    renderer = Renderer(cell_size_layout, cell_size_map, screen_width, screen_height, center)
    view_mode = "layout"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    view_mode = "map" if view_mode == "layout" else "layout"
                    logger.info(f"Switched to {view_mode} view")

        screen.fill((0, 0, 0))

        if view_mode == "layout":
            renderer.render_layout(screen, layout_grid, hull_points, core_points, internal_points)
            renderer.render_labels(screen, rooms)
        else:
            renderer.render_pathfinding_map(screen, pathfinding_grid, hull_points)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    logger.info("Program terminated")

if __name__ == "__main__":
    main()