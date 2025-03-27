class Starship:
    def __init__(self, layout):
        self.layout = layout
        self.systems = {"navigation": "operational", "engineering": "operational"}

    def update_system(self, system, status):
        self.systems[system] = status