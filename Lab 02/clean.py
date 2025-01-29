import random

class Environment:
    def __init__(self):
        self.state = random.choice(['dirty', 'clean'])

    def get_percept(self):
        return self.state

    def clean(self):
        self.state = 'clean'

    def randomize_state(self):
        self.state = random.choice(['dirty', 'clean'])

class Agent:
    def act(self, percept):
        if percept == 'dirty':
            return 'clean the room'
        else:
            return 'room is already clean'

def run_agent(agent, env, n):
    for _ in range(n):
        percept = env.get_percept()
        action = agent.act(percept)

        print(f"Percept: {percept}, Action: {action}")

        if percept == 'dirty':
            env.clean()

        env.randomize_state()

agent = Agent()
env = Environment()
run_agent(agent, env, 5)
