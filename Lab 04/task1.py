from queue import PriorityQueue
from itertools import permutations


class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


def heuristic(current_pos, end_pos):
    return abs(current_pos[0] - end_pos[0]) + abs(current_pos[1] - end_pos[1])


def best_first_search(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    start_node = Node(start)
    frontier = PriorityQueue()
    frontier.put(start_node)
    visited = set()

    while not frontier.empty():
        current_node = frontier.get()
        current_pos = current_node.position

        if current_pos == end:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        visited.add(current_pos)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if (
                0 <= new_pos[0] < rows
                and 0 <= new_pos[1] < cols
                and maze[new_pos[0]][new_pos[1]] == 0
                and new_pos not in visited
            ):
                new_node = Node(new_pos, current_node)
                new_node.g = current_node.g + 1
                new_node.h = heuristic(new_pos, end)
                new_node.f = new_node.h
                frontier.put(new_node)
                visited.add(new_pos)

    return None


def find_shortest_path_through_goals(maze, start, goals):
    shortest_path = None
    shortest_distance = float("inf")

    for perm in permutations(goals):
        total_path = []
        total_distance = 0
        current_start = start
        valid_path = True

        for goal in perm:
            path = best_first_search(maze, current_start, goal)
            if path is None:
                valid_path = False
                break
            total_path.extend(path[:-1])
            total_distance += len(path) - 1
            current_start = goal

        if valid_path and total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = total_path + [perm[-1]]

    return shortest_path, shortest_distance


maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
]

start = (0, 0)
goals = [(4, 4), (2, 3), (1, 4)]

path, cost = find_shortest_path_through_goals(maze, start, goals)
print("Shortest path through all goals:", path)
print("Lowest cost through all goals:", cost)
