import random


class Environment:
    def __init__(self, num_tasks=5):
        self.tasks = []
        for i in range(num_tasks):
            status = random.choice(['Completed', 'Failed'])
            self.tasks.append({'task_id': i + 1, 'status': status})

    def get_percepts(self):
        return self.tasks

    def display_task_statuses(self):
        for task in self.tasks:
            print(f"Task {task['task_id']}: {task['status']}")
        print('\n')


class Agent:
    def act(self, tasks):
        failed_tasks = [task for task in tasks if task['status'] == 'Failed']

        if failed_tasks:
            return 'Retry failed tasks'
        else:
            return 'All tasks completed'

    def retry_failed_tasks(self, tasks):
        for task in tasks:
            if task['status'] == 'Failed':
                if random.random() < 0.25:
                    task['status'] = 'Completed'


def run_agent(agent, env):
    env.display_task_statuses()

    while True:
        tasks = env.get_percepts()
        action = agent.act(tasks)

        print(f"Action: {action}")
        
        if action == 'All tasks completed':
            break

        agent.retry_failed_tasks(tasks)
        env.display_task_statuses()


agent = Agent()
env = Environment()
run_agent(agent, env)
