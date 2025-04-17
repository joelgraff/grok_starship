import numpy as np
import math
from hull_shapes import HullShape
from utils import is_within_ellipse

class GalacticaHull(HullShape):
    def generate(self):
        """Generate a triangular hull with rounded edges (Galactica-inspired)."""
        center_x, center_y = self.grid_size["width"] // 2, self.grid_size["height"] // 2
        aspect_ratio = self.config["hull_shape"].get("aspect_ratio", 2.0)
        corner_radius = self.config["hull_shape"].get("corner_radius", 0.1) * min(center_x, center_y)

        # Triangle vertices
        width = center_x * 0.8
        height = width / aspect_ratio
        v1 = (center_x, center_y - height)  # Top
        v2 = (center_x - width, center_y + height)  # Bottom left
        v3 = (center_x + width, center_y + height)  # Bottom right

        # Centroid for core
        core_x = (v1[0] + v2[0] + v3[0]) / 3
        core_y = (v1[1] + v2[1] + v3[1]) / 3
        core_semi_axis_x = min(center_x, center_y) * self.core_size
        core_semi_axis_y = core_semi_axis_x / self.semi_axis_ratio

        # Boundary points with rounded corners (rotated 90 degrees clockwise)
        hull_points = []
        num_corner_points = 60
        # Arc at v1 (top): from v2 to v3 (previously 210-330, now 120-240)
        for angle in range(120, 240):
            theta = math.radians(angle)
            hull_x = v1[0] + corner_radius * math.cos(theta)
            hull_y = v1[1] + corner_radius * math.sin(theta)
            hull_points.append((hull_x, hull_y))
        # Arc at v2 (bottom left): from v3 to v1 (previously 330-450, now 240-360)
        for angle in range(240, 360):
            theta = math.radians(angle)
            hull_x = v2[0] + corner_radius * math.cos(theta)
            hull_y = v2[1] + corner_radius * math.sin(theta)
            hull_points.append((hull_x, hull_y))
        # Arc at v3 (bottom right): from v1 to v2 (previously 90-210, now 0-120)
        for angle in range(0, 120):
            theta = math.radians(angle)
            hull_x = v3[0] + corner_radius * math.cos(theta)
            hull_y = v3[1] + corner_radius * math.sin(theta)
            hull_points.append((hull_x, hull_y))

        # Core points
        core_points = []
        for angle in range(360):
            theta = math.radians(angle)
            core_x_point = core_x + core_semi_axis_x * math.cos(theta)
            core_y_point = core_y + core_semi_axis_y * math.sin(theta)
            core_points.append((core_x_point, core_y_point))

        # Set grid size
        all_points = hull_points + core_points
        width, height = self.compute_grid_size(all_points)
        self.layout_grid = np.ones((height, width), dtype=int)

        # Generate the grid
        for y in range(height):
            for x in range(width):
                in_triangle = self.point_in_triangle(x, y, v1, v2, v3)
                near_corner = False
                for v in [v1, v2, v3]:
                    dist = math.sqrt((x - v[0])**2 + (y - v[1])**2)
                    if dist <= corner_radius:  # Include points within corner radius
                        in_triangle = True
                        near_corner = True
                    elif dist > corner_radius and in_triangle:
                        # Exclude points outside the corner radius but inside the triangle's sharp corner
                        in_triangle = False
                if in_triangle:
                    self.layout_grid[y, x] = 0  # Open space
                else:
                    self.layout_grid[y, x] = 1  # Wall
                if is_within_ellipse(x, y, (core_x, core_y), core_semi_axis_x, core_semi_axis_y):
                    self.layout_grid[y, x] = 2  # Central core

        return self.layout_grid, hull_points, core_points, (center_x, center_y)