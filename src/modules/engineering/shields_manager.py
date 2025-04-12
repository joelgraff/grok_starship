import random

class ShieldsManager:
    """Manages shields, including regeneration and overload events."""
    def __init__(self, common_data):
        self.common_data = common_data

    def update(self, sim_time):
        """Update shields state."""
        eng = self.common_data["engineering"]

        # Regenerate shields
        if eng["shields"] < 100:
            eng["shields"] = min(100, eng["shields"] + 5)

        # Shield overload event
        if eng["allocations"]["shields"] > 80 and eng["system_health"]["shields"] < 20 and random.random() < 0.10:
            eng["shields"] = 0
            self.common_data["debug"].append({"timestamp": sim_time,
                                             "message": "ENG: Shield overload—resetting"})