import numpy as np
import math
from utils import is_within_ellipse

class HullShape:
    def __init__(self, config):
        self.config = config
        self.grid_size = config["grid_size"]
        self.semi_axis_ratio = config["hull_shape"].get("semi_axis_ratio", 1.5)
        self.core_size = config["hull_shape"].get("core_size", 0.1)
        self.layout_grid = None

    def compute_grid_size(self, hull_points):
        """Compute the required grid size based on hull points."""
        if not hull_points:
            return self.grid_size["width"], self.grid_size["height"]
        min_x = min(x for x, y in hull_points)
        max_x = max(x for x, y in hull_points)
        min_y = min(y for x, y in hull_points)
        max_y = max(y for x, y in hull_points)
        width = max(self.grid_size["width"], int(max_x - min_x) + 20)
        height = max(self.grid_size["height"], int(max_y - min_y) + 20)
        return width, height

    def point_in_triangle(self, x, y, v1, v2, v3):
        """Check if a point is inside a triangle using barycentric coordinates."""
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        d1 = sign((x, y), v1, v2)
        d2 = sign((x, y), v2, v3)
        d3 = sign((x, y), v3, v1)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    def point_near_line(self, x, y, p1, p2, width):
        """Check if a point is near a line segment within a given width."""
        x1, y1 = p1
        x2, y2 = p2
        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        denom = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        if denom == 0:
            return False
        dist = num / denom
        if (min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)):
            return dist <= width
        return False

    def convex_hull(self, points):
        """Compute the convex hull of a set of points using Graham scan."""
        if len(points) < 3:
            return points

        # Find the point with the lowest y-coordinate (and lowest x if tied)
        points = sorted(points, key=lambda p: (p[1], p[0]))
        start = points[0]
        points = points[1:]

        # Sort points by polar angle with respect to the start point
        def polar_angle(p):
            x, y = p[0] - start[0], p[1] - start[1]
            return math.atan2(y, x)

        points.sort(key=polar_angle)

        # Initialize the hull with the first three points
        hull = [start]
        for p in points:
            while len(hull) > 1:
                # Check if the last two points and the current point make a counter-clockwise turn
                x1, y1 = hull[-2]
                x2, y2 = hull[-1]
                x3, y3 = p
                cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                if cross <= 0:  # Clockwise or collinear
                    hull.pop()
                else:
                    break
            hull.append(p)

        return hull