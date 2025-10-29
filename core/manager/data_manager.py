import json
from typing import Callable, List, Dict, Optional

from core.model.timer_factory import TimerConfig


class DataManager:
    def __init__(self):
        self.config_list: List[TimerConfig] = []
        self._subscribers: List[Callable[[TimerConfig], None]] = []

    def save_config_input(self, config_data):
        self.config_list.append(config_data)
        self._notify_subscribers(self.config_list)
        print(f'設置資料儲存為：{self.config_list}')

    def remove_config_input(self, config_data):
        self.config_list = [data for data in self.config_list if data != config_data]
        print(f'資料已刪除{config_data}')
        print(self.config_list)
        self._notify_subscribers(self.config_list)

    def update_config(self, old: TimerConfig, new: TimerConfig):
        try:
            index = self.config_list.index(old)
            self.config_list[index] = new
            self._notify_subscribers(self.config_list)
        except ValueError:
            print("找不到要更新的計時器")

    def get_config_list(self) -> List[TimerConfig]:
        return self.config_list

    def subscribe(self, callback: Callable[[TimerConfig], None]):
        self._subscribers.append(callback)

    def _notify_subscribers(self, config_data):
        for callback in self._subscribers:
            callback(config_data)

    def save_to_file(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(
                [config.to_dict() for config in self.config_list],
                f,
                ensure_ascii=False,
                indent=4
            )

    def load_from_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_list = json.load(f)

        self.config_list.clear()
        for raw in raw_list:
            config = TimerConfig.from_dict(raw)
            self.config_list.append(config)

        self._notify_subscribers(self.config_list)

    # def load_from_file(self, filepath: str):
    #     with open(filepath, 'r', encoding='utf-8') as f:
    #         raw_list = json.load(f)
    #
    #     self.config_list.clear()
    #     for raw in raw_list:
    #         config = TimerConfig.from_dict(raw)
    #         self.config_list.append(config)
    #         self._notify_subscribers(config)
    #
    #     print(f'原始資料已匯入：{self.config_list}')

# 單例模式（可選）

data_manager = DataManager()