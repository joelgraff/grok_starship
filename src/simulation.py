# src/simulation.py
import simpy
from mesa import Model
from src.crew import CrewAgent
from src.tasks import TaskManager

class StarshipSimulation(Model):
    def __init__(self, crew_data, ship_layout):
        super().__init__()
        self.env = simpy.Environment()
        self.ship_layout = ship_layout
        self.task_manager = TaskManager(self)
        self.running = True

        # Initialize crew agents using AgentSet (self.agents)
        for i, data in enumerate(crew_data):
            agent = CrewAgent(i, self, data)
            self.agents.add(agent)  # Add agents to the model's AgentSet
        self.crew = self.agents  # Alias for convenience

    def step(self):
        """Advance the simulation by one step."""
        self.agents.shuffle_do("step")  # Randomly activate all agents' step method
        self.task_manager.update()
        self.env.run(until=self.env.now + 1)  # Simulate one time unit