from ortools.sat.python import cp_model
import math


def solve_robot_path_csp(grid_size, start, target, obstacles):
    start = (start[0] - 1, start[1] - 1)
    target = (target[0] - 1, target[1] - 1)
    obstacles = [(o[0] - 1, o[1] - 1) for o in obstacles]

    model = cp_model.CpModel()

    max_path_length = grid_size * 2

    is_in_path = {}
    step = {}

    for i in range(grid_size):
        for j in range(grid_size):
            is_in_path[i, j] = model.NewBoolVar(f"path_{i}_{j}")
            step[i, j] = model.NewIntVar(0, max_path_length, f"step_{i}_{j}")

    model.Add(is_in_path[start] == 1)
    model.Add(step[start] == 0)
    model.Add(is_in_path[target] == 1)

    for obs in obstacles:
        model.Add(is_in_path[obs] == 0)

    for i in range(grid_size):
        for j in range(grid_size):
            model.Add(step[i, j] == 0).OnlyEnforceIf(is_in_path[i, j].Not())

    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) != target:
                next_cells = []

                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < grid_size and 0 <= nj < grid_size:
                        next_cell = model.NewBoolVar(f"next_{i}_{j}_to_{ni}_{nj}")
                        model.Add(step[ni, nj] == step[i, j] + 1).OnlyEnforceIf(
                            next_cell
                        )
                        model.Add(is_in_path[ni, nj] == 1).OnlyEnforceIf(next_cell)
                        next_cells.append(next_cell)

                if next_cells:
                    model.Add(sum(next_cells) == is_in_path[i, j]).OnlyEnforceIf(
                        is_in_path[i, j]
                    )

    model.Minimize(step[target])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        path = []
        for i in range(grid_size):
            for j in range(grid_size):
                if solver.Value(is_in_path[i, j]) == 1:
                    path.append((i, j, solver.Value(step[i, j])))

        path.sort(key=lambda x: x[2])

        return [(p[0] + 1, p[1] + 1) for p in path]
    else:
        return None


def main():
    grid_size = 5
    start = (1, 1)
    target = (4, 4)

    obstacles = [(2, 3), (3, 2)]

    path = solve_robot_path_csp(grid_size, start, target, obstacles)

    if path:
        print("Path found:")
        for i, p in enumerate(path):
            print(f"Step {i}: {p}")

        total_cost = (len(path) - 1) * math.sqrt(2)
        print(f"Total cost: {total_cost:.2f}")
    else:
        print("No valid path found.")


if __name__ == "__main__":
    main()
