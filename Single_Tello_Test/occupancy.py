import math
import numpy as np


def world_to_cell(point, x_min, y_min, cell_cm):
    """(x, y) in cm -> (row, col). Rows follow y, columns follow x."""
    x, y = point
    return math.floor((y - y_min) / cell_cm + 0.5), math.floor((x - x_min) / cell_cm + 0.5)


def cell_to_world(cell, x_min, y_min, cell_cm):
    row, col = cell
    return x_min + col * cell_cm, y_min + row * cell_cm


def build_occupancy_matrix(x_min, x_max, y_min, y_max, start, end, obstacles, cell_cm=50):
    """Returns (grid, start_cell, end_cell). grid[row, col] is 1 for obstacles, 0 otherwise."""
    rows = int((y_max - y_min) // cell_cm) + 1
    cols = int((x_max - x_min) // cell_cm) + 1
    grid = np.zeros((rows, cols), dtype=np.uint8)

    def to_cell(point, name):
        r, c = world_to_cell(point, x_min, y_min, cell_cm)
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError(f"{name} {point} is outside x[{x_min},{x_max}] y[{y_min},{y_max}]")
        return r, c

    for p in obstacles:
        grid[to_cell(p, "Obstacle")] = 1

    start_cell, end_cell = to_cell(start, "Start"), to_cell(end, "Finish")
    for name, cell in (("Start", start_cell), ("Finish", end_cell)):
        if grid[cell]:
            raise ValueError(f"{name} {cell} is on an obstacle")
    return grid, start_cell, end_cell