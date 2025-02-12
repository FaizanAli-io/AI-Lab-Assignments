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


class DLSAgent:
    def depth_limited_search(self, initial, goal, limit):
        stack = [(initial, [], 0)]
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

            print(stack)

        return None


class UCSAgent:
    def uniform_cost_search(self, initial, goal, limit):
        queue = [(initial, [], 0)]
        seen = set()

        while queue:
            state, path, cost = queue.pop()

            if state == goal:
                return path

            if cost < limit:
                seen.add(state)

                for neighbor in get_neighbors(state):
                    if neighbor not in seen:
                        queue.append((neighbor, path + [neighbor], depth + 1))

            print(queue)

        return None


agent = DLSAgent()
path = agent.depth_limited_search("A", "H", 3)

print("DLS Path:", path)


# def get_neighbors_cost(state):

#     if state == "A":
#         return [("B", "to B", 5), ("C", "to C", 2)]
#     elif state == "B":
#         return [("D", "to D", 4), ("E", "to E", 2)]
#     elif state == "C":
#         return [("F", "to F", 1), ("G", "to G", 6)]
#     elif state == "E":
#         return [("H", "to H", 2)]
#     else:
#         return []


# utility_based_agent = UtilityBasedAgent("A", "H", get_neighbors_cost)
# path = utility_based_agent.uniform_cost_search()
# print("UCS Path:", path)
