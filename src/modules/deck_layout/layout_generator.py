import numpy as np
import logging
from enterprise_hull import EnterpriseHull
from galactica_hull import GalacticaHull
from rocinante_hull import RocinanteHull

logger = logging.getLogger(__name__)

class LayoutGenerator:
    def __init__(self, config):
        self.config = config
        self.grid_size = config["grid_size"]
        self.hull_type = config["hull_shape"].get("hull_type", "Enterprise")
        self.layout_grid = None
        self.pathfinding_grid = None
        self.rooms = []

    def generate_hull(self):
        """Generate the hull based on hull_type."""
        hull_classes = {
            "Enterprise": EnterpriseHull,
            "Galactica": GalacticaHull,
            "Rocinante": RocinanteHull
        }
        hull_class = hull_classes.get(self.hull_type, EnterpriseHull)
        if self.hull_type not in hull_classes:
            logger.warning(f"Hull type '{self.hull_type}' not supported. Defaulting to Enterprise.")
        else:
            logger.info(f"Generating hull type: {self.hull_type}")
        hull = hull_class(self.config)
        result = hull.generate()
        # Handle different return values based on hull type
        if self.hull_type == "Rocinante":
            self.layout_grid, hull_points, core_points, center, internal_points = result
        else:
            self.layout_grid, hull_points, core_points, center = result
            internal_points = None
        return self.layout_grid, hull_points, core_points, center, internal_points

    def generate_pathfinding_grid(self):
        """Generate the pathfinding grid based on the layout."""
        self.pathfinding_grid = np.ones_like(self.layout_grid, dtype=float)
        for y in range(self.layout_grid.shape[0]):
            for x in range(self.layout_grid.shape[1]):
                if self.layout_grid[y, x] == 0:  # Open space
                    self.pathfinding_grid[y, x] = 0.0
                elif self.layout_grid[y, x] == 2:  # Central core
                    self.pathfinding_grid[y, x] = 0.1
                else:  # Walls
                    self.pathfinding_grid[y, x] = 1.0
        logger.info("Pathfinding grid generated")
        return self.pathfinding_grid

    def modify_grid(self, x, y, width, height, layout_value, pathfinding_value):
        """Modify a region of both grids."""
        try:
            self.layout_grid[y:y+height, x:x+width] = layout_value
            self.pathfinding_grid[y:y+height, x:x+width] = pathfinding_value
            logger.info(f"Grid modified at ({x}, {y}) with size ({width}, {height})")
        except IndexError:
            logger.warning(f"Grid modification out of bounds at ({x}, {y})")

    def place_rooms(self):
        """Place rooms within the hull based on room types from config."""
        room_types = self.config["room_types"]
        large_rooms = room_types["large"]
        small_rooms = room_types["small"]

        large_room_min_size = 10
        large_room_max_size = 20
        small_room_min_size = 5
        small_room_max_size = 10

        core_center = None
        for y in range(self.layout_grid.shape[0]):
            for x in range(self.layout_grid.shape[1]):
                if self.layout_grid[y, x] == 2:
                    core_center = (x, y)
                    break
            if core_center:
                break

        if not core_center:
            core_center = (self.layout_grid.shape[1] // 2, self.layout_grid.shape[0] // 2)
            logger.warning("Core center not found, using grid center.")

        for room_name in large_rooms:
            placed = False
            attempts = 0
            max_attempts = 50
            while not placed and attempts < max_attempts:
                width = np.random.randint(large_room_min_size, large_room_max_size + 1)
                height = np.random.randint(large_room_min_size, large_room_max_size + 1)
                x = int(np.random.normal(core_center[0], self.layout_grid.shape[1] / 10))
                y = int(np.random.normal(core_center[1], self.layout_grid.shape[0] / 10))
                x = max(0, min(x, self.layout_grid.shape[1] - width))
                y = max(0, min(y, self.layout_grid.shape[0] - height))

                suitable = True
                for ry in range(y, y + height):
                    for rx in range(x, x + width):
                        if ry >= self.layout_grid.shape[0] or rx >= self.layout_grid.shape[1]:
                            suitable = False
                            break
                        if self.layout_grid[ry, rx] not in [0, 2]:
                            suitable = False
                            break
                    if not suitable:
                        break

                if suitable:
                    self.modify_grid(x, y, width, height, 3, 0.0)
                    self.rooms.append({
                        "name": room_name,
                        "type": "large",
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height
                    })
                    placed = True
                    logger.info(f"Placed large room '{room_name}' at ({x}, {y}) with size ({width}, {height})")
                attempts += 1

            if not placed:
                logger.warning(f"Could not place large room '{room_name}' after {max_attempts} attempts.")

        for room_name in small_rooms:
            placed = False
            attempts = 0
            max_attempts = 50
            while not placed and attempts < max_attempts:
                width = np.random.randint(small_room_min_size, small_room_max_size + 1)
                height = np.random.randint(small_room_min_size, small_room_max_size + 1)
                x = int(np.random.normal(self.layout_grid.shape[1] / 2, self.layout_grid.shape[1] / 4))
                y = int(np.random.normal(self.layout_grid.shape[0] / 2, self.layout_grid.shape[0] / 4))
                x = max(0, min(x, self.layout_grid.shape[1] - width))
                y = max(0, min(y, self.layout_grid.shape[0] - height))

                suitable = True
                for ry in range(y, y + height):
                    for rx in range(x, x + width):
                        if ry >= self.layout_grid.shape[0] or rx >= self.layout_grid.shape[1]:
                            suitable = False
                            break
                        if self.layout_grid[ry, rx] not in [0]:
                            suitable = False
                            break
                    if not suitable:
                        break

                if suitable:
                    self.modify_grid(x, y, width, height, 3, 0.0)
                    self.rooms.append({
                        "name": room_name,
                        "type": "small",
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height
                    })
                    placed = True
                    logger.info(f"Placed small room '{room_name}' at ({x}, {y}) with size ({width}, {height})")
                attempts += 1

            if not placed:
                logger.warning(f"Could not place small room '{room_name}' after {max_attempts} attempts.")

        return self.rooms

    def generate_corridors(self):
        """Placeholder for corridor generation."""
        pass