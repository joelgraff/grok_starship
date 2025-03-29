# src/simulation.py
import simpy
from mesa import Model
from src.crew import CrewAgent
from src.tasks import TaskManager
from src.ship import Starship

class StarshipSimulation(Model):
    def __init__(self, crew_data, ship_layout):
        super().__init__()
        self.env = simpy.Environment()
        self.ship = Starship(ship_layout)
        self.task_manager = TaskManager(self)
        self.running = True

        for i, data in enumerate(crew_data):
            agent = CrewAgent(i, self, data)
            self.agents.add(agent)
        self.crew = self.agents

    def step(self):
        self.agents.shuffle_do("step")
        self.task_manager.update()
        self.env.run(until=self.env.now + 1)