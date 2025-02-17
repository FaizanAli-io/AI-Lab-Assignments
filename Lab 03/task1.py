class Environment:
    def get_neighbors(self, state):
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

    def get_neighbors_with_cost(self, state):
        return {
            "A": [("B", 1), ("C", 2)],
            "B": [("D", 3), ("E", 1)],
            "C": [("F", 4), ("G", 2)],
            "D": [("H", 6)],
            "E": [("H", 2)],
            "F": [("H", 3)],
            "G": [("H", 4)],
            "H": [],
        }[state]


class DLSAgent:
    def __init__(self, env):
        self.env = env

    def depth_limited_search(self, initial, goal, limit):
        stack = [(initial, [initial], 0)]
        seen = set()

        while stack:
            state, path, depth = stack.pop()

            if state == goal:
                return path

            if depth < limit:
                seen.add(state)

                for neighbor in self.env.get_neighbors(state):
                    if neighbor not in seen:
                        stack.append((neighbor, path + [neighbor], depth + 1))

        return None


class UCSAgent:
    def __init__(self, env):
        self.env = env

    def uniform_cost_search(self, initial, goal):
        seen = set()
        queue = [(initial, 0)]
        parent = {initial: None}
        node_cost = {initial: 0}

        while queue:
            queue.sort(key=lambda x: x[1])
            state, current_cost = queue.pop(0)

            if state in seen:
                continue

            if state == goal:
                path = []
                while state:
                    path.append(state)
                    state = parent[state]

                path.reverse()
                return path, current_cost

            for neighbor, cost in self.env.get_neighbors_with_cost(state):
                new_cost = cost + current_cost
                if neighbor not in node_cost or node_cost[neighbor] > new_cost:
                    queue.append((neighbor, new_cost))
                    node_cost[neighbor] = new_cost
                    parent[neighbor] = state

        return None


if __name__ == "__main__":
    env = Environment()
    dls_agent = DLSAgent(env)
    ucs_agent = UCSAgent(env)

    dls_path = dls_agent.depth_limited_search("A", "H", 3)
    ucs_path = ucs_agent.uniform_cost_search("A", "H")

    print("DLS Path:", dls_path)
    print("UCS Path:", ucs_path)
