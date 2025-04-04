from ortools.sat.python import cp_model
import numpy as np


def detect_largest_landmass_boundary(grid):
    grid = np.array(grid)
    rows, cols = grid.shape

    def find_largest_landmass():
        visited = set()
        max_size = 0
        largest_landmass = set()

        def dfs(r, c, landmass):
            if (
                r < 0
                or c < 0
                or r >= rows
                or c >= cols
                or grid[r, c] == 0
                or (r, c) in visited
            ):
                return

            visited.add((r, c))
            landmass.add((r, c))

            dfs(r + 1, c, landmass)
            dfs(r - 1, c, landmass)
            dfs(r, c + 1, landmass)
            dfs(r, c - 1, landmass)

        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == 1 and (r, c) not in visited:
                    current_landmass = set()
                    dfs(r, c, current_landmass)

                    if len(current_landmass) > max_size:
                        max_size = len(current_landmass)
                        largest_landmass = current_landmass

        return largest_landmass

    largest_landmass = find_largest_landmass()

    model = cp_model.CpModel()

    cells = {}
    for r in range(rows):
        for c in range(cols):
            cells[r, c] = model.NewBoolVar(f"cell_{r}_{c}")
            model.Add(cells[r, c] == (1 if (r, c) in largest_landmass else 0))

    boundary_edges = []

    for r, c in largest_landmass:
        adjacent_coords = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

        for adj_r, adj_c in adjacent_coords:
            if (
                0 <= adj_r < rows
                and 0 <= adj_c < cols
                and (adj_r, adj_c) not in largest_landmass
            ):
                boundary_edges.append(((r, c), (adj_r, adj_c)))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("\nSolution found")
        return boundary_edges
    else:
        print("\nNo solution found")
        return []


grid = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

boundary_edges = detect_largest_landmass_boundary(grid)

visual_grid = np.zeros((len(grid), len(grid[0])), dtype=str)
visual_grid.fill(" ")

for r in range(len(grid)):
    for c in range(len(grid[0])):
        visual_grid[r, c] = "L" if grid[r][c] == 1 else "W"

for edge in boundary_edges:
    land_r, land_c = edge[0]
    visual_grid[land_r, land_c] = "B"

print()
for row in visual_grid:
    print(" ".join(row))
print()

land = np.count_nonzero(visual_grid.flatten() == "L")
bound = np.count_nonzero(visual_grid.flatten() == "B")

print("Landmass:", land + bound)
print("Boundary:", bound)
