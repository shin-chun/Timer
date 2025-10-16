# manager/data_manager.py
import json
from typing import Callable, List, Dict, Optional
from model.timer_factory import TimerConfig
# class DataManager:
#     def __init__(self):
#         self._subscribers = {
#             "load_config": []
#         }
#
#     def subscribe(self, event_type: str, callback):
#         self._subscribers[event_type].append(callback)
#
#     def notify(self, event_type: str, payload=None):
#         for callback in self._subscribers.get(event_type, []):
#             callback(payload)
#
#     def request_config_load(self, config: TimerConfig):
#         self.notify("load_config", config)

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

    def save_to_file(self, filepath: str):
        data = [config.to_dict() for config in self._timers]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        self._timers.clear()
        for item in raw_data:
            config = TimerConfig.from_dict(item)
            self._timers.append(config)
            self._notify_subscribers(config)
        print(f'資料已匯入為：{self._timers}')


# 單例模式（可選）
data_manager = DataManager()