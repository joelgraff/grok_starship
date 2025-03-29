# src/simulation.py
import simpy
from mesa import Model
from src.crew import CrewAgent
from src.tasks import TaskManager

class StarshipSimulation(Model):
    def __init__(self, crew_data, ship_layout):
        super().__init__()
        self.env = simpy.Environment()
        # self.schedule = RandomActivation(self)  # Scheduler for agents
        self.ship_layout = ship_layout
        self.task_manager = TaskManager(self)
        self.running = True

        # Initialize crew agents and add to scheduler
        for i, data in enumerate(crew_data):
            agent = CrewAgent(i, self, data)
            self.agents.add(agent)
            #self.schedule.add(agent)
        self.crew = self.agents  # Store agents for easy access

    def step(self):
    """Advance the simulation by one step."""
        self.agents.shuffle_do("step")  # This will skip dead agents after removal
        self.task_manager.update()
        self.env.run(until=self.env.now + 1)