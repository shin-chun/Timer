from typing import List, Dict

from PySide6.QtCore import Signal, QObject

from core.manager.data_manager import data_manager
from core.model.timer_factory import KeyState, TimerConfig


class TimerManager(QObject):
    tick = Signal()

    def __init__(self):
        super().__init__()
        self._group_cache = {}
        self.state = KeyState.IDLE
        self._key_state: Dict[str, KeyState] = {}  # 每個 select_key 的目前狀態

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
        self.state = KeyState.ACTIVE
        print(f"✅ 啟動計時器：{config.event_name}")
        self.tick.emit()

    def reset_states(self):
        self._key_state.clear()
        self.state = KeyState.IDLE

    def load_configs(self):
        self._configs = self.get_data()

    def get_data(self) -> List[TimerConfig]:
        raw_inputs = data_manager.get_all_raw_inputs()
        print(f'get_data:{raw_inputs}')
        configs = [
            TimerConfig.config_from_dict(raw)
            for raw in raw_inputs
            if isinstance(raw, dict)
        ]
        return configs

    def start_tick(self):
        if self.state.name.startswith("ACTIVE") or self.state == KeyState.ACTIVE:
            self.tick.emit()

    def stop_tick(self):
        self.state = KeyState.IDLE
        print("計時器已停止")
