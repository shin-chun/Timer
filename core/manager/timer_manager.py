from typing import List

from PySide6.QtCore import Signal, QObject
from core.manager.data_manager import data_manager
from core.model.timer_factory import KeyState, TimerConfig

class TimerManager(QObject):
    tick = Signal(str)
    key_state = Signal(str, KeyState)
    reset_all = Signal()

    def __init__(self, state: KeyState=KeyState.IDLE):
        super().__init__()
        data_manager.subscribe(self.get_data)
        self.config_data_list = []
        self.state = state
        self.id = []

    def get_data(self, config_list: List[TimerConfig]):
        self.config_data_list = config_list
        print(f'這是資料中心傳到計時器管理器：{self.config_data_list}')

    def match_sequence(self, key):
        for config in self.config_data_list:
            if config.select == 'None' and config.lock == 'None':
                if key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3:
                    self.state = KeyState.ACTIVE
                    self.tick.emit(str(config.uuid))
                    self.key_state.emit(str(config.uuid), self.state)
            elif key == config.select:
                if self.id:
                    self.id.clear()
                    self.state = KeyState.SELECT
                    self.key_state.emit(str(config.uuid), self.state)
                else:
                    self.state = KeyState.SELECT
                    self.key_state.emit(str(config.uuid), self.state)
            elif key == config.lock and self.state == KeyState.SELECT:
                self.id.append(config.uuid)
                self.state = KeyState.LOCK
                self.key_state.emit(str(config.uuid), self.state)
            elif key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3 and self.state == KeyState.LOCK:
                for _ in self.id:
                    if self.id[0] == config.uuid:
                        self.state = KeyState.ACTIVE
                        self.tick.emit(str(config.uuid))
                        self.key_state.emit(str(config.uuid), self.state)
                        self.id.clear()
                        print(config)
                    else:
                        self.state = KeyState.IDLE
                        self.key_state.emit(str(config.uuid), self.state)

    def reset_all_cooldowns(self):
        self.reset_all.emit()

# class TimerManager(QObject):
#     tick = Signal(TimerConfig)
#
#     def __init__(self):
#         super().__init__()
#         self._group_cache = {}
#         self.state = KeyState.IDLE
#         self._key_state: Dict[str, KeyState] = {}  # 每個 select_key 的目前狀態
#         print(f"[DEBUG] TimerManager initialized: {id(self)}")
#
#
#     def input_key(self, key: str):
#         print(f"🧠 TimerManager 收到鍵：{key}")
#         self.handle_key_press(key)
#
#     def handle_key_press(self, key: str):
#         for config in self.get_data():
#             keymap = config.keymap
#             for group_id, group in keymap.groups.items():
#                 if key == group.select_key:
#                     self._key_state[group_id] = KeyState.SELECT
#                     print(f"[{group_id}] 已選擇")
#                 elif key == group.members.get(KeyState.LOCK):
#                     if self._key_state.get(group_id) == KeyState.SELECT:
#                         self._key_state[group_id] = KeyState.LOCK
#                         print(f"[{group_id}] 已鎖定")
#                 elif key == group.members.get(KeyState.ACTIVE):
#                     current = self._key_state.get(group_id, KeyState.IDLE)
#                     if KeyState.LOCK in group.members:
#                         if current == KeyState.LOCK:
#                             self._start_timer(config)
#                     elif group.select_key:
#                         if current == KeyState.SELECT:
#                             self._start_timer(config)
#                     else:
#                         self._start_timer(config)
#
#
#     def _start_timer(self, config: TimerConfig):
#         self.state = KeyState.IDLE
#         self.tick.emit(config)
#
#     def inject_receiver(self, receiver_callable):
#         self.tick.connect(receiver_callable)
#
#     def on_tick(self):
#         print('tick:已接到')
#
#     def reset_states(self):
#         self._key_state.clear()
#         self.state = KeyState.IDLE
#
#     def load_configs(self):
#         self._configs = self.get_data()
#
#     def get_data(self) -> list[TimerConfig]:
#         raw_configs = data_manager.get_all_raw_inputs()
#         result = []
#         for raw in raw_configs:
#             keymap = KeyMapBuilder.from_key_labels(raw["key_labels"])
#             config = TimerConfig(
#                 event_name=raw["event_name"],
#                 duration=raw["duration"],
#                 limit_time=raw["limit_time"],
#                 keymap=keymap
#             )
#             result.append(config)
#         return result
#
#     def start_tick(self):
#         if self.state.name.startswith("ACTIVE") or self.state == KeyState.ACTIVE:
#             self.tick.emit()
#
#     def stop_tick(self):
#         self.state = KeyState.IDLE
#         print("計時器已停止")


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

