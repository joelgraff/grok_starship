import random

class EnergyManager:
    """Manages main energy and warp energy, including regeneration and power surges."""
    def __init__(self, common_data):
        self.common_data = common_data

    def update(self, sim_time):
        """Update energy and warp energy states."""
        eng = self.common_data["engineering"]

        # Regenerate main energy
        if eng["energy"] < eng["max_energy"]:
            eng["energy"] = min(eng["max_energy"], int(eng["energy"] + 5))

        # Regenerate warp energy
        if eng["warp_energy"] < eng["max_warp_energy"]:
            eng["warp_energy"] = min(eng["max_warp_energy"], int(eng["warp_energy"] + 10))

        # Power surge event (affects main energy)
        if eng["energy"] > eng["max_energy"] * 0.95 and random.random() < 0.05:
            eng["energy"] = int(eng["energy"] - 50)
            eng["surge"] = True
            self.common_data["debug"].append({"timestamp": sim_time,
                                             "message": "ENG: Power surge detected -50 energy"})
        else:
            eng["surge"] = False