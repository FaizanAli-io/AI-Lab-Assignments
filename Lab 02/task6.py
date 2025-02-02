class Environment:
    def __init__(self):
        self.grid = [
            [("A", False), ("B", False), ("C", True)],
            [("D", False), ("E", True), ("F", False)],
            [("G", False), ("H", False), ("J", True)],
        ]

    def get_state(self, pos):
        return self.grid[pos // 3][pos % 3]

    def set_state(self, pos, state):
        self.grid[pos // 3][pos % 3] = state

    def show_state(self):
        print()
        [
            print(" ".join("🔥" if state else "✅" for _, state in row))
            for row in self.grid
        ]
        print()


class Agent:
    def __init__(self):
        self.pos = 0

    def finished(self):
        return self.pos >= 9

    def process_state(self, env):
        room, status = env.get_state(self.pos)

        if status:
            print(f"🤖: Room {room} is on fire, extinguishing...")
            env.set_state(self.pos, (room, False))

        else:
            print(f"🤖: Room {room} is safe, moving on...")
            self.pos += 1


def run_agent():
    agent = Agent()
    env = Environment()

    print("Initial State:")
    env.show_state()

    while not agent.finished():
        agent.process_state(env)
        env.show_state()

    print("All fires have been put out.")


run_agent()
