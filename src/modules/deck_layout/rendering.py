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
        surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        self.offset_x, self.offset_y = self.compute_offsets(hull_points)

        hull_pixels = [(x + self.offset_x, y + self.offset_y) for x, y in hull_points]
        hull_pixels = [(x * self.cell_size_layout, y * self.cell_size_layout) for x, y in hull_pixels]
        core_pixels = [(x + self.offset_x, y + self.offset_y) for x, y in core_points]
        core_pixels = [(x * self.cell_size_layout, y * self.cell_size_layout) for x, y in core_pixels]

        if hull_pixels:
            pygame.draw.polygon(surface, (255, 255, 255, 50), hull_pixels)
            pygame.draw.aalines(surface, (255, 255, 255), True, hull_pixels)
        if core_pixels:
            pygame.draw.polygon(surface, (100, 100, 255, 100), core_pixels)
            pygame.draw.aalines(surface, (100, 100, 255), True, core_pixels)

        if internal_points:
            for module_points in internal_points:
                module_pixels = [(x + self.offset_x, y + self.offset_y) for x, y in module_points]
                module_pixels = [(x * self.cell_size_layout, y * self.cell_size_layout) for x, y in module_pixels]
                pygame.draw.aalines(surface, (255, 255, 255, 100), True, module_pixels)

        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                rect_x = (x + self.offset_x) * self.cell_size_layout
                rect_y = (y + self.offset_y) * self.cell_size_layout
                if grid[y, x] == 3:
                    pygame.draw.rect(surface, (255, 165, 0, 100),
                                   (rect_x, rect_y, self.cell_size_layout, self.cell_size_layout))
                elif grid[y, x] == 4:
                    pygame.draw.rect(surface, (0, 255, 255, 100),
                                   (rect_x, rect_y, self.cell_size_layout, self.cell_size_layout))

        screen.blit(surface, (0, 0))

    def render_pathfinding_map(self, screen, grid, hull_points=None):
        map_surface = pygame.Surface((grid.shape[1] * self.cell_size_map, grid.shape[0] * self.cell_size_map))

        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                value = grid[y, x]
                if value >= 1.0:
                    color = (255, 0, 0)
                elif value == 0.1:
                    color = (150, 150, 255)
                elif value == 0.0:
                    color = (0, 255, 0)
                else:
                    color = (0, 200, 0)
                pygame.draw.rect(map_surface, color,
                               (x * self.cell_size_map, y * self.cell_size_map,
                                self.cell_size_map, self.cell_size_map))

        map_width = grid.shape[1] * self.cell_size_map
        map_height = grid.shape[0] * self.cell_size_map
        scale_factor = min(self.screen_width / map_width, self.screen_height / map_height)
        scaled_width = int(map_width * scale_factor)
        scaled_height = int(map_height * scale_factor)
        scaled_surface = pygame.transform.scale(map_surface, (scaled_width, scaled_height))

        # Center the map using the same offset as the layout, adjusted for scale
        if hull_points:
            offset_x, offset_y = self.compute_offsets(hull_points)
            # Adjust the offset for the map's scale
            map_scale_adjustment = self.cell_size_map / self.cell_size_layout
            map_offset_x = (offset_x * self.cell_size_layout * scale_factor) / self.cell_size_layout
            map_offset_y = (offset_y * self.cell_size_layout * scale_factor) / self.cell_size_layout
            screen.blit(scaled_surface, (map_offset_x, map_offset_y))
        else:
            offset_x = (self.screen_width - scaled_width) // 2
            offset_y = (self.screen_height - scaled_height) // 2
            screen.blit(scaled_surface, (offset_x, offset_y))

    def render_agents(self, screen, agents):
        pass

    def render_labels(self, screen, rooms):
        font = pygame.font.Font(None, 24)
        for room in rooms:
            x = room["x"]
            y = room["y"]
            width = room["width"]
            height = room["height"]
            label_x = (x + self.offset_x + width / 2) * self.cell_size_layout
            label_y = (y + self.offset_y + height / 2) * self.cell_size_layout
            text = font.render(room["name"], True, (255, 255, 0))
            text_rect = text.get_rect(center=(label_x, label_y))
            screen.blit(text, text_rect)