import simpy
from mesa import Model
from src.crew import CrewAgent
from src.tasks import TaskManager

class StarshipSimulation(Model):
    def __init__(self, crew_data, ship_layout):
        # Initialize Mesa Model
        super().__init__()
        # Set up SimPy environment
        self.env = simpy.Environment()
        # Initialize crew agents
        self.crew = [CrewAgent(i, self, data) for i, data in enumerate(crew_data)]
        self.ship_layout = ship_layout
        self.task_manager = TaskManager(self)  # Pass simulation instance
        self.running = True

    def step(self):
        """Advance the simulation by one step."""
        for agent in self.crew:
            agent.step()
        self.task_manager.update()
        self.env.run(until=self.env.now + 1)  # Simulate one time unit