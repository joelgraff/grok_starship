import numpy as np
import math
from hull_shapes import HullShape
from utils import is_within_ellipse

class RocinanteHull(HullShape):
    def generate(self):
        """Generate a cluster of modules (Rocinante-inspired)."""
        center_x, center_y = self.grid_size["width"] // 2, self.grid_size["height"] // 2
        num_modules = 3
        module_types = self.config["hull_shape"].get("module_types", ["ellipse", "rectangle"])
        base_size = min(center_x, center_y) * 0.3

        # Generate modules
        modules = []
        for i in range(num_modules):
            angle = math.radians(i * 360 / num_modules)
            size = base_size * 0.8
            m_center_x = center_x + (base_size * 1.2) * math.cos(angle)
            m_center_y = center_y + (base_size * 1.2) * math.sin(angle)
            m_type = module_types[i % len(module_types)]
            modules.append({
                "center": (m_center_x, m_center_y),
                "size": size,
                "type": m_type
            })

        # Core in the first module
        core_x, core_y = modules[0]["center"]
        core_semi_axis_x = base_size * self.core_size
        core_semi_axis_y = core_semi_axis_x / self.semi_axis_ratio

        # Generate individual module points
        module_points = []
        for module in modules:
            m_center_x, m_center_y = module["center"]
            size = module["size"]
            points = []
            num_points = 90 if module["type"] == "rectangle" else 360
            for angle in range(num_points):
                theta = math.radians(angle)
                if module["type"] == "ellipse":
                    m_x = m_center_x + size * math.cos(theta)
                    m_y = m_center_y + (size / self.semi_axis_ratio) * math.sin(theta)
                else:
                    m_x = m_center_x + size * (1 if angle < 90 or angle >= 270 else -1)
                    m_y = m_center_y + (size / self.semi_axis_ratio) * (1 if 0 <= angle < 180 else -1)
                points.append((m_x, m_y))
            module_points.append(points)

        # Combine all points and compute convex hull
        all_points = []
        for points in module_points:
            all_points.extend(points)
        hull_points = self.convex_hull(all_points)

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
                in_module = False
                for module in modules:
                    m_center_x, m_center_y = module["center"]
                    size = module["size"]
                    if module["type"] == "ellipse":
                        if is_within_ellipse(x, y, (m_center_x, m_center_y), size, size / self.semi_axis_ratio):
                            in_module = True
                    else:
                        dx = abs(x - m_center_x)
                        dy = abs(y - m_center_y)
                        if dx <= size and dy <= size / self.semi_axis_ratio:
                            in_module = True
                in_corridor = False
                for i in range(len(modules)):
                    curr_module = modules[i]
                    next_module = modules[(i + 1) % len(modules)]
                    p1 = curr_module["center"]
                    p2 = next_module["center"]
                    corridor_width = base_size * 0.2
                    if self.point_near_line(x, y, p1, p2, corridor_width):
                        in_corridor = True
                if in_module or in_corridor:
                    self.layout_grid[y, x] = 0  # Open space
                else:
                    self.layout_grid[y, x] = 1  # Wall
                if is_within_ellipse(x, y, (core_x, core_y), core_semi_axis_x, core_semi_axis_y):
                    self.layout_grid[y, x] = 2  # Central core

        return self.layout_grid, hull_points, core_points, (center_x, center_y), module_points  # Return module points for rendering