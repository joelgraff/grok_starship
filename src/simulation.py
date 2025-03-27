import simpy
from mesa import Model
from crew import CrewAgent
from tasks import TaskManager

class StarshipSimulation(Model):
    def __init__(self, crew_data, ship_layout):
        super().__init__()
        self.env = simpy.Environment()
        self.crew = [CrewAgent(i, self, data) for i, data in enumerate(crew_data)]
        self.ship_layout = ship_layout
        self.task_manager = TaskManager(self)  # Initialize here
        self.running = True

    def step(self):
        for agent in self.crew:
            agent.step()
        self.task_manager.update()
        self.env.run(until=self.env.now + 1)