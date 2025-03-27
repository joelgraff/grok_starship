# main.py
from src.simulation import StarshipSimulation
from src.interface import StarshipInterface
from src.ship import Starship
from src.tasks import TaskManager
import json

def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    crew_data = load_config("config/crew_data.json")
    ship_layout = load_config("config/ship_layout.json")
    ship = Starship(ship_layout)
    sim = StarshipSimulation(crew_data, ship_layout)
    sim.task_manager = TaskManager(ship)  # Add task manager to simulation
    interface = StarshipInterface(sim)
    interface.run()