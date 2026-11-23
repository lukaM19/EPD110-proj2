grid = [
    [0, 0, 1, 1, 1, 1, 0, 0, 1, 1],   # y=0
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],   # y=1
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1],   # y=2
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],   # y=3
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 1],   # y=4
    [1, 0, 1, 0, 1, 1, 0, 0, 1, 0],   # y=5
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0],   # y=6
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],   # y=7
]
start = (0, 0)
goal = (9, 7)




def h(cell):
    x, y = cell
    return abs(x - goal[0]) + abs(y - goal[1])

def neighbours(cell):
    x, y = cell

    # Movements of the "current" cell selected
    moves = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    result = []

    # Transformation of the current cell with the movements listed
    for dx, dy in moves:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            if grid[ny][nx] == 0:
                result.append((nx, ny))

    return result






# Initilaising lists needed to save cells.

open_list = [start]

# New cells and their cost to get to them from the start position

g = {
    start: 0
}

# Where we identify new cells and their parent cell

parent = {}


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

    print("Shortest path:", path)
    print("Total cost:", g[goal])

else:
    print("No path found")

