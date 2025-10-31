from typing import List

from PySide6.QtCore import Signal, QObject
from core.manager.data_manager import data_manager
from core.model.timer_factory import KeyState, TimerConfig

class TimerManager(QObject):
    tick = Signal(str)
    key_state = Signal(str, KeyState)
    reset_all = Signal()
    reset_background = Signal(str)

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
                self.check_only_active(key, config)
            elif key == config.select:
                self.check_select_key(config)
            elif key == config.lock and self.state == KeyState.SELECT:
                self.check_lock_key(config)
            elif self.state == KeyState.LOCK:
                self.check_active_key(key, config)

    def check_only_active(self, key, config: TimerConfig):
        if key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3:
            self.tick.emit(str(config.uuid))
            self.key_state.emit(str(config.uuid), KeyState.ACTIVE)

    def check_select_key(self, config: TimerConfig):
        self.state = KeyState.SELECT
        self.key_state.emit(str(config.uuid), KeyState.SELECT)

    def check_lock_key(self, config: TimerConfig):
        self.id.append(config.uuid)
        self.state = KeyState.LOCK
        self.key_state.emit(str(config.uuid), KeyState.LOCK)

    def check_active_key(self, key, config: TimerConfig):
        if key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3:
            if self.id[0] == config.uuid:
                self.state = KeyState.IDLE
                self.id.clear()
                self.tick.emit(str(config.uuid))
                self.key_state.emit(str(config.uuid), KeyState.ACTIVE)
                self.reset_background.emit(str(config.uuid))

    def reset_all_cooldowns(self):
        self.reset_all.emit()

