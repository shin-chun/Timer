from PySide6.QtWidgets import QLineEdit, QSpinBox
from pynput import keyboard
from core.manager.data_manager import data_manager
from core.manager.key_map import KeyMap, KeyState
from timer_config import TimerConfig


class EditWindowManager:
    def __init__(self):
        self.index = 0
        self.recording_index = None
        self.listener = None
        self.key_labels = []


    def start_recording(self, index):
        # 設定錄製狀態
        self.recording_index = index
        self.key_labels[index].setText("錄製中...")

        # 若已有監聽器，先停止
        if self.listener:
            self.listener.stop()
            for i in range(len(self.key_labels)):
                if i != index and self.key_labels[i].text() == '錄製中...':
                    self.key_labels[i].setText("None")

        # 啟動新的監聽器
        self.listener = keyboard.Listener(on_press=self.on_key_detected)
        self.listener.start()

    def on_key_detected(self, key):
        try:
            key_name = key.char if hasattr(key, 'char') else str(key)
        except Exception:
            key_name = str(key)

        # 更新 Label 顯示
        if self.recording_index is not None:
            self.key_labels[self.recording_index].setText(key_name)
            self.recording_index = None

        # 停止監聽
        if self.listener:
            self.listener.stop()
            self.listener = None

    def remove(self, index):
        self.recording_index = index
        print("recording_index=", self.recording_index)
        self.key_labels[index].setText("None")
        print("key_label=", self.key_labels[index].text())

    def on_confirm(self):
        config = TimerConfig(
            event_name=self.event_name_input.text(),
            limit_time=self.limit_time_input.value(),
            duration=self.duration_input.value(),
            keymap=self.collect_keymap()
        )
        data_manager.save_timer(config)
        self.accept()

    def collect_keymap(self) -> KeyMap:
        role_map = {
            0: KeyState.SELECT,
            1: KeyState.LOCK,
            2: KeyState.ACTIVE,
            3: KeyState.SELECT2,
            4: KeyState.LOCK2,
            5: KeyState.ACTIVE2
        }

        keys = {}
        for i, label in enumerate(self.key_labels):
            key = label.text()
            if key != "None":
                keys[role_map[i]] = key
        return KeyMap(keys=keys)