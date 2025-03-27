# agents.py

import mesa
from config import SHIP_ZONES

class CrewAgent(mesa.Agent):
    def __init__(self, unique_id, model, name, age, role, health=100, fatigue=0, skill=50):
        super().__init__(unique_id, model)
        self.name = name
        self.age = age
        self.role = role
        self.health = health
        self.fatigue = fatigue
        self.skill = skill
        self.task = None  # (index, target_pos)

    def move_toward(self, target_pos):
        tx, ty = target_pos
        cx, cy = self.pos
        dx = 1 if tx > cx else (-1 if tx < cx else 0)
        dy = 1 if ty > cy else (-1 if ty < cy else 0)
        new_pos = (cx + dx, cy + dy)
        if self.model.grid.is_cell_empty(new_pos) or new_pos == target_pos:
            self.model.grid.move_agent(self, new_pos)

    def step(self):
        if self.task:
            task_idx, target_pos = self.task
            task_name, effort_required, effort_done, zone = self.model.starship.tasks[task_idx]
            if self.pos != target_pos:
                self.move_toward(target_pos)
                self.fatigue = min(100, self.fatigue + 1)
            else:
                effort = min(self.skill / 10, effort_required - effort_done)
                self.model.starship.tasks[task_idx] = (task_name, effort_required, effort_done + effort, zone)
                self.fatigue = min(100, self.fatigue + 2)
                if effort_done + effort >= effort_required:
                    self.model.starship.log.append(f"{task_name} completed!")
                    if task_name ==Execute as "Repair shields":
                        self.model.starship.shields = min(100, self.model.starship.shields + 20)
                    self.model.starship.tasks.pop(task_idx)
                    self.task = None
        else:
            possible_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            new_pos = random.choice(possible_moves)
            self.model.grid.move_agent(self, new_pos)
            self.fatigue = min(100, self.fatigue + 1)