from modules.module import Module
import random

class Engineering(Module):
    def __init__(self, ship, common_data):
        super().__init__(ship)
        self.name = "Engineering"
        self.common_data = common_data  # Shared data for all state and communication
        
        # Initialize common_data["engineering"] if not set by SimulationController
        if "engineering" not in self.common_data:
            self.common_data["engineering"] = {
                "energy": 1000,  # Current energy, sole state source
                "max_energy": 1000,  # Default max, adjustable
                "allocations": {"shields": 30, "weapons": 20, "propulsion": 40, "reserve": 10},
                "shields": 100,  # Strength %
                "system_health": {"shields": 100, "weapons": 100, "propulsion": 100},
                "impulse_speed": 50,  # 0-100% (maps to 0-0.25c)
                "warp_factor": 0,  # 0-10
                "surge": False  # Flag for power surge events
            }

    def update(self, sim_time=None):
        """Update energy, shields, and propulsion state each tick using common_data."""
        eng = self.common_data["engineering"]
        sim_time = sim_time or "Unknown Time"  # Fallback if sim_time not provided
        
        # Reset surge flag each tick
        eng["surge"] = False

        # Regenerate energy (5 units/second at 1 tick/second)
        if eng["energy"] < eng["max_energy"]:
            eng["energy"] += 5

        # Regenerate shields based on allocation and damage
        shields_alloc = eng["allocations"]["shields"]
        shield_regen = shields_alloc * (1 - (100 - eng["shields"]) / 100)  # Diminishing returns
        eng["shields"] = min(100, eng["shields"] + shield_regen)

        # Update propulsion
        prop_alloc = eng["allocations"]["propulsion"]
        if eng["warp_factor"] > 0:
            warp_cost = min(1000, eng["warp_factor"]**2 * 10)  # e.g., Warp 9 = 810 units/second
            if eng["energy"] >= warp_cost:
                eng["energy"] -= warp_cost
            else:
                eng["warp_factor"] = 0  # Warp disengages if energy insufficient
                self.common_data["debug"].append({"timestamp": sim_time, 
                                                 "message": "ENG: Warp disengaged - insufficient energy"})
        else:
            eng["impulse_speed"] = min(100, prop_alloc * 2)  # 1% alloc = 2% speed, capped at 100%

        # Process repair tasks (5%/second at 1 tick/second)
        for task in self.common_data.get("crew_tasks", []):
            if task["system"] in eng["system_health"] and eng["system_health"][task["system"]] < 100:
                rate = task.get("rate", 5)  # Default 5%, overrideable by Crew module
                task["progress"] += rate
                if task["progress"] >= task["target"]:
                    eng["system_health"][task["system"]] = min(100, task["target"])
                    self.common_data["crew_tasks"].remove(task)
                    self.common_data["debug"].append({"timestamp": sim_time, 
                                                     "message": f"ENG: {task['system']} repaired to {task['target']}%"})
                else:
                    eng["system_health"][task["system"]] = task["progress"]

        # Check for power surge event (5% chance at >95% allocation)
        if sum(eng["allocations"].values()) > 95 and random.random() < 0.05:
            eng["energy"] -= 50
            eng["surge"] = True
            self.common_data["debug"].append({"timestamp": sim_time, 
                                             "message": "ENG: Power surge detected -50 energy"})

    def handle_command(self, command, sim_time=None):
        """Handle engineering-specific commands with consistent sim_time."""
        parts = command.split()
        eng = self.common_data["engineering"]
        sim_time = sim_time or "Unknown Time"  # Fallback if sim_time not provided

        if not parts:
            return "No command provided."

        cmd = parts[0].lower()

        if cmd == "status":
            return self.get_status()

        elif cmd == "boost_shields" and len(parts) > 1:
            try:
                amount = int(parts[1])
                self.adjust_allocation("shields", amount)
                self.common_data["debug"].append({"timestamp": sim_time, 
                                                 "message": f"ENG: Shields boosted by {amount}%"})
                return f"Shields allocation set to {eng['allocations']['shields']}%"
            except ValueError:
                return "Invalid amount. Use: eng boost_shields <number>"

        elif cmd == "reroute_power" and len(parts) > 1:
            system = parts[1].lower()
            if system in ["shields", "weapons", "propulsion"]:
                self.adjust_allocation(system, eng["allocations"][system] + 20)  # +20% shift
                self.common_data["debug"].append({"timestamp": sim_time, 
                                                 "message": f"ENG: Power rerouted to {system}"})
                return f"Power rerouted to {system}: {eng['allocations'][system]}%"
            return "Invalid system. Use: shields, weapons, propulsion"

        elif cmd == "reserve" and len(parts) > 1:
            try:
                amount = int(parts[1])
                self.adjust_allocation("reserve", amount)
                self.common_data["debug"].append({"timestamp": sim_time, 
                                                 "message": f"ENG: Reserve set to {amount}%"})
                return f"Reserve set to {eng['allocations']['reserve']}%"
            except ValueError:
                return "Invalid amount. Use: eng reserve <number>"

        elif cmd == "warp" and len(parts) > 1:
            try:
                factor = float(parts[1])
                if 0 <= factor <= 10:
                    eng["warp_factor"] = factor
                    eng["impulse_speed"] = 0  # Warp overrides impulse
                    warp_cost = min(1000, factor**2 * 10)
                    self.common_data["debug"].append({"timestamp": sim_time, 
                                                     "message": f"ENG: Warp set to {factor}, cost {warp_cost} energy/tick"})
                    return f"Warp engaged at factor {factor}"
                return "Warp factor must be between 0 and 10."
            except ValueError:
                return "Invalid factor. Use: eng warp <number>"

        elif cmd == "repair" and len(parts) > 1:
            system = parts[1].lower()
            if system in eng["system_health"] and eng["system_health"][system] < 100:
                task = {"system": system, "progress": eng["system_health"][system], "target": 100}
                self.common_data["crew_tasks"].append(task)
                self.common_data["debug"].append({"timestamp": sim_time, 
                                                 "message": f"ENG: Repair task queued for {system}"})
                return f"Repair task queued for {system}"
            return f"{system} is either fully repaired or invalid."

        elif cmd == "set_max_energy" and len(parts) > 1:
            try:
                amount = int(parts[1])
                if amount >= 100:  # Minimum reasonable cap
                    eng["max_energy"] = amount
                    eng["energy"] = min(eng["energy"], eng["max_energy"])  # Clamp current energy
                    self.common_data["debug"].append({"timestamp": sim_time, 
                                                     "message": f"ENG: Max energy set to {amount}"})
                    return f"Max energy capacity set to {eng['max_energy']}"
                return "Max energy must be at least 100."
            except ValueError:
                return "Invalid amount. Use: eng set_max_energy <number>"

        return super().handle_command(command)

    def adjust_allocation(self, system, amount):
        """Adjust energy allocation, ensuring total ≤ 100%."""
        eng = self.common_data["engineering"]
        current = eng["allocations"]
        
        # Cap amount at 100
        amount = min(100, max(0, amount))
        total = sum(current.values()) - current[system] + amount
        
        if total > 100:
            # Scale other systems proportionally
            scale = (100 - amount) / (total - amount)
            for key in current:
                if key != system:
                    current[key] *= scale
        current[system] = amount
        
        # Auto-adjust reserve
        current["reserve"] = 100 - sum([current[k] for k in current if k != "reserve"])

    def get_status(self):
        """Return structured status for UI parsing."""
        eng = self.common_data["engineering"]
        alloc = eng["allocations"]
        return (f"Energy: {eng['energy']}/{eng['max_energy']}|"
                f"Shields: {eng['shields']:.1f}%|"
                f"Alloc-Shields: {alloc['shields']}%|"
                f"Alloc-Weapons: {alloc['weapons']}%|"
                f"Alloc-Propulsion: {alloc['propulsion']}%|"
                f"Alloc-Reserve: {alloc['reserve']}%|"
                f"Impulse: {eng['impulse_speed']}%|"
                f"Warp: {eng['warp_factor']}|"
                f"Health-Shields: {eng['system_health']['shields']}%|"
                f"Health-Weapons: {eng['system_health']['weapons']}%|"
                f"Health-Propulsion: {eng['system_health']['propulsion']}%")