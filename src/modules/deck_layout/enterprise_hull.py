import numpy as np
import math
from hull_shapes import HullShape
from utils import is_within_ellipse

class EnterpriseHull(HullShape):
    def generate(self):
        """Generate a single elliptical hull (Enterprise-inspired)."""
        center_x, center_y = self.grid_size["width"] // 2, self.grid_size["height"] // 2
        semi_axis_x = center_x
        semi_axis_y = int(semi_axis_x / self.semi_axis_ratio)

        # Core size
        core_semi_axis_y = semi_axis_y * self.core_size
        core_semi_axis_x = core_semi_axis_y * self.semi_axis_ratio

        # Compute boundary points
        hull_points = []
        core_points = []
        num_points = 360
        for angle in range(num_points):
            theta = math.radians(angle)
            hull_x = center_x + semi_axis_x * math.cos(theta)
            hull_y = center_y + semi_axis_y * math.sin(theta)
            hull_points.append((hull_x, hull_y))
            core_x = center_x + core_semi_axis_x * math.cos(theta)
            core_y = center_y + core_semi_axis_y * math.sin(theta)
            core_points.append((core_x, core_y))

        # Set grid size
        width, height = self.compute_grid_size(hull_points)
        self.layout_grid = np.ones((height, width), dtype=int)

        # Generate the grid
        for y in range(height):
            for x in range(width):
                if is_within_ellipse(x, y, (center_x, center_y), semi_axis_x, semi_axis_y):
                    self.layout_grid[y, x] = 0  # Open space
                else:
                    self.layout_grid[y, x] = 1  # Wall
                if is_within_ellipse(x, y, (center_x, center_y), core_semi_axis_x, core_semi_axis_y):
                    self.layout_grid[y, x] = 2  # Central core

        return self.layout_grid, hull_points, core_points, (center_x, center_y)