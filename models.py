# models.py

import mesa
import random
from agents import CrewAgent

class StarshipModel:
    def __init__(self):
        self.x, self.y = 0, 0
        self.energy = 10000
        self.shields = 100
        self.velocity = 0
        self.log = []
        self.tasks = []  # (task_name, effort_required, effort_done, zone)

    def step(self, dt=1.0):
        if self.velocity > 0:
            self.x += self.velocity * dt
            self.y += self.velocity * dt
            self.energy -= self.velocity * 50 * dt
        if random.random() < 0.05 and not any("Alien" in t[0] for t in self.tasks):
            self.log.append("Alien ship detected!")
            self.shields -= 20
            self.tasks.append(("Repair shields", 100, 0, "Engine Room"))
        self.energy = max(0, self.energy)
        self.shields = max(0, min(100, self.shields))

    def process_command(self, command):
        if command.startswith("Warp"):
            try:
                self.velocity = int(command.split()[1])
                self.log.append(f"Set warp to {self.velocity}")
            except:
                self.log.append("Invalid warp command")
        elif command == "Shields up":
            self.shields = min(100, self.shields + 20)
            self.log.append("Shields raised")
        elif command == "Treat sick":
            self.tasks.append(("Treat sick", 200, 0, "Medbay"))
            self.log.append("Medical team dispatched")

class ShipModel(mesa.Model):
    def __init__(self, starship):
        self.starship = starship
        self.grid = mesa.space.MultiGrid(20, 10, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        from faker import Faker  # Local import to avoid circular dependency
        fake = Faker()
        num_crew = random.randint(200, 400)
        roles = ["Captain", "Navigator", "Engineer", "Communicator", "Scientist"] + ["Crew"] * 10
        for i in range(num_crew):
            name = fake.name()
            age = random.randint(20, 60)
            role = random.choice(roles)
            health = random.randint(70, 100)
            fatigue = random.randint(0, 30)
            skill = random.randint(30, 90)
            agent = CrewAgent(i, self, name, age, role, health, fatigue, skill)
            self.schedule.add(agent)
            x, y = random.randint(0, 19), random.randint(0, 9)
            self.grid.place_agent(agent, (x, y))

    def step(self):
        self.starship.step()
        self.schedule.step()
        from config import SHIP_ZONES
        idle_crew = [a for a in self.schedule.agents if a.task is None and a.fatigue < 80]
        for i, (task_name, effort_required, effort_done, zone) in enumerate(self.starship.tasks):
            if effort_done < effort_required and idle_crew:
                crew = random.choice(idle_crew)
                (x1, y1), (x2, y2) = SHIP_ZONES[zone]
                target_pos = (random.randint(x1, x2), random.randint(y1, y2))
                crew.task = (i, target_pos)
                idle_crew.remove(crew)