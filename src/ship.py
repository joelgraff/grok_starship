# src/ship.py
class Starship:
    def __init__(self, layout):
        self.layout = layout  # e.g., 2D grid or networkx graph
        self.systems = {"navigation": "operational", "engineering": "operational"}

    def update_system(self, system, status):
        self.systems[system] = status