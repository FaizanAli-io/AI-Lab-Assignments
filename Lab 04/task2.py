import random
import time


def a_star_dynamic(graph, start, goal, heuristic, max_iterations=20):
    frontier = [(start, heuristic[start])]
    visited = set()
    g_costs = {start: 0}
    came_from = {start: None}

    iteration = 0
    while frontier and iteration < max_iterations:
        frontier.sort(key=lambda x: x[1])
        current_node, _ = frontier.pop(0)

        if current_node in visited:
            continue

        print(f"Visiting: {current_node}")
        visited.add(current_node)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"Goal found with A*. Path: {path}")
            return path

        for neighbor in graph[current_node]:
            graph[current_node][neighbor] += random.randint(-1, 2)
            graph[current_node][neighbor] = max(1, graph[current_node][neighbor])

        for neighbor, cost in graph[current_node].items():
            new_g_cost = g_costs[current_node] + cost
            f_cost = new_g_cost + heuristic[neighbor]

            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                came_from[neighbor] = current_node
                frontier.append((neighbor, f_cost))

        iteration += 1
        time.sleep(0.5)

    print("Goal not found within iteration limit.")
    return None


graph = {
    "A": {"B": 2, "C": 4},
    "B": {"A": 2, "D": 7, "E": 3},
    "C": {"A": 4, "E": 1},
    "D": {"B": 7, "F": 2},
    "E": {"B": 3, "C": 1, "F": 5},
    "F": {"D": 2, "E": 5, "G": 1},
    "G": {"F": 1},
}

heuristic = {
    "A": 10,
    "B": 8,
    "C": 7,
    "D": 5,
    "E": 6,
    "F": 3,
    "G": 0,
}

print("\nRunning Dynamic A* Search:")
a_star_dynamic(graph, "A", "G", heuristic)
