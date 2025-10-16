import sys

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel, QSizePolicy, QApplication, QDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from core.manager.data_manager import data_manager
from core.gui.edit_window import EditWindow
from model.timer_factory import KeyMap, KeyState, TimerConfig, KeyGroup


class MainWindow(QMainWindow):
    def __init__(self):
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
        self.refresh_timer_list()

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
        bottom_button = QPushButton("啟動計時器")
        bottom_button.setFont(font)
        bottom_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(bottom_button)
        layout.addStretch()
        return layout

    def init_label(self, font):
        label = QLabel("請點選按鈕")
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def handle_button_click(self, index):
        match index:
            case 0:
                self.create_timer()
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

    def create_timer(self):
        edit_window = EditWindow(parent=self)
        if edit_window.exec() == QDialog.accepted:
            self.refresh_timer_list()

    def edit_timer(self):
        print("編輯計時器")

    def save_file(self):
        print("儲存檔案")

    def delete_timer(self):
        print("刪除計時器")

    def reset_timer(self):
        print("重置計時器")

    def import_config(self):
        print("匯入設定檔")


    def on_timer_updated(self, config: TimerConfig):
        self.refresh_timer_list()

    def refresh_timer_list(self):
        self.timer_list.clear()

        for config in data_manager.get_all_timers():
            for group_id, group in config.keymap.groups.items():
                select_key = group.select_key or "未設定"
                lock_key = group.members.get(KeyState.LOCK, "未設定")
                active_key = group.members.get(KeyState.ACTIVE, "未設定")
                sub_active_key1 = group.members.get(KeyState.SUB_ACTIVE1, "未設定")
                sub_active_key2 = group.members.get(KeyState.SUB_ACTIVE2, "未設定")
                sub_active_key3 = group.members.get(KeyState.SUB_ACTIVE3, "未設定")

                text = (
                    f"{config.event_name} - {config.duration}s | "
                    f"🔴主鍵位：{select_key} -> {lock_key} -> {active_key} | "
                    f"🟡 副鍵位：{sub_active_key1} - {sub_active_key2} - {sub_active_key3}"
                )

                item = QListWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, config)
                self.timer_list.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

