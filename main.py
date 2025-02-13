
from gui import RunWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Initialize QApplication
    window = RunWindow()          # Create the RunWindow instance
    window.show()                 # Show the window
    sys.exit(app.exec())          # Run the application loop

    