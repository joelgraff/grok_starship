# src/crew.py
from mesa import Agent
from src.tasks import TaskType, Task  # Fully qualified import
import random
import logging

logger = logging.getLogger(__name__)

class CrewAgent(Agent):
    def __init__(self, unique_id, model, data):
        self.unique_id = unique_id
        self.model = model
        if self.model is not None:
            self.model.register_agent(self)
        self.name = data["name"]
        self.age = data["age"]
        self.role = data["role"]
        self.health = data["health"]
        self.mood = data["mood"]
        self.position = (1, 0, 0)
        self.task = None
        self.performance = 100

        logger.info(
            "%s status: Health=%s, Mood=%s, Task=%s (%s%% complete)",
            self.name, self.health, self.mood, self.task.name if self.task else "None",
            self.task.progress if self.task else 0,
            extra={'sim': self.model}
        )

    def step(self):
        if self.health > 0:
            if not self.task and not hasattr(self, 'cooldown'):
                self.task = self.model.task_manager.generate_random_event(self.role)
                if self.task:
                    self.task.assign(self)
                    logger.info(
                        f"{self.name} assigned task: {self.task.name} at {self.task.location} (0% complete)",
                        extra={'sim': self.model}
                    )
            elif not self.task and hasattr(self, 'cooldown'):
                self.cooldown -= 1
                if self.cooldown <= 0:
                    del self.cooldown
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
            logger.info(f"{self.name} moved to {self.position} toward {self.task.name}")

    def get_nearby_crew(self):
        """Return list of crew within 1 unit (same deck)."""
        nearby = []
        for other in self.model.agents:
            if other is not self and other.health > 0:
                o_deck, o_x, o_y = other.position
                s_deck, s_x, s_y = self.position
                if o_deck == s_deck and abs(o_x - s_x) <= 1 and abs(o_y - s_y) <= 1:
                    nearby.append(other)
        return nearby

    def update_status(self):
        if self.health > 0:
            nearby_crew = self.get_nearby_crew()
            morale_boost = len(nearby_crew) * 1
            if self.task and self.task.priority > 5:
                self.mood -= 2
                self.health -= 1 if random.random() < 0.1 else 0
            else:
                self.mood += 1
            self.mood += morale_boost
            self.mood = max(0, min(100, self.mood))
            self.health = max(0, min(100, self.health))
            self.performance = min(100, self.health + self.mood // 2)
            logger.info(
                "%s status: Health=%s, Mood=%s, Task=%s (%s%% complete), Morale boost=%s",
                self.name, self.health, self.mood,
                self.task.name if self.task else "None",
                self.task.progress if self.task else 0,
                morale_boost,
                extra={'sim': self.model}
            )
        if self.health == 0:
            self.task = None
            logger.info("%s has died (Health = 0)", self.name, extra={'sim': self.model})
            self.model.agents.remove(self)