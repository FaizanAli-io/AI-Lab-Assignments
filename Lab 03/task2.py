from copy import deepcopy


def get_tsp_neighbors(state):
    return {
        1: [(2, 10), (3, 15), (4, 20)],
        2: [(1, 10), (4, 25), (3, 35)],
        3: [(1, 15), (2, 35), (4, 30)],
        4: [(1, 20), (2, 25), (3, 30)],
    }[state]


def find_cheapest_cycle():
    paths = [{"path": [node], "cost": 0} for node in range(1, 5)]
    complete_paths = []

    while paths:
        current = paths.pop(0)

        if len(current["path"]) == 5:
            complete_paths.append(current)
            continue

        for node, cost in get_tsp_neighbors(current["path"][-1]):
            root = current["path"][0]
            if (len(current["path"]) == 4 and node == root) or (
                node not in current["path"]
            ):
                new_cost = current["cost"] + cost
                new_path = deepcopy(current["path"]) + [node]
                paths.append({"path": new_path, "cost": new_cost})

    best_path = min(complete_paths, key=lambda x: x["cost"])

    return best_path


if __name__ == "__main__":
    path = find_cheapest_cycle()
    print("The cheapest cyce is:", path)
