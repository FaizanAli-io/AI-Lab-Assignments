import heapq
import random
import time


def a_star_real_time_traffic(graph, start, goal, heuristic, max_iterations=50):
    frontier = []
    heapq.heappush(frontier, (heuristic[start], start))
    visited = set()
    g_costs = {start: 0}
    came_from = {start: None}
    iteration = 0

    while frontier and iteration < max_iterations:
        _, current_node = heapq.heappop(frontier)

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
            print(f"Goal found! Fastest route: {path}")
            return path

        for neighbor in graph[current_node]:
            traffic_change = random.randint(-2, 3)
            graph[current_node][neighbor] = max(
                1, graph[current_node][neighbor] + traffic_change
            )

        for neighbor, cost in graph[current_node].items():
            new_g_cost = g_costs[current_node] + cost
            f_cost = new_g_cost + heuristic[neighbor]

            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                came_from[neighbor] = current_node
                heapq.heappush(frontier, (f_cost, neighbor))

        iteration += 1
        time.sleep(0.5)

    print("Goal not found within iteration limit.")
    return None


graph = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "D": 5, "E": 10},
    "C": {"A": 2, "E": 8},
    "D": {"B": 5, "F": 6},
    "E": {"B": 10, "C": 8, "F": 3},
    "F": {"D": 6, "E": 3, "G": 2},
    "G": {"F": 2},
}

heuristic = {"A": 10, "B": 8, "C": 7, "D": 5, "E": 6, "F": 3, "G": 0}

print("\nRunning A* with Real-Time Traffic Updates:")
a_star_real_time_traffic(graph, "A", "G", heuristic)
