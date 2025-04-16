import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
from community_simulator import CommunitySimulator

class CommunityUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Starship Community Simulator")
        self.common_data = {
            "simulation": {"tick_count": 0},
            "engineering": {
                "system_health": {"propulsion": 100, "shields": 100, "weapons": 100},
                "shields": 100
            },
            "debug": []
        }
        self.ship = type('Ship', (), {'status': 'Nominal'})()
        self.simulator = CommunitySimulator(self.ship, self.common_data)
        self.simulator.initialize(crew_size=200)

        # Metric history for plots
        self.morale_history = []
        self.stress_history = []
        self.fatigue_history = []
        self.time_steps = []

        # Log history
        self.log_entries = []

        # UI Layout
        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Metrics Tab
        metrics_tab = ttk.Frame(self.notebook)
        self.notebook.add(metrics_tab, text="Metrics")

        control_frame = ttk.LabelFrame(metrics_tab, text="Controls")
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(control_frame, text="Start", command=self.start_simulation).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_simulation).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Step", command=self.step_simulation).grid(row=0, column=2, padx=5)

        scenario_frame = ttk.LabelFrame(metrics_tab, text="Trigger Scenarios")
        scenario_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(scenario_frame, text="System Failure", command=lambda: self.trigger_scenario("system_failure")).grid(row=0, column=0, padx=5)
        ttk.Button(scenario_frame, text="Social Gathering", command=lambda: self.trigger_scenario("social_gathering")).grid(row=0, column=1, padx=5)
        ttk.Button(scenario_frame, text="Crisis", command=lambda: self.trigger_scenario("crisis")).grid(row=0, column=2, padx=5)

        metrics_frame = ttk.LabelFrame(metrics_tab, text="Crew Metrics")
        metrics_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.metrics_label = ttk.Label(metrics_frame, text="Time Step: 0\nScenarios: 0\nMorale: 0\nStress: 0\nFatigue: 0")
        self.metrics_label.grid(row=0, column=0, padx=5, pady=5)

        plot_frame = ttk.LabelFrame(metrics_tab, text="Metric Trends")
        plot_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

        # Crew Tab
        crew_tab = ttk.Frame(self.notebook)
        self.notebook.add(crew_tab, text="Crew")

        crew_frame = ttk.LabelFrame(crew_tab, text="Crew Details (Sample of 10)")
        crew_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.crew_text = scrolledtext.ScrolledText(crew_frame, width=50, height=10)
        self.crew_text.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(crew_frame, text="Refresh", command=self.update_crew_details).grid(row=1, column=0, padx=5)

        # Events Tab
        events_tab = ttk.Frame(self.notebook)
        self.notebook.add(events_tab, text="Events")

        events_frame = ttk.LabelFrame(events_tab, text="Active Scenarios")
        events_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.events_text = scrolledtext.ScrolledText(events_frame, width=50, height=10)
        self.events_text.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(events_frame, text="Refresh", command=self.update_event_details).grid(row=1, column=0, padx=5)

        # Relationships Tab
        rel_tab = ttk.Frame(self.notebook)
        self.notebook.add(rel_tab, text="Relationships")

        rel_frame = ttk.LabelFrame(rel_tab, text="Full Relationship Network")
        rel_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.rel_fig, self.rel_ax = plt.subplots(figsize=(5, 3))
        self.rel_canvas = FigureCanvasTkAgg(self.rel_fig, master=rel_frame)
        self.rel_canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Recent Log (Last 20 Events)")
        log_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.log_text = scrolledtext.ScrolledText(log_frame, width=60, height=5)
        self.log_text.grid(row=0, column=0, padx=5, pady=5)

    def start_simulation(self):
        self.simulator.running = True
        self.run_simulation()

    def pause_simulation(self):
        self.simulator.running = False

    def step_simulation(self):
        self.simulator.running = True
        self.simulator.update()
        self.update_ui()
        self.simulator.running = False

    def run_simulation(self):
        if self.simulator.running:
            self.simulator.update()
            self.update_ui()
            self.root.after(1000, self.run_simulation)

    def trigger_scenario(self, event_type):
        scenario = self.simulator.trigger_event(event_type)
        if scenario:
            entry = f"Step {self.simulator.time_step}: Triggered {event_type}: {scenario['type']} at {scenario['location']} with {len(scenario['participants'])} crew"
            self.log_entries.append(entry)
            if len(self.log_entries) > 20:
                self.log_entries.pop(0)
            self.update_log()

    def update_ui(self):
        status = self.simulator.get_status()
        metrics_text = (
            f"Time Step: {status['time_step']}\n"
            f"Active Scenarios: {status['active_scenarios']}\n"
            f"Morale: {status['crew_stats']['avg_morale']:.1f}\n"
            f"Stress: {status['crew_stats']['avg_stress']:.1f}\n"
            f"Fatigue: {status['crew_stats']['avg_fatigue']:.1f}"
        )
        self.metrics_label.config(text=metrics_text)

        # Update metric history
        self.time_steps.append(status['time_step'])
        self.morale_history.append(status['crew_stats']['avg_morale'])
        self.stress_history.append(status['crew_stats']['avg_stress'])
        self.fatigue_history.append(status['crew_stats']['avg_fatigue'])
        if len(self.time_steps) > 50:
            self.time_steps.pop(0)
            self.morale_history.pop(0)
            self.stress_history.pop(0)
            self.fatigue_history.pop(0)

        # Update metric plots
        self.ax.clear()
        self.ax.plot(self.time_steps, self.morale_history, label="Morale", color="green")
        self.ax.plot(self.time_steps, self.stress_history, label="Stress", color="red")
        self.ax.plot(self.time_steps, self.fatigue_history, label="Fatigue", color="blue")
        self.ax.set_xlabel("Time Step")
        self.ax.set_ylabel("Value")
        self.ax.legend()
        self.ax.set_ylim(0, 100)
        self.canvas.draw()

        # Update relationship graph
        self.rel_ax.clear()
        nodes, edges = self.simulator.get_relationship_graph()
        theta = [2 * math.pi * i / len(nodes) for i in range(len(nodes))]
        x = [math.cos(t) for t in theta]
        y = [math.sin(t) for t in theta]
        sampled_edges = random.sample(edges, min(500, len(edges)))
        for edge in sampled_edges:
            i1, i2 = nodes.index(edge[0]), nodes.index(edge[1])
            alpha = edge[2]
            self.rel_ax.plot([x[i1], x[i2]], [y[i1], y[i2]], 'k-', alpha=alpha * 0.5 + 0.1)
        for i in range(len(nodes)):
            self.rel_ax.plot(x[i], y[i], 'o', markersize=3, color='blue')
        self.rel_ax.set_xticks([])
        self.rel_ax.set_yticks([])
        self.rel_ax.set_title(f"Relationships ({len(sampled_edges)} of {len(edges)} edges)")
        self.rel_canvas.draw()

        self.update_crew_details()
        self.update_event_details()
        self.update_log()

    def update_crew_details(self):
        self.crew_text.delete(1.0, tk.END)
        crew_details = self.simulator.get_crew_details()
        for crew in crew_details:
            rels = ", ".join([f"Crew {k} ({v['type']}, A:{v['affinity']:.2f})" for k, v in crew["relationships"].items()]) or "None"
            text = (
                f"ID: {crew['id']}\n"
                f"Role: {crew['role']}\n"
                f"Status: {crew['status']}\n"
                f"Morale: {crew['morale']:.1f}, Stress: {crew['stress']:.1f}\n"
                f"Relationships: {rels}\n"
                f"---\n"
            )
            self.crew_text.insert(tk.END, text)
        self.crew_text.see(tk.END)

    def update_event_details(self):
        self.events_text.delete(1.0, tk.END)
        scenarios = self.simulator.get_scenario_details()
        if not scenarios:
            self.events_text.insert(tk.END, "No active scenarios.\n")
        for scenario in scenarios:
            participants = ", ".join([f"Crew {p['id']} ({p['role']}, {p['status']})" for p in scenario["participants"]])
            outcomes = "\n".join(scenario["outcomes"]) or "No outcomes yet."
            text = (
                f"Scenario: {scenario['type'].capitalize()} at {scenario['location']}\n"
                f"Progress: {scenario['progress']:.1f}/{scenario['duration']}\n"
                f"Participants: {participants}\n"
                f"Outcomes:\n{outcomes}\n"
                f"---\n"
            )
            self.events_text.insert(tk.END, text)
        self.events_text.see(tk.END)

    def update_log(self):
        self.log_text.delete(1.0, tk.END)
        for entry in self.log_entries:
            self.log_text.insert(tk.END, f"{entry}\n")
        for debug in self.common_data["debug"][-5:]:
            self.log_text.insert(tk.END, f"Step {debug['time']}: {debug['event']}\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CommunityUI(root)
    root.mainloop()