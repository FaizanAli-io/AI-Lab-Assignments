import random

class Environment:
    def __init__(self):
        self.size = 4

        self.states = ['Safe', 'Enemy', 'Danger']

        self.grid = [
            [
                random.choice(self.states) 
                for _ in range(self.size)
            ] 
            for _ in range(self.size)
        ]

    def get_state(self, pos):
        return self.grid[pos // self.size][pos % self.size]

    def set_state(self, pos, state):
        self.grid[pos // self.size][pos % self.size] = state

    def show_state(self):
        [print(row) for row in self.grid]

class Agent:
    def __init__(self):
        self.pos = 0

    def act(self, state):
        if state == 'Safe':
            print('Agent is safe, moving forward')
            return 'Move'
        elif state == 'Enemy':
            print('Agent saw an enemy, attacking')
            return 'Attack'
        elif state == 'Danger':
            print('Agent is in danger, hiding')
            return 'Hide'

def run_agent(agent, env):
    env.show_state()

    while agent.pos < env.size ** 2:
        state = env.get_state(agent.pos)
        action = agent.act(state)

        print(f"Position: {agent.pos}, State: {state}, Action: {action}\n")

        if action == 'Move':
            agent.pos += 1
        elif action == 'Attack':
            env.set_state(agent.pos, 'Safe')
        elif action == 'Hide':
            env.set_state(agent.pos, 'Enemy')

    env.show_state()

    print('Grid Cleared, No enemies left')


agent = Agent()
env = Environment()
run_agent(agent, env)