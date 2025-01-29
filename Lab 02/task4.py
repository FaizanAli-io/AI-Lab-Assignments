import random

class Environment:
    def __init__(self):
        self.components = {
            'A': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'B': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'C': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'D': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'E': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'F': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'G': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'H': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
            'I': random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']),
        }

    def get_system_state(self):
        return self.components

    def display_system_state(self):
        print("System Components Status:")
        for component, status in self.components.items():
            print(f"Component {component}: {status}")

class Agent:
    def scan_system(self, system_state):
        for component, status in system_state.items():
            if status == 'Safe':
                print(f"Component {component} is Safe.")
            else:
                print(f"Warning: Component {component} has {status}.")

    def patch_vulnerabilities(self, system_state):
        for component, status in system_state.items():
            if status == 'Low Risk Vulnerable':
                print(f"Patching Low Risk Vulnerability in Component {component}.")
                system_state[component] = 'Safe'
            elif status == 'High Risk Vulnerable':
                print(f"High Risk Vulnerability detected in Component {component}. Premium service required.")

def run_security_exercise(agent, env):
    print("Initial System Check:")
    env.display_system_state()

    print("\nSystem Scan:")
    agent.scan_system(env.get_system_state())

    print("\nPatching Vulnerabilities:")
    agent.patch_vulnerabilities(env.get_system_state())

    print("\nFinal System Check:")
    env.display_system_state()

env = Environment()
agent = Agent()

run_security_exercise(agent, env)
