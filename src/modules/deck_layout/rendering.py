import pygame
import logging

logger = logging.getLogger(__name__)

class Renderer:
    def __init__(self, cell_size_layout, cell_size_map, screen_width, screen_height, center=None):
        self.cell_size_layout = cell_size_layout
        self.cell_size_map = cell_size_map
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = center if center else (screen_width // (2 * cell_size_layout), screen_height // (2 * cell_size_layout))
        self.offset_x = 0
        self.offset_y = 0

    def compute_offsets(self, points):
        """Compute offsets to center the points within the screen."""
        if not points:
            return 0, 0
        min_x = min(x for x, y in points)
        max_x = max(x for x, y in points)
        min_y = min(y for x, y in points)
        max_y = max(y for x, y in points)
        hull_width = max_x - min_x
        hull_height = max_y - min_y
        offset_x = (self.screen_width / self.cell_size_layout - hull_width) / 2 - min_x
        offset_y = (self.screen_height / self.cell_size_layout - hull_height) / 2 - min_y
        return offset_x, offset_y

    def render_layout(self, screen, grid, hull_points, core_points, internal_points=None):
        """Render the layout view with single-pixel edges using precomputed points."""
        surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        # Compute offsets to center the hull
        self.offset_x, self.offset_y = self.compute_offsets(hull_points)

        # Apply offset to center the hull
        hull_pixels = [(x + self.offset_x, y + self.offset_y) for x, y in hull_points]
        hull_pixels = [(x * self.cell_size_layout, y * self.cell_size_layout) for x, y in hull_pixels]
        core_pixels = [(x + self.offset_x, y + self.offset_y) for x, y in core_points]
        core_pixels = [(x * self.cell_size_layout, y * self.cell_size_layout) for x, y in core_pixels]

        # Draw filled interiors
        if hull_pixels:
            pygame.draw.polygon(surface, (255, 255, 255, 50), hull_pixels)  # Semi-transparent white fill
            pygame.draw.aalines(surface, (255, 255, 255), True, hull_pixels)  # White single-pixel edges
        if core_pixels:
            pygame.draw.polygon(surface, (100, 100, 255, 100), core_pixels)  # Semi-transparent blue fill
            pygame.draw.aalines(surface, (100, 100, 255), True, core_pixels)  # Blue single-pixel edges

        # Draw internal module boundaries (e.g., for Rocinante) as dashed lines
        if internal_points:
            for module_points in internal_points:
                module_pixels = [(x + self.offset_x, y + self.offset_y) for x, y in module_points]
                module_pixels = [(x * self.cell_size_layout, y * self.cell_size_layout) for x, y in module_pixels]
                pygame.draw.aalines(surface, (255, 255, 255, 100), True, module_pixels)  # Semi-transparent white dashed lines

        # Draw rooms
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                if grid[y, x] == 3:  # Room
                    rect_x = (x + self.offset_x) * self.cell_size_layout
                    rect_y = (y + self.offset_y) * self.cell_size_layout
                    pygame.draw.rect(surface, (255, 165, 0, 100),  # Orange, semi-transparent
                                   (rect_x, rect_y, self.cell_size_layout, self.cell_size_layout))

        screen.blit(surface, (0, 0))

    def render_pathfinding_map(self, screen, grid, hull_points=None):
        """Render the pathfinding map, scaled to fill the window with proper centering."""
        map_surface = pygame.Surface((grid.shape[1] * self.cell_size_map, grid.shape[0] * self.cell_size_map))

        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                value = grid[y, x]
                if value >= 1.0:  # Non-traversable (walls)
                    color = (255, 0, 0)  # Red
                elif value == 0.1:  # Central core
                    color = (150, 150, 255)  # Light blue
                elif value == 0.0:  # Traversable (open space)
                    color = (0, 255, 0)  # Green
                else:  # Placeholder for other costs
                    color = (0, 200, 0)  # Light green
                pygame.draw.rect(map_surface, color,
                               (x * self.cell_size_map, y * self.cell_size_map,
                                self.cell_size_map, self.cell_size_map))

        # Scale the map surface to fit the screen while maintaining aspect ratio
        map_width = grid.shape[1] * self.cell_size_map
        map_height = grid.shape[0] * self.cell_size_map
        scale_factor = min(self.screen_width / map_width, self.screen_height / map_height)  # Removed padding for consistent scaling
        scaled_width = int(map_width * scale_factor)
        scaled_height = int(map_height * scale_factor)
        scaled_surface = pygame.transform.scale(map_surface, (scaled_width, scaled_height))

        # Center the scaled surface using the same offset as the layout view
        if hull_points:
            offset_x, offset_y = self.compute_offsets(hull_points)
            map_offset_x = offset_x * self.cell_size_map * scale_factor / self.cell_size_layout
            map_offset_y = offset_y * self.cell_size_map * scale_factor / self.cell_size_layout
            screen.blit(scaled_surface, (map_offset_x, map_offset_y))
        else:
            offset_x = (self.screen_width - scaled_width) // 2
            offset_y = (self.screen_height - scaled_height) // 2
            screen.blit(scaled_surface, (offset_x, offset_y))

    def render_agents(self, screen, agents):
        """Placeholder for rendering agents."""
        pass

    def render_labels(self, screen, rooms):
        """Render room labels."""
        font = pygame.font.Font(None, 24)
        for room in rooms:
            x = room["x"]
            y = room["y"]
            width = room["width"]
            height = room["height"]
            # Use the same offsets as render_layout
            label_x = (x + self.offset_x + width / 2) * self.cell_size_layout
            label_y = (y + self.offset_y + height / 2) * self.cell_size_layout
            text = font.render(room["name"], True, (255, 255, 0))  # Yellow text
            text_rect = text.get_rect(center=(label_x, label_y))
            screen.blit(text, text_rect)