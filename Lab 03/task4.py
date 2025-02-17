grid = [
    ["S", 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 0, "G"],
]


def path_finder(start):
    w = len(grid[0])
    h = len(grid)

    seen = set()
    queue = [start]
    parent = {start: None}

    while queue:
        state = queue.pop(0)
        seen.add(state)
        i, j = state

        if grid[i][j] == "G":
            path = []
            while state:
                path.append(state)
                state = parent[state]
            path.reverse()
            print("Path to goal:", path)
            return

        if i + 1 < h and grid[i + 1][j] != 1:
            new_state = i + 1, j
            if new_state not in seen:
                queue.append(new_state)
                parent[new_state] = state

        if i - 1 >= 0 and grid[i - 1][j] != 1:
            new_state = i - 1, j
            if new_state not in seen:
                queue.append(new_state)
                parent[new_state] = state

        if j + 1 < w and grid[i][j + 1] != 1:
            new_state = i, j + 1
            if new_state not in seen:
                queue.append(new_state)
                parent[new_state] = state

        if j - 1 >= 0 and grid[i][j - 1] != 1:
            new_state = i, j - 1
            if new_state not in seen:
                queue.append(new_state)
                parent[new_state] = state


if __name__ == "__main__":
    path_finder((0, 0))
