# src/gui/panels/engineering_status.py
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QFont
from ..custom_progress import CustomProgressBar

def setup_engineering_status(app, module, layout, font):
    status = module.get_status()
    eng_data = {k.split(': ')[0]: k.split(': ')[1] for k in status.split('|')}
    energy_bar = CustomProgressBar()
    energy_bar.setMaximum(app.common_data["engineering"]["max_energy"])
    energy_bar.setValue(int(eng_data["Energy"].split('/')[0]))
    energy_bar.setCustomText(f"Energy: {eng_data['Energy']}")
    energy_bar.setFont(font)
    warp_energy_bar = CustomProgressBar()
    warp_energy_bar.setMaximum(int(eng_data["Warp Energy"].split('/')[1]))
    warp_energy_bar.setValue(int(eng_data["Warp Energy"].split('/')[0]))
    warp_energy_bar.setCustomText(f"Warp Energy: {eng_data['Warp Energy']}")
    warp_energy_bar.setFont(font)
    shields_bar = CustomProgressBar()
    shields_bar.setMaximum(100)
    shields_bar.setValue(int(float(eng_data["Shields"].rstrip('%'))))
    shields_bar.setCustomText(f"Shields: {eng_data['Shields']}")
    shields_bar.setFont(font)
    alloc_separator = QFrame()
    alloc_separator.setFrameShape(QFrame.HLine)
    alloc_separator.setFrameShadow(QFrame.Sunken)
    alloc_shields_bar = CustomProgressBar()
    alloc_shields_bar.setMaximum(100)
    alloc_shields_val = int(float(eng_data['Alloc-Shields'].rstrip('%')))
    alloc_shields_bar.setValue(alloc_shields_val)
    alloc_shields_bar.setCustomText(f"Shields Alloc: {alloc_shields_val}%")
    alloc_shields_bar.setFont(font)
    alloc_weapons_bar = CustomProgressBar()
    alloc_weapons_bar.setMaximum(100)
    alloc_weapons_val = int(float(eng_data['Alloc-Weapons'].rstrip('%')))
    alloc_weapons_bar.setValue(alloc_weapons_val)
    alloc_weapons_bar.setCustomText(f"Weapons Alloc: {alloc_weapons_val}%")
    alloc_weapons_bar.setFont(font)
    alloc_propulsion_bar = CustomProgressBar()
    alloc_propulsion_bar.setMaximum(100)
    alloc_propulsion_val = int(float(eng_data['Alloc-Propulsion'].rstrip('%')))
    alloc_propulsion_bar.setValue(alloc_propulsion_val)
    alloc_propulsion_bar.setCustomText(f"Propulsion Alloc: {alloc_propulsion_val}%")
    alloc_propulsion_bar.setFont(font)
    alloc_reserve_bar = CustomProgressBar()
    alloc_reserve_bar.setMaximum(100)
    alloc_reserve_val = int(float(eng_data['Alloc-Reserve'].rstrip('%')))
    alloc_reserve_bar.setValue(alloc_reserve_val)
    alloc_reserve_bar.setCustomText(f"Reserve Alloc: {alloc_reserve_val}%")
    alloc_reserve_bar.setFont(font)
    propulsion_separator = QFrame()
    propulsion_separator.setFrameShape(QFrame.HLine)
    propulsion_separator.setFrameShadow(QFrame.Sunken)
    impulse_bar = CustomProgressBar()
    impulse_bar.setMaximum(100)
    impulse_val = int(float(eng_data['Impulse'].rstrip('%')))
    impulse_bar.setValue(impulse_val)
    impulse_bar.setCustomText(f"Impulse: {impulse_val}%")
    impulse_bar.setFont(font)
    impulse_bar.setStyleSheet("""
        QProgressBar {
            border: 1px solid gray;
            background-color: #444444;
            color: white;
            text-align: center;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #006400, stop:1 #FFD700);
        }
    """)
    warp_bar = CustomProgressBar()
    warp_bar.setMaximum(10)
    warp_val = int(float(eng_data['Warp']))
    warp_bar.setValue(warp_val)
    warp_bar.setCustomText(f"Warp: {warp_val}")
    warp_bar.setFont(font)
    warp_bar.setStyleSheet("""
        QProgressBar {
            border: 1px solid gray;
            background-color: #444444;
            color: white;
            text-align: center;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 blue, stop:1 red);
        }
    """)
    health_separator = QFrame()
    health_separator.setFrameShape(QFrame.HLine)
    health_separator.setFrameShadow(QFrame.Sunken)
    health_shields_bar = CustomProgressBar()
    health_shields_bar.setMaximum(100)
    health_shields_val = int(float(eng_data['Health-Shields'].rstrip('%')))
    health_shields_bar.setValue(health_shields_val)
    health_shields_bar.setCustomText(f"Shields Health: {health_shields_val}%")
    health_shields_bar.setFont(font)
    health_weapons_bar = CustomProgressBar()
    health_weapons_bar.setMaximum(100)
    health_weapons_val = int(float(eng_data['Health-Weapons'].rstrip('%')))
    health_weapons_bar.setValue(health_weapons_val)
    health_weapons_bar.setCustomText(f"Weapons Health: {health_weapons_val}%")
    health_weapons_bar.setFont(font)
    health_propulsion_bar = CustomProgressBar()
    health_propulsion_bar.setMaximum(100)
    health_propulsion_val = int(float(eng_data['Health-Propulsion'].rstrip('%')))
    health_propulsion_bar.setValue(health_propulsion_val)
    health_propulsion_bar.setCustomText(f"Propulsion Health: {health_propulsion_val}%")
    health_propulsion_bar.setFont(font)
    for bar in [energy_bar, warp_energy_bar, shields_bar, alloc_shields_bar, alloc_weapons_bar,
                alloc_propulsion_bar, alloc_reserve_bar, health_shields_bar,
                health_weapons_bar, health_propulsion_bar]:
        bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid gray;
                background-color: #444444;
                color: white;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #008080;
            }
        """)
    layout.addWidget(energy_bar)
    layout.addWidget(warp_energy_bar)
    layout.addWidget(shields_bar)
    layout.addWidget(alloc_separator)
    layout.addWidget(alloc_shields_bar)
    layout.addWidget(alloc_weapons_bar)
    layout.addWidget(alloc_propulsion_bar)
    layout.addWidget(alloc_reserve_bar)
    layout.addWidget(propulsion_separator)
    layout.addWidget(impulse_bar)
    layout.addWidget(warp_bar)
    layout.addWidget(health_separator)
    layout.addWidget(health_shields_bar)
    layout.addWidget(health_weapons_bar)
    layout.addWidget(health_propulsion_bar)
    app.module_bars["engineering"] = {
        "energy": energy_bar,
        "warp_energy": warp_energy_bar,
        "shields": shields_bar,
        "alloc_shields": alloc_shields_bar,
        "alloc_weapons": alloc_weapons_bar,
        "alloc_propulsion": alloc_propulsion_bar,
        "alloc_reserve": alloc_reserve_bar,
        "impulse": impulse_bar,
        "warp": warp_bar,
        "health_shields": health_shields_bar,
        "health_weapons": health_weapons_bar,
        "health_propulsion": health_propulsion_bar
    }
    app.module_labels[module.name] = [None] * 11  # Empty list, no labels used