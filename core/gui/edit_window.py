import sys
from functools import partial
from typing import Dict, Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QSpinBox, QGroupBox, QFrame, QSizePolicy, QApplication
)
from core.manager.data_manager import data_manager
from core.manager.edit_window_manager import EditWindowManager
from model.timer_factory import KeyMap, KeyState, TimerConfig, KeyGroup


class EditWindow(QDialog):
    def __init__(self, title='編輯計時器', parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(700, 350)

        self.event_name_input = QLineEdit()
        self.limit_time_input = QSpinBox()
        self.duration_input = QSpinBox()
        self.key_labels = []

        self._setup_ui()
        self.recording_index = None
        self.edit_manager = EditWindowManager(self.update_key_label)


    def _setup_ui(self):
        main_layout = QVBoxLayout()

        # 事件名稱區塊
        event_font = QFont()
        event_font.setBold(True)
        event_font.setPointSize(14)

        self.event_name_input.setFont(event_font)
        self.event_name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.event_name_input.setPlaceholderText("請輸入事件名稱")
        self.event_name_input.setStyleSheet("border: 1px solid gray;")

        self.duration_input.setRange(1, 3600)
        self.duration_input.setValue(10)
        self.duration_input.setFixedHeight(40)

        self.limit_time_input.setValue(3)
        self.limit_time_input.setFixedHeight(40)

        all_layout = QVBoxLayout()
        all_layout.addWidget(self.event_name_input)
        all_layout.addWidget(QLabel("限制完成時間"))
        all_layout.addWidget(self.limit_time_input)
        all_layout.addWidget(QLabel("持續秒數"))
        all_layout.addWidget(self.duration_input)

        event_frame = QFrame()
        event_frame.setLayout(all_layout)
        event_frame.setFrameShape(QFrame.Shape.Box)
        event_frame.setFixedWidth(200)
        event_frame.setStyleSheet("QFrame { border: 2px solid #aaa; border-radius: 6px; padding: 6px; }")

        # 主鍵位區與副鍵位區
        main_keys = self._create_key_group("觸發主鍵", range(3))
        sub_keys = self._create_key_group("副鍵位區", range(3, 6))

        key_layout = QHBoxLayout()
        key_layout.addWidget(main_keys)
        key_layout.addWidget(sub_keys)

        top_layout = QHBoxLayout()
        top_layout.addWidget(event_frame)
        top_layout.addLayout(key_layout)

        # 按鈕區（無功能）
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        confirm_btn = QPushButton("確認")
        confirm_btn.setFixedSize(100, 50)
        confirm_btn.setStyleSheet(self._button_style())
        confirm_btn.clicked.connect(self._on_confirm)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(100, 50)
        cancel_btn.setStyleSheet(self._button_style())
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        main_layout.addLayout(top_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def _create_key_group(self, title, indices):
        record_btn_label = ['選擇鍵', '鎖定鍵', '觸發鍵', '子觸發1', '子觸發2', '子觸發3']
        group_box = QGroupBox(title)
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid gray;
                border-radius: 6px;
                margin-top: 10px;
                padding: 6px;
            }
        """)
        layout = QGridLayout()
        group_box.setLayout(layout)

        for i in indices:
            col = i % 3

            record_btn = QPushButton(record_btn_label[i])
            record_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            record_btn.clicked.connect(partial(self._start_recording, i))

            label = QLabel("None")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.key_labels.append(label)

            clear_btn = QPushButton("清除")
            clear_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            clear_btn.clicked.connect(partial(self.remove, i))

            layout.addWidget(record_btn, 0, col)
            layout.addWidget(label, 1, col)
            layout.addWidget(clear_btn, 2, col)

        return group_box

    def _button_style(self):
        return """
            QPushButton {
                background-color: #D0D0D0;
                color: black;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
        """
    def _start_recording(self, index):
        self.recording_index = index
        self.key_labels[index].setText('錄製中...')

        for i in range(len(self.key_labels)):
            if i != index and self.key_labels[i].text() == '錄製中...':
                self.key_labels[i].setText('None')

        self.edit_manager.on_recording(index)

    def update_key_label(self, key_name):
        # 更新 Label 顯示
        if self.recording_index is not None:
            self.key_labels[self.recording_index].setText(key_name)
            self.recording_index = None

    def remove(self, index):
        self.recording_index = index
        self.key_labels[index].setText("None")

    def _on_confirm(self):
        config = TimerConfig(
            event_name=self.event_name_input.text(),
            limit_time=self.limit_time_input.value(),
            duration=self.duration_input.value(),
            keymap=self._collect_keymap()
        )
        data_manager.save_timer(config)
        self.accept()

    def _collect_keymap(self) -> KeyMap:
        role_map = {
            0: KeyState.SELECT,
            1: KeyState.LOCK,
            2: KeyState.ACTIVE,
            3: KeyState.SUB_ACTIVE1,
            4: KeyState.SUB_ACTIVE2,
            5: KeyState.SUB_ACTIVE3
        }

        members: Dict[KeyState, str] = {}
        select_key: Optional[str] = None

        for i, label in enumerate(self.key_labels):
            key = label.text()
            if key and key != "None":
                state = role_map[i]
                members[state] = key
                if state == KeyState.SELECT:
                    select_key = key

        if not select_key:
            # 若沒有 SELECT，視為單鍵觸發，使用事件名稱作為 group_id
            group_id = self.event_name_input.text().strip() or "default"
            select_key = "__single__"
        else:
            group_id = select_key

        group = KeyGroup(select_key=select_key, members=members)
        return KeyMap(groups={group_id: group})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditWindow()
    window.show()
    sys.exit(app.exec())
