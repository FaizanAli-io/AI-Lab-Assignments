def get_neighbors(state):
    return {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F", "G"],
        "D": [],
        "E": ["H"],
        "F": [],
        "G": [],
        "H": [],
    }[state]


def depth_limited_search(initial, goal, limit):
    stack = [(initial, [initial], 0)]
    seen = set()

    while stack:
        state, path, depth = stack.pop()

        if state == goal:
            return path

        if depth < limit:
            seen.add(state)

            for neighbor in get_neighbors(state):
                if neighbor not in seen:
                    stack.append((neighbor, path + [neighbor], depth + 1))

    return None


def iterative_depth_limited_search(initial, goal):
    for i in range(1, 5):
        result = depth_limited_search(initial, goal, i)
        if result:
            print(f"Found path to target at depth {i}: {result}")
            break
        else:
            print(f"Failed to find path at depth {i}")


if __name__ == "__main__":
    iterative_depth_limited_search("A", "H")
