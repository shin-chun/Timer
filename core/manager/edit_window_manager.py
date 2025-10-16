from typing import Callable, Optional, Dict
from pynput import keyboard

from core.manager.data_manager import data_manager
from model.timer_factory import TimerConfig, KeyState, KeyMap, KeyGroup


class EditWindowManager:
    """
    管理 EditWindow 的鍵位錄製流程，包括：
    - 啟動與停止鍵盤監聽器
    - 記錄目前正在錄製的鍵位索引
    - 將錄製結果回傳給 UI（透過 callback）
    """

    def __init__(self, update_callback: Callable[[int, str], None]):
        """
        初始化管理器

        :param update_callback: 當鍵位錄製完成時，呼叫此函式並傳入 (index, key_name)
        """
        self.recording_index: Optional[int] = None
        self.listener: Optional[keyboard.Listener] = None
        self.recording_index = None
        self.update_callback = update_callback

    def on_recording(self, index: int):
        """
        啟動鍵位錄製流程，並設定目前錄製的索引

        :param index: 鍵位區的索引（0~5）
        """
        self.recording_index = index
        self.stop_listener()
        self.listener = keyboard.Listener(on_press=self._on_key_detected)
        self.listener.start()

    def stop_listener(self):
        """
        停止鍵盤監聽器（若存在）
        """
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _on_key_detected(self, key):
        """
        鍵盤事件觸發時呼叫，解析鍵名並回傳給 UI

        :param key: pynput 傳入的鍵盤事件物件
        """
        try:
            key_name = key.char if hasattr(key, 'char') and key.char else str(key)
        except Exception:
            key_name = str(key)

        if self.recording_index is not None:
            self.update_callback(key_name)
            self.recording_index = None

        self.stop_listener()
