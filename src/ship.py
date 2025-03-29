# src/ship.py
class Starship:
    def __init__(self, layout):
        self.layout = layout
        self.systems = {
            "navigation": {"status": "operational", "integrity": 100},
            "engineering": {"status": "operational", "integrity": 100},
            "hull": {"status": "operational", "integrity": 100},
            "security": {"status": "operational", "integrity": 100}
        }

    def update_system(self, system, status=None, integrity_change=0):
        if system in self.systems:
            if status:
                self.systems[system]["status"] = status
            self.systems[system]["integrity"] = max(0, min(100, self.systems[system]["integrity"] + integrity_change))