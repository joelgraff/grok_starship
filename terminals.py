# terminals.py
import tkinter as tk
from tkinter import ttk

class TerminalWindow:
    def __init__(self, starship, ship_model, title, role):
        self.starship = starship
        self.ship_model = ship_model
        self.role = role
        self.root = tk.Tk()
        self.root.title(title)
        self.display = tk.Text(self.root, height=10, width=50)
        self.display.pack()
        self.entry = ttk.Entry(self.root)
        self.entry.pack()
        self.entry.bind("<Return>", self.send_command)
        self.step_button = ttk.Button(self.root, text="Step", command=self.step)
        self.step_button.pack()

    def step(self):
        self.ship_model.step()
        self.update_display()

    def send_command(self, event):
        command = self.entry.get()
        self.starship.process_command(command)
        self.entry.delete(0, tk.END)
        self.update_display()

    def update_display(self):
        pass

    def run(self):
        self.update_display()
        self.root.mainloop()

class CaptainWindow(TerminalWindow):
    def __init__(self, starship, ship_model):
        super().__init__(starship, ship_model, "Starship - Captain", "Captain")

    def update_display(self):
        self.display.delete(1.0, tk.END)
        text = f"Position: ({self.starship.x:.1f}, {self.starship.y:.1f})\n"
        text += f"Velocity: Warp {self.starship.velocity}\n"
        text += "Recent Logs:\n" + "\n".join(self.starship.log[-5:])
        self.display.insert(tk.END, text)

class NavigatorWindow(TerminalWindow):
    def __init__(self, starship, ship_model):
        super().__init__(starship, ship_model, "Starship - Navigator", "Navigator")

    def update_display(self):
        self.display.delete(1.0, tk.END)
        text = f"Position: ({self.starship.x:.1f}, {self.starship.y:.1f})\n"
        crew = [a for a in self.ship_model.schedule.agents if a.role == "Navigator"]
        text += f"Navigators: {len(crew)} active\n"
        if crew:
            text += f"Lead: {crew[0].name}, Pos: {crew[0].pos}"
        self.display.insert(tk.END, text)

class EngineerWindow(TerminalWindow):
    def __init__(self, starship, ship_model):
        super().__init__(starship, ship_model, "Starship - Engineer", "Engineer")

    def update_display(self):
        self.display.delete(1.0, tk.END)
        text = f"Energy: {self.starship.energy:.1f} units\n"
        text += f"Shields: {self.starship.shields}%\n"
        engineers = [a for a in self.ship_model.schedule.agents if a.role == "Engineer"]
        text += f"Engineers: {len(engineers)} active\n"
        tasks = [t for t in self.starship.tasks if "Repair" in t[0]]
        if tasks:
            text += "Tasks:\n" + "\n".join(f"{t[0]}: {t[2]}/{t[1]}" for t in tasks)
        self.display.insert(tk.END, text)

class CommunicatorWindow(TerminalWindow):
    def __init__(self, starship, ship_model):
        super().__init__(starship, ship_model, "Starship - Communicator", "Communicator")

    def update_display(self):
        self.display.delete(1.0, tk.END)
        text = "Communications Log:\n" + "\n".join(self.starship.log[-5:])
        communicators = [a for a in self.ship_model.schedule.agents if a.role == "Communicator"]
        text += f"\nCommunicators: {len(communicators)} active"
        self.display.insert(tk.END, text)

class ScientistWindow(TerminalWindow):
    def __init__(self, starship, ship_model):
        super().__init__(starship, ship_model, "Starship - Scientist", "Scientist")

    def update_display(self):
        self.display.delete(1.0, tk.END)
        text = f"Energy: {self.starship.energy:.1f} units\n"
        scientists = [a for a in self.ship_model.schedule.agents if a.role == "Scientist"]
        text += f"Scientists: {len(scientists)} active\n"
        tasks = [t for t in self.starship.tasks if "Treat" in t[0]]
        if tasks:
            text += "Tasks:\n" + "\n".join(f"{t[0]}: {t[2]}/{t[1]}" for t in tasks)
        self.display.insert(tk.END, text)