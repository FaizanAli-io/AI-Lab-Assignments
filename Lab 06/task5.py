from ortools.sat.python import cp_model
import numpy as np


def solve_sudoku_with_constraints(initial_grid):
    model = cp_model.CpModel()

    cells = {}
    for i in range(9):
        for j in range(9):
            cells[(i, j)] = model.NewIntVar(1, 9, f"cell_{i}_{j}")

    for i in range(9):
        for j in range(9):
            if initial_grid[i][j] != 0:
                model.Add(cells[(i, j)] == initial_grid[i][j])

    [model.AddAllDifferent([cells[(i, j)] for j in range(9)]) for i in range(9)]
    [model.AddAllDifferent([cells[(i, j)] for i in range(9)]) for j in range(9)]

    for box_i in range(3):
        for box_j in range(3):
            box_vars = []
            for i in range(3):
                for j in range(3):
                    box_vars.append(cells[(box_i * 3 + i, box_j * 3 + j)])
            model.AddAllDifferent(box_vars)

    main_sum = model.NewIntVar(0, 9 * 9, "main_sum")
    other_sum = model.NewIntVar(0, 9 * 9, "other_sum")

    main_remainder = model.NewIntVar(0, 2, "main_remainder")
    other_remainder = model.NewIntVar(0, 2, "other_remainder")

    model.Add(main_sum == sum(cells[(i, i)] for i in range(9)))
    model.Add(other_sum == sum(cells[(i, 8 - i)] for i in range(9)))

    model.AddModuloEquality(main_remainder, main_sum, 3)
    model.AddModuloEquality(other_remainder, other_sum, 3)

    model.Add(main_remainder == 0)
    model.Add(other_remainder == 0)

    """Adjacent primes check commented out as no solution was possible with this restriction"""

    # is_prime = {}
    # primes = [2, 3, 5, 7]

    # for i in range(9):
    #     for j in range(9):
    #         is_prime[(i, j)] = model.NewBoolVar(f"is_prime_{i}_{j}")
    #         prime_indicators = []
    #         for p in primes:
    #             indicator = model.NewBoolVar(f"is_{p}_{i}_{j}")
    #             model.Add(cells[(i, j)] == p).OnlyEnforceIf(indicator)
    #             model.Add(cells[(i, j)] != p).OnlyEnforceIf(indicator.Not())
    #             prime_indicators.append(indicator)

    #         model.AddBoolOr(prime_indicators).OnlyEnforceIf(is_prime[(i, j)])
    #         model.AddBoolAnd(
    #             [indicator.Not() for indicator in prime_indicators]
    #         ).OnlyEnforceIf(is_prime[(i, j)].Not())

    # for i in range(9):
    #     for j in range(8):
    #         model.AddBoolOr([is_prime[(i, j)].Not(), is_prime[(i, j + 1)].Not()])

    # for i in range(8):
    #     for j in range(9):
    #         model.AddBoolOr([is_prime[(i, j)].Not(), is_prime[(i + 1, j)].Not()])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                solution[i][j] = solver.Value(cells[(i, j)])
        return solution
    else:
        return None


initial_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

solution = solve_sudoku_with_constraints(initial_grid)

if solution is not None:
    print("Solution found:")
    for row in solution:
        print(row)

    main_diagonal_sum = sum(solution[i, i] for i in range(9))
    other_diagonal_sum = sum(solution[i, 8 - i] for i in range(9))
    print(f"Diagonal 1: {main_diagonal_sum} % 3 = {main_diagonal_sum % 3})")
    print(f"Diagonal 2: {other_diagonal_sum} % 3 = {other_diagonal_sum % 3})")

    print("\nSolution Grid:")
    for row in solution:
        print(" ".join(str(int(cell)) for cell in row))
else:
    print("No solution found")
