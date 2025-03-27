# src/simulation.py
import simpy
from mesa import Model
from src.crew import CrewAgent

class StarshipSimulation(Model):
    def __init__(self, crew_data, ship_layout):
        self.env = simpy.Environment()  # SimPy environment for event scheduling
        super().__init__()
        self.crew = [CrewAgent(i, self, data) for i, data in enumerate(crew_data)]
        self.ship_layout = ship_layout
        self.running = True

    def step(self):
        # Advance simulation one step
        for agent in self.crew:
            agent.step()
        self.env.run(until=self.env.now + 1)

    def run(self, duration):
        self.env.run(until=duration)