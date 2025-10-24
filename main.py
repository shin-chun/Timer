# main.py

import sys
from PySide6.QtWidgets import QApplication
from core.gui.main_window import MainWindow
from core.manager.timer_manager import TimerManager


# from manager.main_window_manager import MainWindowManager
# from hotkey.listen_key import hotkeylistener
# from manager.data_manager import DataManager

def main():
    # Step 1: 初始化 Qt 應用
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()