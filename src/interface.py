# src/interface.py
import tkinter as tk
from src.simulation import StarshipSimulation

class StarshipInterface:
    def __init__(self, simulation):
        self.simulation = simulation
        self.root = tk.Tk()
        self.root.title("Starship Simulation")
        self.paused = False
        
        self.bridge_frame = tk.Frame(self.root, width=400, height=300, bg="gray")
        self.bridge_frame.grid(row=0, column=0)
        self.engineering_frame = tk.Frame(self.root, width=400, height=300, bg="gray")
        self.engineering_frame.grid(row=0, column=1)
        self.crew_frame = tk.Frame(self.root, width=800, height=300, bg="gray")
        self.crew_frame.grid(row=1, column=0, columnspan=2)

        self.crew_label = tk.Label(self.crew_frame, text="", bg="gray", fg="white", justify="left")
        self.crew_label.pack()

        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=2, column=0, columnspan=2)

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")

    def update_display(self):
        crew_text = "\n".join(
            f"{agent.name}: {agent.role}, Health: {agent.health}, Mood: {agent.mood}, Pos: {agent.position}, Task: {agent.task.name if agent.task else 'None'}"
            for agent in self.simulation.crew
        )
        self.crew_label.config(text=crew_text)
        
        if not self.paused:
            self.simulation.step()
        self.root.after(1000, self.update_display)  # Update every second

    def run(self):
        self.update_display()
        self.root.mainloop()