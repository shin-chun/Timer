from typing import List, Dict

from PySide6.QtCore import Signal, QObject, QTimer

from core.manager.data_manager import data_manager, DataManager
from core.model.timer_factory import KeyState, TimerConfig, KeyMap, KeyGroup, KeyMapBuilder


class TimerManager(QObject):
    tick = Signal(TimerConfig)

    def __init__(self):
        super().__init__()
        self._group_cache = {}
        self.state = KeyState.IDLE
        self._key_state: Dict[str, KeyState] = {}  # 每個 select_key 的目前狀態
        print(f"[DEBUG] TimerManager initialized: {id(self)}")


    def input_key(self, key_name: str):
        print(f"🧠 TimerManager 收到鍵：{key_name}")
        self.handle_key_press(key_name)

    def handle_key_press(self, key: str):
        for config in self.get_data():
            keymap = config.keymap
            for group_id, group in keymap.groups.items():
                if key == group.select_key:
                    self._key_state[group_id] = KeyState.SELECT
                    print(f"[{group_id}] 已選擇")
                elif key == group.members.get(KeyState.LOCK):
                    if self._key_state.get(group_id) == KeyState.SELECT:
                        self._key_state[group_id] = KeyState.LOCK
                        print(f"[{group_id}] 已鎖定")
                elif key == group.members.get(KeyState.ACTIVE):
                    current = self._key_state.get(group_id, KeyState.IDLE)
                    if KeyState.LOCK in group.members:
                        if current == KeyState.LOCK:
                            self._start_timer(config)
                    elif group.select_key:
                        if current == KeyState.SELECT:
                            self._start_timer(config)
                    else:
                        self._start_timer(config)

    def _start_timer(self, config: TimerConfig):
        self.state = KeyState.IDLE
        self.tick.emit(config)

    def inject_receiver(self, receiver_callable):
        self.tick.connect(receiver_callable)

    def on_tick(self):
        print('tick:已接到')

    def reset_states(self):
        self._key_state.clear()
        self.state = KeyState.IDLE

    def load_configs(self):
        self._configs = self.get_data()

    def get_data(self) -> list[TimerConfig]:
        raw_configs = data_manager.get_all_raw_inputs()
        result = []
        for raw in raw_configs:
            keymap = KeyMapBuilder.from_key_labels(raw["key_labels"])
            config = TimerConfig(
                event_name=raw["event_name"],
                duration=raw["duration"],
                limit_time=raw["limit_time"],
                keymap=keymap
            )
            result.append(config)
        return result

    def start_tick(self):
        if self.state.name.startswith("ACTIVE") or self.state == KeyState.ACTIVE:
            self.tick.emit()

    def stop_tick(self):
        self.state = KeyState.IDLE
        print("計時器已停止")


# def test_timer_activation():
#     # 模擬原始資料
#     data_manager._raw_inputs = [
#         {
#             "event_name": "影子",
#             "duration": 60,
#             "limit_time": 3,
#             "key_labels": [
#                 "Key.shift_r", "Key.left", "Key.ctrl_l",  # group_0
#                 "Key.alt_l", "None", "Key.backspace"      # group_1
#             ]
#         }
#     ]
#
#     # 建立 TimerManager 並連接 tick 訊號
#     tm = TimerManager()
#     tm.tick.connect(lambda: print("🕒 tick 被觸發"))
#     tm.load_configs()
#
#     # 模擬鍵盤輸入流程
#     tm.input_key("Key.shift_r")    # SELECT group_0
#     tm.input_key("Key.left")
#     tm.input_key("Key.ctrl_l")# LOCK group_0
#     tm.input_key("Key.shift_r")      # ACTIVE group_0 → 應該啟動計時器
#     tm.input_key("Key.ctrl_l")
#     tm.input_key("c")
#     tm.input_key("Key.left")
#     tm.input_key("Key.ctrl_l")
#
#     # 驗證狀態
#     assert tm.state == KeyState.ACTIVE
#     print("✅ 測試完成：計時器已啟動")
#
# test_timer_activation()

