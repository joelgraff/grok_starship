from modules.module import Module
from .energy_manager import EnergyManager
from .propulsion_manager import PropulsionManager
from .shields_manager import ShieldsManager
from .command_handler import CommandHandler
from .status_reporter import StatusReporter

class Engineering(Module):
    """Core Engineering module coordinating energy, propulsion, shields, and commands."""
    def __init__(self, ship, common_data=None):
        super().__init__(ship)
        self.name = "Engineering"
        self.common_data = common_data or {}
        self.energy_mgr = EnergyManager(self.common_data)
        self.propulsion_mgr = PropulsionManager(self.common_data)
        self.shields_mgr = ShieldsManager(self.common_data)
        self.command_handler = CommandHandler(self.common_data)
        self.status_reporter = StatusReporter(self.common_data)

        # Initialize engineering state if not set
        if "engineering" not in self.common_data:
            self.common_data["engineering"] = {
                "energy": 1000,
                "max_energy": 2000,
                "warp_energy": 1500,
                "max_warp_energy": 1500,
                "allocations": {"shields": 30, "weapons": 20, "propulsion": 40, "reserve": 10},
                "shields": 100,
                "system_health": {"shields": 100, "weapons": 100, "propulsion": 100},
                "impulse_speed": 50,
                "warp_factor": 0,
                "surge": False,
                "warp_duration": 0
            }

    def update(self, sim_time=None):
        """Update all engineering systems each tick."""
        sim_time = sim_time or "Unknown Time"
        self.energy_mgr.update(sim_time)
        self.propulsion_mgr.update(sim_time)
        self.shields_mgr.update(sim_time)
        # Process crew repair tasks
        eng = self.common_data["engineering"]
        for task in self.common_data.get("crew_tasks", []):
            if task["system"] in eng["system_health"] and eng["system_health"][task["system"]] < 100:
                rate = task.get("rate", 5)
                task["progress"] += rate
                if task["progress"] >= task["target"]:
                    eng["system_health"][task["system"]] = min(100, task["target"])
                    self.common_data["crew_tasks"].remove(task)
                    self.common_data["debug"].append({"timestamp": sim_time,
                                                     "message": f"ENG: {task['system']} repaired to {task['target']}%"})
                else:
                    eng["system_health"][task["system"]] = task["progress"]

    def handle_command(self, command, sim_time=None):
        """Handle engineering commands via command handler."""
        return self.command_handler.handle_command(command, sim_time)

    def get_status(self):
        """Return formatted status string for UI."""
        return self.status_reporter.get_status()