# src/crew.py
from mesa import Agent
from src.tasks import TaskType
import random

class CrewAgent(Agent):
    def __init__(self, unique_id, model, data):
        print(f"Initializing CrewAgent with unique_id={unique_id}, model={model}")
        self.unique_id=unique_id
        self.model = model
        
        if self.model is not None:
            self.model.register_agent(self)

        self.name = data["name"]
        self.name = data["name"]
        self.age = data["age"]
        self.role = data["role"]
        self.health = data["health"]
        self.mood = data["mood"]
        self.position = (1, 0, 0)    # Start on Bridge Deck
        self.task = None
        self.performance = 100
        print(f"After Agent.__init__, self.model={self.model}")

    def step(self):
        if not self.task:
            self.task = self.model.task_manager.generate_random_event()
            self.task.assign(self)
        self.move_toward_task()
        self.update_status()

    def move_toward_task(self):
        if self.task and self.position != self.task.location:
            curr_deck, curr_x, curr_y = self.position
            targ_deck, targ_x, targ_y = self.task.location
            if curr_deck != targ_deck:
                self.position = (targ_deck, curr_x, curr_y)
            elif curr_x < targ_x:
                self.position = (curr_deck, curr_x + 1, curr_y)
            elif curr_x > targ_x:
                self.position = (curr_deck, curr_x - 1, curr_y)
            elif curr_y < targ_y:
                self.position = (curr_deck, curr_x, curr_y + 1)
            elif curr_y > targ_y:
                self.position = (curr_deck, curr_x, curr_y - 1)

# src/crew.py (partial)
    def update_status(self):
        if self.health > 0:  # Only update if alive
            if self.task and self.task.priority > 5:
                self.mood -= 2
                self.health -= 1 if random.random() < 0.1 else 0
            else:
                self.mood += 1
        self.mood = max(0, min(100, self.mood))
        self.health = max(0, min(100, self.health))
        self.performance = min(100, self.health + self.mood // 2)

        if self.health == 0:
            self.task = None
            print(f"{self.name} has died (Health = 0)")
            self.model.agents.remove(self)  # Remove from simulation