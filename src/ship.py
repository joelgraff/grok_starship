# src/ship.py
import logging

logger = logging.getLogger(__name__)  # Use shared config from simulation.py

class Starship:
    def __init__(self, layout):
        self.layout = layout
        self.systems = {
            "navigation": {"status": "operational", "integrity": 100},
            "engineering": {"status": "operational", "integrity": 100},
            "hull": {"status": "operational", "integrity": 100},
            "security": {"status": "operational", "integrity": 100}
        }
        logger.info("Ship initialized with systems: %s", self.systems, extra={'sim': None})

    def update_system(self, system, status=None, integrity_change=0):
        if system in self.systems:
            old_state = self.systems[system].copy()
            if status:
                self.systems[system]["status"] = status
            self.systems[system]["integrity"] = max(0, min(100, self.systems[system]["integrity"] + integrity_change))
            logger.info(
                "System %s updated: %s -> %s",
                system, old_state, self.systems[system],
                extra={'sim': None}  # Will be set when called from tasks
            )