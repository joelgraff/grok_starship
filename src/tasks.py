from enum import Enum
import random

class TaskType(Enum):
    REPAIR = "Repair"
    NAVIGATE = "Navigate"
    SECURITY = "Security"
    MEDICAL = "Medical"
    ROUTINE = "Routine"

class Task:
    def __init__(self, name, task_type, location, priority, duration):
        self.name = name
        self.task_type = task_type
        self.location = location
        self.priority = priority
        self.duration = duration
        self.assigned_to = None

    def assign(self, agent):
        self.assigned_to = agent

class TaskManager:
    def __init__(self, simulation):
        self.simulation = simulation
        self.active_tasks = []

    def generate_random_event(self):
        events = [
            Task("Repair Hull Breach", TaskType.REPAIR, (2, 5, 6), 8, 10),
            Task("Recalibrate Navigation", TaskType.NAVIGATE, (1, 0, 0), 4, 5),
            Task("Intruder Alert", TaskType.SECURITY, (2, 5, 5), 10, 15),
            Task("Treat Injured Crew", TaskType.MEDICAL, (2, 5, 5), 6, 8),
            Task("Routine Maintenance", TaskType.ROUTINE, (2, 5, 6), 2, 3)
        ]
        task = random.choice(events)
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