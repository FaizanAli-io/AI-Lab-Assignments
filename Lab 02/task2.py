import random

class Environment:
    def __init__(self, num_servers=5):
        self.servers = {}
        for i in range(1, num_servers + 1):
            self.servers[f"Server_{i}"] = random.choice(["Underloaded", "Balanced", "Overloaded"])

    def get_system_state(self):
        return self.servers

    def display_system_state(self):
        print("\nUpdated System Load Status:")
        for server, status in self.servers.items():
            print(f"{server}: {status}")

class LoadBalancerAgent:
    def balance_load(self, env):
        overloaded_servers = [server for server, state in env.servers.items() if state == "Overloaded"]
        underloaded_servers = [server for server, state in env.servers.items() if state == "Underloaded"]

        if len(overloaded_servers) > len(underloaded_servers):
            message = "\nNot enough underloaded servers"
        elif len(overloaded_servers) < len(underloaded_servers):
            message = "\nNot enough overloaded servers"
        else:
            message = "\nLoad balanced"

        for overloaded_server in overloaded_servers:
            if underloaded_servers:
                underloaded_server = underloaded_servers.pop()
                print(f"Moving tasks from {overloaded_server} to {underloaded_server}.")
                env.servers[overloaded_server] = "Balanced"
                env.servers[underloaded_server] = "Balanced"
                overloaded_servers = [server for server, state in env.servers.items() if state == "Overloaded"]
                underloaded_servers = [server for server, state in env.servers.items() if state == "Underloaded"]
            else:
                break
        
        print(message)

    def scan_and_balance(self, system_state):
        overloaded_servers = [server for server, state in system_state.items() if state == "Overloaded"]
        underloaded_servers = [server for server, state in system_state.items() if state == "Underloaded"]

        print(f"Overloaded servers: {overloaded_servers}")
        print(f"Underloaded servers: {underloaded_servers}")

        if overloaded_servers and underloaded_servers:
            print("\nBalancing the load...")
            return True  
        else:
            print("\nNo balancing needed. All servers are either balanced or at capacity.")
            return False

def run_load_balancer(agent, env):
    print("Initial System Load Status:")
    env.display_system_state()

    agent.scan_and_balance(env.get_system_state())
    result = agent.balance_load(env)

    env.display_system_state()

env = Environment()
agent = LoadBalancerAgent()
run_load_balancer(agent, env)
