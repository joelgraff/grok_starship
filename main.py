# main.py
from src.simulation import StarshipSimulation
from src.interface import StarshipInterface
from src.ship import Starship
import json
import os
import traceback

def load_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    with open(file_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    try:
        crew_data = load_config("config/crew_data.json")
        ship_layout = load_config("config/ship_layout.json")
        ship = Starship(ship_layout)
        sim = StarshipSimulation(crew_data, ship_layout)
        interface = StarshipInterface(sim)
        interface.run()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  # Print full stack trace for debugging