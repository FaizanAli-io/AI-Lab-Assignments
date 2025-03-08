from queue import PriorityQueue


def heuristic(current_pos, end_pos):
    return abs(current_pos[0] - end_pos[0]) + abs(current_pos[1] - end_pos[1])


def greedy_best_first_search(maze, start, deliveries):
    rows, cols = len(maze), len(maze[0])
    frontier = PriorityQueue()
    frontier.put((0, start))
    visited = set()
    path = []

    while not frontier.empty() and deliveries:
        _, current_pos = frontier.get()

        if current_pos in visited:
            continue

        path.append(current_pos)
        visited.add(current_pos)

        if current_pos in deliveries:
            delivery_time = deliveries[current_pos]
            print(f"Delivered at {current_pos} within time window {delivery_time}")
            del deliveries[current_pos]

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if (
                0 <= new_pos[0] < rows
                and 0 <= new_pos[1] < cols
                and maze[new_pos[0]][new_pos[1]] == 0
                and new_pos not in visited
            ):
                priority = (
                    min([heuristic(new_pos, d) for d in deliveries])
                    if deliveries
                    else 0
                )
                frontier.put((priority, new_pos))

    return path


maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
]

start = (0, 0)
deliveries = {
    (4, 4): (8, 12),
    (2, 3): (5, 10),
    (1, 4): (3, 7),
}

print("Optimized Delivery Route:")
route = greedy_best_first_search(maze, start, deliveries)
print("Route taken:", route)
