def update_grid(grid, boundary_condition):
    rows, cols = grid.shape
    new_grid = grid.copy()

    def get_neighbors(row, col):
        neighbors = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc

                if boundary_condition == "periodic":
                    nr, nc = nr % rows, nc % cols  # zawijanie

                elif boundary_condition == "reflective":
                    if nr < 0:
                        nr = 0
                    elif nr >= rows:
                        nr = rows - 1
                    if nc < 0:
                        nc = 0
                    elif nc >= cols:
                        nc = cols - 1
                neighbors += grid[nr, nc]
        return neighbors

    for r in range(rows):
        for c in range(cols):
            num_alive_neighbors = get_neighbors(r, c)
            if grid[r, c] == 1 and (num_alive_neighbors < 2 or num_alive_neighbors > 3):
                new_grid[r, c] = 0
            elif grid[r, c] == 0 and num_alive_neighbors == 3:
                new_grid[r, c] = 1
    return new_grid
