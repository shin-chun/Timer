# main.py
import sys

from PySide6.QtWidgets import QApplication

from core.gui.main_window import MainWindow
from core.manager.timer_manager import TimerManager
from core.utils.resource import resource_path





def main():
    app = QApplication(sys.argv)
    timer_manager = TimerManager()
    main_window = MainWindow(timer_manager)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()