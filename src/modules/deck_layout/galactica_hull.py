import numpy as np
import math
from hull_shapes import HullShape
from utils import is_within_ellipse

class GalacticaHull(HullShape):
    def generate(self):
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

        # Compute angles for each vertex
        # Vector from v1 to v2
        v1_v2 = (v2[0] - v1[0], v2[1] - v1[1])
        v1_v3 = (v3[0] - v1[0], v3[1] - v1[1])
        # Vector from v2 to v1 and v3
        v2_v1 = (v1[0] - v2[0], v1[1] - v2[1])
        v2_v3 = (v3[0] - v2[0], v3[1] - v2[1])
        # Vector from v3 to v1 and v2
        v3_v1 = (v1[0] - v3[0], v1[1] - v3[1])
        v3_v2 = (v2[0] - v3[0], v2[1] - v3[1])

        # Angle at v1 (top)
        angle_v1 = math.degrees(math.atan2(v1_v3[1], v1_v3[0]) - math.atan2(v1_v2[1], v1_v2[0]))
        if angle_v1 < 0:
            angle_v1 += 360
        # Angle at v2 (bottom left)
        angle_v2 = math.degrees(math.atan2(v2_v3[1], v2_v3[0]) - math.atan2(v2_v1[1], v2_v1[0]))
        if angle_v2 < 0:
            angle_v2 += 360
        # Angle at v3 (bottom right)
        angle_v3 = math.degrees(math.atan2(v3_v2[1], v3_v2[0]) - math.atan2(v3_v1[1], v3_v1[0]))
        if angle_v3 < 0:
            angle_v3 += 360

        # Compute bisectors and arc midpoints
        # Top arc (v1): Midpoint vertically above v1
        top_mid_angle = 90  # Vertical (points downward)
        top_start_angle = top_mid_angle - angle_v1 / 2
        top_end_angle = top_mid_angle + angle_v1 / 2

        # Bottom left arc (v2): Bisector of angle at v2
        v2_v1_angle = math.degrees(math.atan2(v2_v1[1], v2_v1[0]))
        v2_v3_angle = math.degrees(math.atan2(v2_v3[1], v2_v3[0]))
        if v2_v1_angle < 0:
            v2_v1_angle += 360
        if v2_v3_angle < 0:
            v2_v3_angle += 360
        v2_bisector = (v2_v1_angle + v2_v3_angle) / 2
        if abs(v2_v1_angle - v2_v3_angle) > 180:
            v2_bisector = (v2_bisector + 180) % 360
        v2_start_angle = v2_bisector - angle_v2 / 2
        v2_end_angle = v2_bisector + angle_v2 / 2

        # Bottom right arc (v3): Bisector of angle at v3
        v3_v1_angle = math.degrees(math.atan2(v3_v1[1], v3_v1[0]))
        v3_v2_angle = math.degrees(math.atan2(v3_v2[1], v3_v2[0]))
        if v3_v1_angle < 0:
            v3_v1_angle += 360
        if v3_v2_angle < 0:
            v3_v2_angle += 360
        v3_bisector = (v3_v1_angle + v3_v2_angle) / 2
        if abs(v3_v1_angle - v3_v2_angle) > 180:
            v3_bisector = (v3_bisector + 180) % 360
        v3_start_angle = v3_bisector - angle_v3 / 2
        v3_end_angle = v3_bisector + angle_v3 / 2

        # Boundary points with rounded corners
        hull_points = []
        num_corner_points = 60
        # Top arc (v1)
        for angle in np.linspace(top_start_angle, top_end_angle, num_corner_points):
            theta = math.radians(angle)
            hull_x = v1[0] + corner_radius * math.cos(theta)
            hull_y = v1[1] + corner_radius * math.sin(theta)
            hull_points.append((hull_x, hull_y))
        # Bottom left arc (v2)
        for angle in np.linspace(v2_start_angle, v2_end_angle, num_corner_points):
            theta = math.radians(angle)
            hull_x = v2[0] + corner_radius * math.cos(theta)
            hull_y = v2[1] + corner_radius * math.sin(theta)
            hull_points.append((hull_x, hull_y))
        # Bottom right arc (v3)
        for angle in np.linspace(v3_start_angle, v3_end_angle, num_corner_points):
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
                    if dist <= corner_radius:
                        in_triangle = True
                        near_corner = True
                    elif dist > corner_radius and in_triangle:
                        in_triangle = False
                if in_triangle:
                    self.layout_grid[y, x] = 0
                else:
                    self.layout_grid[y, x] = 1
                if is_within_ellipse(x, y, (core_x, core_y), core_semi_axis_x, core_semi_axis_y):
                    self.layout_grid[y, x] = 2

        return self.layout_grid, hull_points, core_points, (center_x, center_y)