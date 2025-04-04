from ortools.sat.python import cp_model
import numpy as np


def create_data_model(num_cities=10):
    data = {}
    np.random.seed(42)
    data["locations"] = np.random.rand(num_cities, 2) * 100
    num_locations = len(data["locations"])
    dist_matrix = np.zeros((num_locations, num_locations))
    for from_loc in range(num_locations):
        for to_loc in range(num_locations):
            if from_loc == to_loc:
                dist_matrix[from_loc][to_loc] = 0
            else:
                x1, y1 = data["locations"][from_loc]
                x2, y2 = data["locations"][to_loc]
                dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                dist_matrix[from_loc][to_loc] = dist
    data["distance_matrix"] = dist_matrix.astype(int)
    return data


def solve_tsp_with_cp_model(data):
    num_cities = len(data["distance_matrix"])
    model = cp_model.CpModel()

    cities_at_position = {}
    for i in range(num_cities):
        cities_at_position[i] = model.NewIntVar(0, num_cities - 1, f"city_at_pos_{i}")

    model.AddAllDifferent(cities_at_position.values())
    model.Add(cities_at_position[0] == 0)

    total_distance = model.NewIntVar(0, 10000, "total_distance")
    distance_terms = []

    for i in range(num_cities):
        current_city = cities_at_position[i]
        next_city = cities_at_position[(i + 1) % num_cities]

        for from_city in range(num_cities):
            for to_city in range(num_cities):
                if from_city == to_city:
                    continue

                is_connection = model.NewBoolVar(f"conn_{i}_{from_city}_{to_city}")
                b1 = model.NewBoolVar(f"curr_{i}_{from_city}")
                b2 = model.NewBoolVar(f"next_{i}_{to_city}")

                model.Add(current_city == from_city).OnlyEnforceIf(b1)
                model.Add(current_city != from_city).OnlyEnforceIf(b1.Not())

                model.Add(next_city == to_city).OnlyEnforceIf(b2)
                model.Add(next_city != to_city).OnlyEnforceIf(b2.Not())

                model.AddBoolAnd([b1, b2]).OnlyEnforceIf(is_connection)
                model.AddBoolOr([b1.Not(), b2.Not()]).OnlyEnforceIf(is_connection.Not())

                distance = data["distance_matrix"][from_city][to_city]
                term = model.NewIntVar(0, distance, f"dist_{i}_{from_city}_{to_city}")
                model.Add(term == distance).OnlyEnforceIf(is_connection)
                model.Add(term == 0).OnlyEnforceIf(is_connection.Not())

                distance_terms.append(term)

    model.Add(total_distance == sum(distance_terms))
    model.Minimize(total_distance)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        route = []
        for i in range(num_cities):
            city = solver.Value(cities_at_position[i])
            route.append(city)

        total_dist = 0
        for i in range(num_cities):
            from_city = route[i]
            to_city = route[(i + 1) % num_cities]
            total_dist += data["distance_matrix"][from_city][to_city]

        return route, total_dist
    else:
        return None, 0


def main():
    data = create_data_model(10)

    print("Distance Matrix:")
    for row in data["distance_matrix"]:
        print(row)

    route, total_distance = solve_tsp_with_cp_model(data)

    if route:
        print("Route:", route)
        print("Total distance:", total_distance)
    else:
        print("No solution found!")


if __name__ == "__main__":
    main()
