class PropulsionManager:
    """Manages warp and impulse propulsion, including costs and strain events."""
    def __init__(self, common_data):
        self.common_data = common_data

    def update(self, sim_time):
        """Update propulsion states."""
        eng = self.common_data["engineering"]
        prop_alloc = eng["allocations"]["propulsion"]

        if eng["warp_factor"] > 0:
            warp_cost = min(1000, eng["warp_factor"] * 75)  # Warp 5 = 375 units/tick
            if eng["warp_energy"] >= warp_cost:
                eng["warp_energy"] = int(eng["warp_energy"] - warp_cost)
                eng["warp_duration"] += 1
            else:
                eng["warp_factor"] = 0
                eng["warp_duration"] = 0
                self.common_data["debug"].append({"timestamp": sim_time,
                                                 "message": "ENG: Warp disengaged - insufficient warp energy"})
        else:
            eng["warp_duration"] = 0
            eng["impulse_speed"] = min(100, prop_alloc * 2)

        # Propulsion strain event
        if eng["warp_factor"] > 7 and eng["warp_duration"] > 10 and random.random() < 0.05:
            eng["system_health"]["propulsion"] -= 10
            self.common_data["debug"].append({"timestamp": sim_time,
                                             "message": "ENG: Propulsion strain—health reduced"})