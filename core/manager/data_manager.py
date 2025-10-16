# manager/data_manager.py
from typing import Callable, List, Dict, Optional
from model.timer_factory import TimerConfig


class DataManager:
    def __init__(self):
        self._timers = []
        self._subscribers: list[Callable[[TimerConfig], None]] = []

    def save_timer(self, config: TimerConfig):
        self._timers.append(config)
        print(f'資料已儲存為：{self._timers}')
        self._notify_subscribers(config)

    def get_all_timers(self):
        return self._timers

    def subscribe(self, callback: Callable[[TimerConfig], None]):
        self._subscribers.append(callback)

    def _notify_subscribers(self, timer_data: TimerConfig):
        for callback in self._subscribers:
            callback(timer_data)


# 單例模式（可選）
data_manager = DataManager()