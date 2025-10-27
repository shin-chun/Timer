import sys

# 📦 視窗與應用程式
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QApplication, QDialog
)
# 📐 Layout 排版
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout
)
# 🎛️ 控制元件與列表
from PySide6.QtWidgets import (
    QPushButton, QListWidget, QListWidgetItem, QLabel, QFileDialog
)
# 📏 尺寸與樣式
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from core.gui.timer_window import TimerWindow
from core.hotkey.listen_key import HotkeyListener
from core.manager.data_manager import data_manager
from core.gui.edit_window import EditWindow
from core.manager.timer_manager import TimerManager
from core.model.timer_factory import KeyState, TimerConfig


class MainWindow(QMainWindow):
    def __init__(self, manager: TimerManager):
        super().__init__()
        self.setWindowTitle("ElswordTimer")
        self.setGeometry(100, 100, 600, 450)

        self.setStyleSheet("""
            QWidget { background-color: #f0f4f8; }
            QPushButton {
                background-color: #E0E0E0;
                color: black;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                min-width: 100px;
                min-height: 40px;
            }
            QPushButton:hover { background-color: #357ABD; }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                padding: 6px;
            }
        """)

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)

        # 初始化 UI 元件
        self.timer_list = QListWidget()
        self.timer_list.setFont(font)

        grid_layout = self.init_buttons(font)
        bottom_button_layout = self.init_bottom_button(font)
        label = self.init_label(font)

        # 主 layout 包裝成 central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.timer_list)
        main_layout.addLayout(bottom_button_layout)
        main_layout.addWidget(label)

        self.setCentralWidget(central_widget)
        data_manager.subscribe(self.on_timer_updated)

        self.timer_list.itemDoubleClicked.connect(self.edit_timer)

        self.timer_manager = manager
        self.timer_windows = []

        self.hotkey_listener = HotkeyListener(self.timer_manager)

    def init_buttons(self, font):
        grid_layout = QGridLayout()
        self.buttons = []

        buttons_labels = [
            '新增計時器', '編輯計時器', '儲存檔案',
            '刪除計時器', '重置計時器', '匯入設定檔'
        ]

        for i, label in enumerate(buttons_labels):
            btn = QPushButton(label)
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.clicked.connect(lambda _, idx=i: self.handle_button_click(idx))
            self.buttons.append(btn)
            grid_layout.addWidget(btn, i // 3, i % 3)

        return grid_layout

    def init_bottom_button(self, font):
        self.bottom_button = QPushButton("啟動計時器")  # ✅ 綁定成屬性
        self.bottom_button.setFont(font)
        self.bottom_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.bottom_button.clicked.connect(self.handle_timer)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.bottom_button)
        layout.addStretch()
        return layout

    def init_label(self, font):
        self.label = QLabel("請點選按鈕")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return self.label

    def handle_button_click(self, index):
        match index:
            case 0:
                self.open_edit_window()
            case 1:
                self.edit_timer()
            case 2:
                self.save_file()
            case 3:
                self.delete_timer()
            case 4:
                self.reset_timer()
            case 5:
                self.import_config()

    def open_edit_window(self):
        edit_window = EditWindow(parent=self)
        if edit_window.exec() == QDialog.DialogCode.Accepted:
            print(TimerConfig.is_valid)
            self.refresh_timer_list()

    def edit_timer(self):
        selected_items = self.timer_list.selectedItems()
        if not selected_items:
            print("請先選擇要編輯的計時器")
            return
        else:
            raw = selected_items[0].data(Qt.ItemDataRole.UserRole)

        edit_window = EditWindow(parent=self)
        edit_window.load_raw_input(raw)

        if edit_window.show() == QDialog.accepted:
            self.refresh_timer_list()  # 🔄 UI 更新即可

    def save_file(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "儲存設定檔", "timers.json", "JSON Files (*.json)")
        if filepath:
            data_manager.save_to_file(filepath)
            print(f"已儲存到 {filepath}")

    def delete_timer(self):
        selected_items = self.timer_list.selectedItems()
        if not selected_items:
            print("請先選擇要刪除的計時器")
            return

        item = selected_items[0]
        raw = item.data(Qt.ItemDataRole.UserRole)

        # 從 data_manager 移除該計時器
        data_manager.remove_raw_input(raw)

        # 更新列表
        self.refresh_timer_list()

    def reset_timer(self):
            print("重置計時器")

    def import_config(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "匯入設定檔", "", "JSON Files (*.json)")
        if filepath:
            data_manager.load_from_file(filepath)
            self.refresh_timer_list()
            print(f"已匯入設定檔：{filepath}")

    def handle_timer(self):
        current_text = self.bottom_button.text()
        if current_text == "啟動計時器":
            self.bottom_button.setText("停止計時器")
            self.label.setText("計時器啟動中")

            # 🔄 清空舊視窗（避免重複）
            for win in self.timer_windows:
                win.close()
            self.timer_windows.clear()

            # ✅ 啟動鍵盤監聽
            self.hotkey_listener.start()
            config_data = data_manager.get_all_config_inputs()

            for config in config_data:
                print(config)
                win = TimerWindow(
                    name=config.event_name,
                    cooldown_seconds=config.duration,
                    timer_manager=self.timer_manager,
                    state=KeyState.IDLE
                )
                win.set_state(KeyState.IDLE)  # ✅ 顯示初始狀態但不啟動
                win.show()
                self.timer_windows.append(win)

        else:
            self.bottom_button.setText("啟動計時器")
            self.label.setText("計時器已停止")

            # ✅ 停止鍵盤監聽
            self.hotkey_listener.stop()

            # 🛑 關閉所有視窗
            for win in self.timer_windows:
                win.close()
            self.timer_windows.clear()

    def on_timer_updated(self, raw: dict):
        self.refresh_timer_list()

    def refresh_timer_list(self):
        self.timer_list.clear()
        config_list = data_manager.get_all_config_inputs()
        print(f'這是更新資料：{config_list}')
        for config in config_list:
            print(config)
            text = (
                f'{config.event_name} - {config.duration}(限時：{config.limit_time}) | '
                f'🔴主鍵位：{config.select} -> {config.lock} -> {config.active} | '
                f'🟡副鍵位：{config.sub_active1} -> {config.sub_active2} -> {config.sub_active3} | '
            )

            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, config)
            self.timer_list.addItem(item)



# if __name__ == "__main__":
#
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

