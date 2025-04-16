import random
from module import Module
from crew import CrewMember

class CommunitySimulator(Module):
    def __init__(self, ship, common_data=None):
        super().__init__(ship)
        self.name = "Community Simulator"
        self.common_data = common_data or {}
        self.scenarios = []
        self.time_step = 0
        self.running = False
        self.sample_crew_ids = []

    def initialize(self, crew_size=200):
        if "crew" not in self.common_data:
            self.common_data["crew"] = [
                CrewMember(
                    id=i,
                    name=f"Crew {i+1}",
                    role=random.choice(["engineer", "medic", "pilot", "technician", "scientist", "security"]),
                    start_room=random.choice(["bridge", "engine_room", "medbay", "crew_quarters", "mess_hall", "recreation"])
                ) for i in range(crew_size)
            ]
            for crew in self.common_data["crew"]:
                num_initial_rels = random.randint(5, 10)
                potential_ids = [c.id for c in self.common_data["crew"] if c.id != crew.id]
                for target_id in random.sample(potential_ids, min(num_initial_rels, len(potential_ids))):
                    crew.update_relationship(target_id, affinity_change=random.uniform(-0.1, 0.1))
        self.sample_crew_ids = random.sample([c.id for c in self.common_data["crew"]], 10)

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

    def trigger_event(self, event_type, params=None):
        params = params or {}
        scenario = None
        if event_type == "system_failure":
            scenario = {
                "type": "repair",
                "system": params.get("system", "propulsion"),
                "location": "engine_room",
                "priority": params.get("priority", 1),
                "participants": [],
                "duration": params.get("duration", 5),  # Extended for visibility
                "progress": 0,
                "outcomes": []
            }
        elif event_type == "social_gathering":
            scenario = {
                "type": "socialize",
                "location": "mess_hall",
                "priority": params.get("priority", 0.5),
                "participants": [],
                "duration": params.get("duration", 3),
                "progress": 0,
                "outcomes": []
            }
        elif event_type == "crisis":
            scenario = {
                "type": "crisis",
                "issue": params.get("issue", "medical_emergency"),
                "location": params.get("location", "medbay"),
                "priority": params.get("priority", 2),
                "participants": [],
                "duration": params.get("duration", 5),
                "progress": 0,
                "outcomes": []
            }
        if scenario:
            self.assign_participants(scenario)
            for crew in scenario["participants"]:
                # Immediate status update
                if scenario["type"] == "socialize":
                    crew.assign_social_action("socialize")
                else:
                    crew.assign_task({
                        "type": scenario["type"],
                        "system": scenario.get("system", scenario.get("issue", "")),
                        "location": scenario["location"]
                    })
            self.scenarios.append(scenario)
            return scenario
        return None

    def assign_participants(self, scenario):
        required_roles = {
            "repair": ["engineer", "technician"],
            "crisis": ["medic", "security"],
            "socialize": []
        }
        num_needed = random.randint(20, 50) if scenario["type"] == "socialize" else random.randint(5, 15)
        eligible_crew = [
            c for c in self.common_data["crew"]
            if c.status == "Idle" and (not required_roles[scenario["type"]] or c.role in required_roles[scenario["type"]])
        ]
        scenario["participants"] = random.sample(eligible_crew, min(num_needed, len(eligible_crew)))

    def update(self, sim_time=None):
        if not self.running:
            return
        self.time_step += 1

        # Update all crew
        for crew in self.common_data["crew"]:
            crew.update()
            if crew.status == "Idle" and not any(c.id in [p.id for s in self.scenarios for p in s["participants"]] for c in self.common_data["crew"] if c.id == crew.id):
                if crew.fatigue > 50:
                    crew.assign_social_action("rest")
                elif crew.morale < 30:
                    crew.assign_social_action("hobby")
                elif random.random() < (crew.personality["extraversion"] / 100):
                    if crew.relationships:
                        target_id = random.choice(list(crew.relationships.keys()))
                        crew.assign_social_action("socialize", target_id)

        # Process scenarios
        for scenario in self.scenarios[:]:
            scenario["progress"] += 1
            for crew in scenario["participants"]:
                if scenario["type"] == "repair":
                    if not crew.current_task:  # Reassign if cleared
                        crew.assign_task({
                            "type": "repair",
                            "system": scenario["system"],
                            "location": scenario["location"]
                        })
                    success = crew.complete_task(self.common_data)
                    if success:
                        scenario["progress"] += 0.5  # Slower progress for visibility
                        scenario["outcomes"].append(f"Crew {crew.id} progressed repair of {scenario['system']}")
                    else:
                        scenario["outcomes"].append(f"Crew {crew.id} failed repair attempt")
                    # Teamwork strengthens bonds
                    for other in scenario["participants"]:
                        if other.id != crew.id and random.random() < 0.5:
                            crew.update_relationship(other.id, affinity_change=0.1, trust_change=0.05)
                elif scenario["type"] == "socialize":
                    if not crew.current_task:
                        target_id = random.choice(list(crew.relationships.keys())) if crew.relationships else None
                        crew.assign_social_action("socialize", target_id)
                    crew.complete_task(self.common_data)
                    crew.morale = min(crew.morale + 3, 100)
                    scenario["outcomes"].append(f"Crew {crew.id} socialized, morale +3")
                    # More frequent relationship updates
                    for other in scenario["participants"]:
                        if other.id != crew.id and random.random() < 0.7:
                            crew.update_relationship(other.id, affinity_change=0.2, trust_change=0.1)
                elif scenario["type"] == "crisis":
                    if not crew.current_task:
                        crew.assign_task({
                            "type": "crisis_response",
                            "issue": scenario["issue"],
                            "location": scenario["location"]
                        })
                    crew.stress = min(crew.stress + 3, 100)
                    success = crew.complete_task(self.common_data)
                    scenario["outcomes"].append(f"Crew {crew.id} {'resolved' if success else 'failed'} {scenario['issue']}")
                    if success:
                        scenario["progress"] += 0.5

            if scenario["progress"] >= scenario["duration"]:
                self.scenarios.remove(scenario)
                for crew in scenario["participants"]:
                    crew.status = "Idle"
                    crew.current_task = None
                    if scenario["type"] == "socialize":
                        crew.morale = min(crew.morale + 5, 100)
                        scenario["outcomes"].append(f"Crew {crew.id} post-gathering morale +5")
                self.common_data["debug"].append({
                    "time": self.time_step,
                    "event": f"Scenario {scenario['type']} completed with {len(scenario['outcomes'])} outcomes"
                })

        avg_morale = sum(c.morale for c in self.common_data["crew"]) / len(self.common_data["crew"])
        if avg_morale < 30:
            self.common_data["debug"].append({"time": sim_time, "event": "Low crew morale detected"})

    def get_status(self):
        return {
            "module": self.name,
            "time_step": self.time_step,
            "active_scenarios": len(self.scenarios),
            "crew_stats": {
                "avg_morale": sum(c.morale for c in self.common_data["crew"]) / len(self.common_data["crew"]),
                "avg_stress": sum(c.stress for c in self.common_data["crew"]) / len(self.common_data["crew"]),
                "avg_fatigue": sum(c.fatigue for c in self.common_data["crew"]) / len(self.common_data["crew"])
            },
            "relationships": sum(len(c.relationships) for c in self.common_data["crew"]) / 2
        }

    def get_crew_details(self, crew_id=None):
        if crew_id is not None:
            for crew in self.common_data["crew"]:
                if crew.id == crew_id:
                    return crew.get_status()
            return None
        return [crew.get_status() for crew in self.common_data["crew"] if crew.id in self.sample_crew_ids]

    def get_crew_sample(self):
        return self.sample_crew_ids

    def get_scenario_details(self):
        details = []
        for scenario in self.scenarios:
            participants = [
                {"id": c.id, "name": c.name, "role": c.role, "status": c.status}
                for c in scenario["participants"]
            ]
            details.append({
                "type": scenario["type"],
                "location": scenario["location"],
                "progress": scenario["progress"],
                "duration": scenario["duration"],
                "participants": participants,
                "outcomes": scenario.get("outcomes", [])
            })
        return details

    def get_relationship_graph(self):
        """Return nodes and edges for all crew relationships."""
        nodes = [c.id for c in self.common_data["crew"]]
        edges = []
        for crew in self.common_data["crew"]:
            for rel_id, rel_data in crew.relationships.items():
                if rel_id > crew.id:  # Avoid duplicates
                    edges.append((crew.id, rel_id, rel_data["affinity"]))
        return nodes, edges