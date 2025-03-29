# src/tasks.py
from enum import Enum
import random
import logging

logger = logging.getLogger(__name__)  # Define logger for this module

class TaskType(Enum):
    REPAIR = "Repair"
    NAVIGATE = "Navigate"
    SECURITY = "Security"
    MEDICAL = "Medical"
    ROUTINE = "Routine"
    ENGINEERING = "Engineering"
    DIPLOMACY = "Diplomacy"

class Task:
    def __init__(self, name, task_type, location, priority, duration):
        self.name = name
        self.task_type = task_type
        self.location = location
        self.priority = priority
        self.duration = duration
        self.assigned_to = []

    def assign(self, agent):
        self.assigned_to.append(agent)

class TaskManager:

    def __init__(self, simulation):
        self.simulation = simulation
        self.active_tasks = []

    def generate_random_event(self, role=None):
        events = [
            Task("Repair Hull Breach", TaskType.REPAIR, (2, 5, 6), 8, 10, roles=["Engineer"]),
            Task("Recalibrate Navigation", TaskType.NAVIGATE, (1, 0, 0), 4, 5, roles=["Navigator"]),
            Task("Intruder Alert", TaskType.SECURITY, (2, 5, 5), 10, 15, roles=["Security"]),
            Task("Treat Injured Crew", TaskType.MEDICAL, (2, 5, 5), 6, 8, roles=["Medic"]),
            Task("Routine Maintenance", TaskType.ROUTINE, (2, 5, 6), 2, 3, roles=["Engineer"]),
            Task("Stabilize Warp Core", TaskType.ENGINEERING, (2, 5, 6), 9, 12, roles=["Engineer"]),
            Task("Negotiate with Aliens", TaskType.DIPLOMACY, (1, 1, 1), 7, 10, roles=["Captain"])
        ]
        if role:
            valid_tasks = [t for t in events if role in t.roles]
            task = random.choice(valid_tasks) if valid_tasks else None
        else:
            task = random.choice(events)
        if task:
            self.active_tasks.append(task)
        return task

    def update(self):
        for task in self.active_tasks[:]:
            task.duration -= 1
            if task.duration <= 0:
                self.complete_task(task)

    def complete_task(self, task):
        if task in self.active_tasks:
            self.active_tasks.remove(task)
            # Affect ship systems and log
            if task.name == "Repair Hull Breach":
                self.simulation.ship.update_system("hull", "operational", +20)
            elif task.name == "Stabilize Warp Core":
                self.simulation.ship.update_system("engineering", "operational", +15)
            elif task.name == "Intruder Alert":
                self.simulation.ship.update_system("security", "operational", +25)

            logger.info(
                "Task %s completed by %s",
                task.name, [a.name for a in task.assigned_to],
                extra={'sim': self.simulation}
            )

class Task:
    def __init__(self, name, task_type, location, priority, duration, roles):
        self.name = name
        self.task_type = task_type
        self.location = location
        self.priority = priority
        self.duration = duration
        self.total_duration = duration  # Store original duration
        self.assigned_to = []
        self.roles = roles

    @property
    def progress(self):
        return max(0, int((1 - self.duration / self.total_duration) * 100)) if self.total_duration > 0 else 100 # % complete

    def assign(self, agent):
        self.assigned_to.append(agent)            