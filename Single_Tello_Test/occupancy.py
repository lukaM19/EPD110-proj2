import numpy as np

def build_occupancy_matrix(rows, cols, start, end, obstacles):
    grid = np.zeros((rows, cols), dtype=np.uint8)
    inside = lambda r, c: 0 <= r < rows and 0 <= c < cols
    for r, c in obstacles:
        if not inside(r, c):
            raise ValueError(f"Obstacle {(r, c)} outside {rows}x{cols} grid")
        grid[r, c] = 1
    for name, (r, c) in (("start", start), ("end", end)):
        if not inside(r, c) or grid[r, c]:
            raise ValueError(f"{name} {(r, c)} is outside the grid or on an obstacle")
    return grid
