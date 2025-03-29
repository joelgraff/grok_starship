# src/simulation.py
import simpy
from mesa import Model
from src.crew import CrewAgent
from src.tasks import TaskManager
from src.ship import Starship
import logging

# Custom formatter with timestep
class SimFormatter(logging.Formatter):
    def format(self, record):
        sim = getattr(record, 'sim', None)
        timestep = int(sim.env.now) if sim and hasattr(sim, 'env') else 'N/A'
        return f"[{timestep}]: {record.levelname} - {record.getMessage()}"

# Configure logging globally
logger = logging.getLogger()  # Root logger to affect all modules
logger.setLevel(logging.INFO)
# Clear any existing handlers to avoid conflicts
logger.handlers = []
# File handler
file_handler = logging.FileHandler("simulation.log")
file_handler.setFormatter(SimFormatter())
logger.addHandler(file_handler)
# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(SimFormatter())
logger.addHandler(console_handler)

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