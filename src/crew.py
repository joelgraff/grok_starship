# src/crew.py
from mesa import Agent
from tasks import TaskType
import random

class CrewAgent(Agent):
    def __init__(self, unique_id, model, data):
        super().__init__(unique_id, model)
        self.name = data["name"]
        self.age = data["age"]
        self.role = data["role"]
        self.health = data["health"]  # 0-100
        self.mood = data["mood"]      # 0-100 (higher is better)
        self.position = (1, 0, 0)     # (deck, x, y)
        self.task = None
        self.performance = 100        # Base performance

    def step(self):
        if not self.task:
            self.task = self.model.task_manager.generate_random_event()
            self.task.assign(self)
        self.move_toward_task()
        self.update_status()

    def move_toward_task(self):
        if self.task and self.position != self.task.location:
            # Simplified movement (expand with pathfinding later)
            curr_deck, curr_x, curr_y = self.position
            targ_deck, targ_x, targ_y = self.task.location
            if curr_deck != targ_deck:
                self.position = (targ_deck, curr_x, curr_y)  # Turbolift
            elif curr_x < targ_x:
                self.position = (curr_deck, curr_x + 1, curr_y)
            elif curr_x > targ_x:
                self.position = (curr_deck, curr_x - 1, curr_y)
            elif curr_y < targ_y:
                self.position = (curr_deck, curr_x, curr_y + 1)
            elif curr_y > targ_y:
                self.position = (curr_deck, curr_x, curr_y - 1)

    def update_status(self):
        # Performance and mood degrade/improve
        if self.task and self.task.priority > 5:
            self.mood -= 2
            self.health -= 1 if random.random() < 0.1 else 0
        else:
            self.mood += 1
        self.mood = max(0, min(100, self.mood))
        self.performance = min(100, self.health + self.mood // 2)