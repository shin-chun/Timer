# main.py

import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
# from manager.main_window_manager import MainWindowManager
# from hotkey.listen_key import hotkeylistener
# from manager.data_manager import DataManager

def main():
    # Step 1: 初始化 Qt 應用
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

    # # Step 2: 載入使用者設定（如有）
    # settings = load_user_settings()
    #
    # # Step 3: 建立主視窗管理器
    # window_manager = WindowManager(settings=settings)
    # window_manager.show_main_window()
    #
    # # Step 4: 啟動快捷鍵監聽（非阻塞）
    # start_hotkey_listener(callback=window_manager.toggle_timer_window)

    # Step 5: 進入事件迴圈
    sys.exit(app.exec())

if __name__ == "__main__":
    main()