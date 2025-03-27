# main.py

import threading
from models import StarshipModel, ShipModel
from visuals import ShipWindow
from terminals import (CaptainWindow, NavigatorWindow, EngineerWindow,
                      CommunicatorWindow, ScientistWindow)

def main():
    starship = StarshipModel()
    ship_model = ShipModel(starship)

    # Start ship interior in a thread
    ship_window = ShipWindow(ship_model)
    ship_thread = threading.Thread(target=ship_window.run)
    ship_thread.daemon = True
    ship_thread.start()

    # Start all five station windows in threads
    windows = [
        CaptainWindow(starship, ship_model),
        NavigatorWindow(starship, ship_model),
        EngineerWindow(starship, ship_model),
        CommunicatorWindow(starship, ship_model),
        ScientistWindow(starship, ship_model),
    ]
    threads = []
    for window in windows[:-1]:
        t = threading.Thread(target=window.run)
        t.daemon = True
        t.start()
        threads.append(t)

    # Run Scientist in main thread
    windows[-1].run()

if __name__ == "__main__":
    main()