import json
from typing import Callable, List, Dict, Optional

from core.model.timer_factory import TimerConfig


class DataManager:
    def __init__(self):
        self.config_list: List[TimerConfig] = []
        self._subscribers: List[Callable[[TimerConfig], None]] = []

    def save_config_input(self, config_raw):
        self.config_list.append(config_raw)
        print(f'設置資料儲存為：{config_raw}')

    def remove_config_input(self, config_raw):
        self.config_list = [raw_data for raw_data in self.config_list if raw_data != config_raw]
        self._notify_subscribers(config_raw)
        print(f'資料已刪除{config_raw}')
        print(self.config_list)

    def update_config(self, old: TimerConfig, new: TimerConfig):
        try:
            index = self.config_list.index(old)
            self.config_list[index] = new
            self._notify_subscribers(new)
        except ValueError:
            print("找不到要更新的計時器")

    def get_all_config_inputs(self) -> List[TimerConfig]:
        return self.config_list

    def subscribe(self, callback: Callable[[TimerConfig], None]):
        self._subscribers.append(callback)

    def _notify_subscribers(self, config_raw):
        for callback in self._subscribers:
            callback(config_raw)

    def save_to_file(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config_list, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            config_list = json.load(f)
        self.config_list.clear()
        for config in config_list:
            self.config_list.append(config)
            self._notify_subscribers(config)
        print(f'原始資料已匯入：{self.config_list}')

# 單例模式（可選）

data_manager = DataManager()