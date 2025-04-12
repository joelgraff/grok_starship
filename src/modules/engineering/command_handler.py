class CommandHandler:
    """Processes engineering commands and manages allocations."""
    def __init__(self, common_data):
        self.common_data = common_data

    def handle_command(self, command, sim_time):
        """Handle engineering-specific commands."""
        parts = command.split()
        eng = self.common_data["engineering"]
        sim_time = sim_time or "Unknown Time"

        if not parts:
            return "No command provided."
        cmd = parts[0].lower()

        if cmd == "boost_shields" and len(parts) > 1:
            try:
                amount = int(parts[1])
                self.adjust_allocation("shields", amount)
                self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Shields boosted by {amount}%"})
                return f"Shields allocation set to {eng['allocations']['shields']}%"
            except ValueError:
                return "Invalid amount. Use: eng boost_shields <number>"

        elif cmd == "reroute_power" and len(parts) > 1:
            system = parts[1].lower()
            if system in ["shields", "weapons", "propulsion"]:
                self.adjust_allocation(system, eng["allocations"][system] + 20)
                self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Power rerouted to {system}"})
                return f"Power rerouted to {system}: {eng['allocations'][system]}%"
            return "Invalid system. Use: shields, weapons, propulsion"

        elif cmd == "reserve" and len(parts) > 1:
            try:
                amount = int(parts[1])
                self.adjust_allocation("reserve", amount)
                self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Reserve set to {amount}%"})
                return f"Reserve set to {eng['allocations']['reserve']}%"
            except ValueError:
                return "Invalid amount. Use: eng reserve <number>"

        elif cmd == "warp" and len(parts) > 1:
            try:
                factor = float(parts[1])
                if 0 <= factor <= 10:
                    eng["warp_factor"] = factor
                    eng["impulse_speed"] = 0
                    warp_cost = min(1000, factor * 75)
                    self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Warp set to {factor}, cost {warp_cost} warp energy/tick"})
                    return f"Warp engaged at factor {factor}"
                return "Warp factor must be between 0 and 10."
            except ValueError:
                return "Invalid factor. Use: eng warp <number>"

        elif cmd == "repair" and len(parts) > 1:
            system = parts[1].lower()
            if system in eng["system_health"] and eng["system_health"][system] < 100:
                task = {"system": system, "progress": eng["system_health"][system], "target": 100}
                self.common_data["crew_tasks"].append(task)
                self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Repair task queued for {system}"})
                return f"Repair task queued for {system}"
            return f"{system} is either fully repaired or invalid."

        elif cmd == "set_max_energy" and len(parts) > 1:
            try:
                amount = int(parts[1])
                if amount >= 100:
                    eng["max_energy"] = amount
                    eng["energy"] = min(eng["energy"], eng["max_energy"])
                    self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Max energy set to {amount}"})
                    return f"Max energy capacity set to {eng['max_energy']}"
                return "Max energy must be at least 100."
            except ValueError:
                return "Invalid amount. Use: eng set_max_energy <number>"

        elif cmd == "set_max_warp_energy" and len(parts) > 1:
            try:
                amount = int(parts[1])
                if amount >= 100:
                    eng["max_warp_energy"] = amount
                    eng["warp_energy"] = min(eng["warp_energy"], eng["max_warp_energy"])
                    self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Max warp energy set to {amount}"})
                    return f"Max warp energy capacity set to {eng['max_warp_energy']}"
                return "Max warp energy must be at least 100."
            except ValueError:
                return "Invalid amount. Use: eng set_max_warp_energy <number>"

        elif cmd == "refuel_warp" and len(parts) > 1:
            try:
                amount = int(parts[1])
                if amount >= 0:
                    eng["warp_energy"] = min(eng["max_warp_energy"], int(eng["warp_energy"] + amount))
                    self.common_data["debug"].append({"timestamp": sim_time, "message": f"ENG: Warp energy refueled by {amount}"})
                    return f"Warp energy now at {eng['warp_energy']}/{eng['max_warp_energy']}"
                return "Amount must be non-negative."
            except ValueError:
                return "Invalid amount. Use: eng refuel_warp <number>"

        elif cmd == "set_shield_health" and len(parts) > 1:
            try:
                amount = int(parts[1])
                if 0 <= amount <= 100:
                    eng["system_health"]["shields"] = amount
                    self.common_data["debug"].append({"timestamp": sim_time,
                                                    "message": f"ENG: Shield health set to {amount}%"})
                    return f"Shield health set to {amount}%"
                return "Health must be between 0 and 100."
            except ValueError:
                return "Invalid amount. Use: eng set_shield_health <number>"
        return "Unknown command."

    def adjust_allocation(self, system, amount):
        """Adjust energy allocation, ensuring total ≤ 100%."""
        eng = self.common_data["engineering"]
        current = eng["allocations"]
        amount = min(100, max(0, amount))
        total = sum(current.values()) - current[system] + amount
        if total > 100:
            scale = (100 - amount) / (total - amount)
            for key in current:
                if key != system:
                    current[key] *= scale
        current[system] = amount
        current["reserve"] = 100 - sum([current[k] for k in current if k != "reserve"])