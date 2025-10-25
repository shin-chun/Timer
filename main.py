# main.py

import sys
from PySide6.QtWidgets import QApplication
from core.gui.main_window import MainWindow
from core.gui.timer_window import TimerWindow
# from core.manager.tick_manager import TickManager
from core.manager.timer_manager import TimerManager


# from manager.main_window_manager import MainWindowManager
# from hotkey.listen_key import hotkeylistener
# from manager.data_manager import DataManager



# def main():
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ 先創建唯一的 TimerManager 實例
    timer_manager = TimerManager()
    print(f"[DEBUG] 主程式 TimerManager: {id(timer_manager)}")

    # ✅ 注入到 MainWindow
    main_window = MainWindow(timer_manager)
    main_window.show()

    sys.exit(app.exec())