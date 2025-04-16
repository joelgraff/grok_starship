import random
from module import Module

class CrewMember:
    def __init__(self, id, name, role, start_room):
        self.id = id
        self.name = name
        self.role = role
        self.start_room = start_room
        self.current_room = start_room
        self.health = 100
        self.fatigue = 0
        self.morale = 50
        self.stress = 0
        self.age = random.randint(18, 60)
        self.gender = random.choice(["male", "female", "non-binary"])
        self.personality = {
            "openness": random.randint(20, 80),
            "conscientiousness": random.randint(20, 80),
            "extraversion": random.randint(20, 80),
            "agreeableness": random.randint(20, 80),
            "neuroticism": random.randint(20, 80)
        }
        self.skills = {
            role: random.randint(50, 90),
            "general": random.randint(30, 60)
        }
        self.relationships = {}
        self.current_task = None
        self.status = "Idle"

    def assign_task(self, task):
        self.current_task = task
        self.current_room = task.get("location", self.current_room)
        self.status = f"Working on {task.get('type', 'task')}"
        self.fatigue = min(self.fatigue + random.uniform(1, 3), 100)
        self.stress = min(self.stress + random.uniform(0.5, 2), 100)

    def assign_social_action(self, action, target_id=None):
        self.current_task = {"type": action, "target_id": target_id}
        self.status = f"Engaging in {action}"
        if action == "socialize" and target_id:
            self.current_room = "mess_hall"
            self.morale = min(self.morale + random.uniform(5, 10), 100)
            self.stress = max(self.stress - random.uniform(3, 7), 0)
            self.update_relationship(target_id, affinity_change=0.15, trust_change=0.1)
        elif action == "hobby":
            self.current_room = "recreation"
            self.morale = min(self.morale + random.uniform(3, 7), 100)
            self.stress = max(self.stress - random.uniform(2, 5), 0)
        elif action == "rest":
            self.current_room = "quarters"
            self.fatigue = max(self.fatigue - random.uniform(5, 10), 0)
            self.stress = max(self.stress - random.uniform(3, 5), 0)

    def complete_task(self, common_data):
        if not self.current_task:
            return False
        task_type = self.current_task.get("type")
        system = self.current_task.get("system")
        skill_level = self.skills.get(self.role, 50)
        personality_bonus = self.personality["conscientiousness"] / 100
        success_prob = (skill_level / 100) * (1 + personality_bonus * 0.2)
        success = random.random() < success_prob

        if task_type == "repair" and system in common_data["engineering"]["system_health"]:
            if success:
                common_data["engineering"]["system_health"][system] = min(
                    common_data["engineering"]["system_health"][system] + 10, 100
                )
                self.status = f"Repaired {system}"
                self.morale = min(self.morale + 5, 100)
            else:
                self.status = f"Failed to repair {system}"
                self.stress = min(self.stress + 5, 100)
            self.fatigue = min(self.fatigue + 10, 100)

        elif task_type == "recharge" and system == "shields":
            if success:
                common_data["engineering"]["shields"] = min(
                    common_data["engineering"]["shields"] + 20, 100
                )
                self.status = "Recharged shields"
                self.morale = min(self.morale + 3, 100)
            else:
                self.status = "Failed to recharge shields"
                self.stress = min(self.stress + 3, 100)
            self.fatigue = min(self.fatigue + 5, 100)

        elif task_type in ["socialize", "hobby", "rest"]:
            self.status = "Idle"
            self.current_task = None
            return True

        self.current_task = None
        return success

    def update_relationship(self, other_id, affinity_change=0, trust_change=0):
        if other_id not in self.relationships and len(self.relationships) < 20:
            self.relationships[other_id] = {
                "type": "acquaintance",
                "trust": 0.5,
                "affinity": 0.5
            }
        if other_id in self.relationships:
            rel = self.relationships[other_id]
            rel["trust"] = max(0, min(1, rel["trust"] + trust_change))
            rel["affinity"] = max(0, min(1, rel["affinity"] + affinity_change))
            if rel["affinity"] > 0.8 and rel["type"] == "acquaintance":
                rel["type"] = random.choice(["friend", "mentor", "rival"])
            elif rel["affinity"] < 0.3 and rel["type"] != "acquaintance":
                rel["type"] = "acquaintance"
            if len(self.relationships) >= 20:
                lowest_affinity = min(self.relationships.items(), key=lambda x: x[1]["affinity"])
                if lowest_affinity[1]["affinity"] < rel["affinity"]:
                    del self.relationships[lowest_affinity[0]]

    def update(self):
        self.fatigue = min(self.fatigue + random.uniform(0.05, 0.2), 100)
        neuroticism_factor = self.personality["neuroticism"] / 100
        self.stress = min(self.stress + random.uniform(0.01, 0.1) * neuroticism_factor, 100)
        if self.fatigue < 50 and self.stress < 50:
            self.morale = min(self.morale + random.uniform(0.2, 0.5) * (self.personality["extraversion"] / 100), 100)
        elif self.fatigue > 80 or self.stress > 80:
            self.morale = max(self.morale - random.uniform(0.5, 1.5), 0)
            self.health = max(self.health - random.uniform(0.05, 0.15), 0)

    def get_status(self):
        # Include affinity/trust for visibility
        rels = {k: {**v, "trust": round(v["trust"], 2), "affinity": round(v["affinity"], 2)} for k, v in self.relationships.items()}
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "health": round(self.health, 1),
            "fatigue": round(self.fatigue, 1),
            "morale": round(self.morale, 1),
            "stress": round(self.stress, 1),
            "status": self.status,
            "room": self.current_room,
            "relationships": rels
        }

class Crew(Module):
    def __init__(self, ship, common_data=None):
        super().__init__(ship)
        self.name = "Crew"
        self.common_data = common_data or {}
        if "crew" not in self.common_data:
            self._initialize_crew()

    def _initialize_crew(self, crew_size=200):
        roles = ["engineer", "medic", "pilot", "technician", "scientist", "security"]
        rooms = ["bridge", "engine_room", "medbay", "crew_quarters", "mess_hall", "recreation"]
        self.common_data["crew"] = [
            CrewMember(
                id=i,
                name=f"Crew {i+1}",
                role=random.choice(roles),
                start_room=random.choice(rooms)
            ) for i in range(crew_size)
        ]
        for crew in self.common_data["crew"]:
            num_initial_rels = random.randint(5, 10)
            potential_ids = [c.id for c in self.common_data["crew"] if c.id != crew.id]
            for target_id in random.sample(potential_ids, min(num_initial_rels, len(potential_ids))):
                crew.update_relationship(target_id, affinity_change=random.uniform(-0.1, 0.1))

    def update(self, sim_time=None):
        for crew in self.common_data["crew"]:
            crew.update()
            if crew.morale < 20 or self.stress > 80:
                self.ship.status = f"Crew {crew.name} in distress"

    def get_status(self):
        return {
            "module": self.name,
            "crew": [crew.get_status() for crew in self.common_data["crew"]],
            "active_tasks": len(self.common_data.get("crew_tasks", []))
        }