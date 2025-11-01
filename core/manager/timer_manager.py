from collections import deque
from typing import List

from PySide6.QtCore import Signal, QObject
from core.manager.data_manager import data_manager
from core.model.timer_factory import KeyState, TimerConfig

class TimerManager(QObject):
    tick = Signal(str, KeyState)
    reset_background = Signal(str)
    reset_all = Signal()

    def __init__(self):
        super().__init__()
        data_manager.subscribe(self.get_data)
        self.config_data_list = []
        self.state = KeyState.IDLE
        self.select_set = set()
        self.select_count = 0
        self.id = []
        print(f'初始化ID：{id(self.state)}')

    def get_data(self, config_list: List[TimerConfig]):
        self.config_data_list = config_list
        print(f'這是資料中心傳到計時器管理器：{self.config_data_list}')
        print(len(self.config_data_list))

    def match_sequence(self, key):
        index = 0
        for config in self.config_data_list:
            if config.select == 'None' and config.lock == 'None':
                self.check_only_active(key, config)
            elif key == config.select:
                self.check_select_key(config)
                self.select_set.add(config.uuid)
                print(f'這裡要IDLE->{config.event_name} : {self.state}, {id(self.state)}')
            elif key != config.lock and self.state == KeyState.SELECT:
                index += 1
                if index == len(self.select_set):
                    self.reset_background.emit('clear')
                    self.state = KeyState.IDLE
                    self.select_set.clear()
                    print(f'這裡要IDLE->{config.event_name} : {self.state}, {id(self.state)}')
            elif key == config.lock and self.state == KeyState.SELECT:
                self.check_lock_key(config)
                self.select_set.clear()
                print(f'{config.event_name} : {self.state}, {id(self.state)}')
            elif self.state == KeyState.LOCK:
                self.check_active_key(key, config)
                self.select_set.clear()
                print(f'{config.event_name} : {self.state}, {id(self.state)}')


    def check_only_active(self, key, config: TimerConfig):
        if key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3:
            self.tick.emit(str(config.uuid), KeyState.ACTIVE)

    def check_select_key(self, config: TimerConfig):
        self.state = KeyState.SELECT
        self.tick.emit(str(config.uuid), KeyState.SELECT)
        if self.id:
            self.id.clear()

    def check_lock_key(self, config: TimerConfig):
        self.id.append(config.uuid)
        self.state = KeyState.LOCK
        self.tick.emit(str(config.uuid), KeyState.LOCK)
        for i in self.config_data_list:
            if i.uuid != config.uuid:
                print(f'這是沒選中的：{i.uuid}')
                self.reset_background.emit(str(i.uuid))

    def check_active_key(self, key, config: TimerConfig):
        if key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3:
            if self.id[0] == config.uuid:
                self.state = KeyState.IDLE
                self.id.clear()
                self.tick.emit(str(config.uuid), KeyState.ACTIVE)

    def reset_all_cooldowns(self):
        self.reset_all.emit()

