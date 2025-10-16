# core/manager/edit_window_manager.py
from pynput import keyboard


class EditWindowManager:
    def __init__(self):
        self.recording_index = None
        self.listener = None
        self.on_start_callback = None
        self.on_stop_callback = None

    def on_recording(self, index: int):
        self.recording_index = index

        if self.listener:
            self.listener.stop()
            if self.on_stop_callback:
                self.on_stop_callback(index)

        self.listener = keyboard.Listener(on_press=self.on_key_detected)
        self.listener.start()

        if self.on_start_callback:
            self.on_start_callback(index)

    def on_key_detected(self, key):
        # 處理鍵盤輸入邏輯
        pass