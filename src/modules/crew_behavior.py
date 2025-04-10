# crew_behavior.py
import random
import modules.module as m

class CrewBehavior(m.Module):
    def __init__(self, ship, common_data=None):
        super().__init__(ship)
        self.name = "Crew Behavior"

    def update(self, sim_time=None):
        self.ship.crew_fatigue += random.randint(0, 2)
        if self.ship.crew_fatigue > 50:
            self.ship.status = "Crew Fatigued"

    def get_status(self):
        return f"Crew Behavior: Fatigue {self.ship.crew_fatigue}"