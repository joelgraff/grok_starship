# main.py
import sys
from PyQt5.QtWidgets import QApplication
from simulation import StarShipApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StarShipApp()
    window.show()
    sys.exit(app.exec_())