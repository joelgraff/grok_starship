class StatusReporter:
    """Formats engineering status for UI display."""
    def __init__(self, common_data):
        self.common_data = common_data

    def get_status(self):
        """Return formatted status string."""
        eng = self.common_data["engineering"]
        alloc = eng["allocations"]
        return (f"Energy: {eng['energy']}/{eng['max_energy']}|"
                f"Warp Energy: {eng['warp_energy']}/{eng['max_warp_energy']}|"
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