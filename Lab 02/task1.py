import random

class Environment:
    def __init__(self):
        self.map = {key: random.choice(['Safe', 'Vulnerable']) 
                    for key in 'ABCDEFGHI'}

    def get_state(self, pos):
        return self.map[pos]

    def set_state(self, pos, state):
        self.map[pos] = state

    def show_state(self):
        print(self.map, '\n')


class Agent:
    def __init__(self):
        self.weak = []

    def act(self, state, pos):
        if state == 'Safe':
            print('Success: Component is Safe.')
            return 'No action needed'

        else:
            self.weak.append(pos)
            print('Warning: Component is Vulnerable')
            return 'Adding to weak component list'
    
    def fix_weak(self, env):
        for pos in self.weak:
            env.set_state(pos, 'Safe')



def run_agent(agent, env):
    print('Initial State: ', end='')
    env.show_state()

    for key in 'ABCDEFGHI':
        state = env.get_state(key)
        action = agent.act(state, key)

        print(f"Position: {key}, State: {state}, Action: {action}\n")

    agent.fix_weak(env)

    print('Final State: ', end='')
    env.show_state()


agent = Agent()
env = Environment()
run_agent(agent, env)