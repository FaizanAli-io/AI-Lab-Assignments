import random
import math
import time


def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_route_distance(route, points):
    total_distance = 0
    for i in range(len(route)):
        total_distance += calculate_distance(
            points[route[i]], points[route[(i + 1) % len(route)]]
        )
    return total_distance


def generate_initial_route(num_points):
    route = list(range(num_points))
    random.shuffle(route)
    return route


def get_neighbor(route):
    neighbor = route.copy()
    i, j = random.sample(range(len(route)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor


def hill_climbing(points, max_iterations=10000, max_no_improve=1000):
    current_route = generate_initial_route(len(points))
    current_distance = calculate_route_distance(current_route, points)

    best_route = current_route.copy()
    best_distance = current_distance

    iterations = 0
    no_improve = 0

    start_time = time.time()

    while iterations < max_iterations and no_improve < max_no_improve:
        neighbor_route = get_neighbor(current_route)
        neighbor_distance = calculate_route_distance(neighbor_route, points)

        if neighbor_distance < current_distance:
            current_route = neighbor_route
            current_distance = neighbor_distance
            no_improve = 0

            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance
        else:
            no_improve += 1

        if iterations % 100 == 0:
            print(f"{iterations}: {best_distance}")

        iterations += 1

    execution_time = time.time() - start_time

    return {
        "best_route": best_route,
        "best_distance": best_distance,
        "iterations": iterations,
        "execution_time": execution_time,
    }


def optimize_delivery_route(delivery_points):
    result = hill_climbing(delivery_points)

    return result["best_route"], result["best_distance"]


def main():
    delivery_points = [
        (0, 0),
        (10, 20),
        (20, 30),
        (30, 10),
        (40, 50),
        (50, 20),
        (20, 40),
        (15, 60),
        (30, 70),
        (45, 35),
    ]

    print(f"Number of delivery points: {len(delivery_points)}")
    print("Finding optimal route...")

    optimized_route, total_distance = optimize_delivery_route(delivery_points)

    print("\nOptimized Delivery Route:")
    print(f"Route order: {optimized_route}")
    print(f"Total distance: {total_distance:.2f} units")

    print("\nDelivery Sequence:")
    for i, point_idx in enumerate(optimized_route):
        print(f"{i+1}. Point {point_idx}: {delivery_points[point_idx]}")

    start_idx = optimized_route[0]
    print(f"{len(optimized_route)+1}. Return to start: {delivery_points[start_idx]}")


if __name__ == "__main__":
    main()
