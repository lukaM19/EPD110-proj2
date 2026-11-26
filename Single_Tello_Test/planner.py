def plan_route(grid, start, goal):
    """A* on a 4-connected grid. grid[row][col] == 1 is an obstacle.
    Returns a list of (row, col) cells from start to goal (inclusive), or None if unreachable."""

    def h(cell):
        r, c = cell
        return abs(r - goal[0]) + abs(c - goal[1])

    def neighbours(cell):
        r, c = cell

        # Movements of the "current" cell selected
        moves = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        result = []

        # Transformation of the current cell with the movements listed
        for dr, dc in moves:
            nr = r + dr
            nc = c + dc

            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if grid[nr][nc] == 0:
                    result.append((nr, nc))

        return result

    # Initilaising lists needed to save cells.

    open_list = [start]

    # New cells and their cost to get to them from the start position

    g = {
        start: 0
    }

    # Where we identify new cells and their parent cell

    parent = {}

    current = start

    # A* algorithm

    while open_list:

        # Find the cell with the lowest f
        current = open_list[0]

        for cell in open_list:
            if g[cell] + h(cell) < g[current] + h(current):
                current = cell

        # Have we reached the goal?
        if current == goal:
            break

        # Remove current from open_list so we can start testing it
        open_list.remove(current)

        # Explore the neighbours
        for nb in neighbours(current):

            # Calculate the proposed cost
            new_g = g[current] + 1

            # Is this a new cell or a cheaper route?
            if nb not in g or new_g < g[nb]:

                g[nb] = new_g
                parent[nb] = current

                if nb not in open_list:
                    open_list.append(nb)

    # Reconstruct the path

    if current == goal:

        path = []
        current = goal

        while current in parent:
            path.append(current)
            current = parent[current]

        path.append(start)
        path.reverse()

        return path

    return None