import json
from typing import Callable, List, Dict, Optional

class DataManager:
    def __init__(self):
        self._raw_inputs: List[Dict] = []
        self._subscribers: List[Callable[[Dict], None]] = []

    def save_raw_input(self, raw: Dict):
        self._raw_inputs.append(raw)
        print(f'原始資料已儲存：{self._raw_inputs}')
        self._notify_subscribers(raw)

    def remove_raw_input(self, raw: Dict):
        self._raw_inputs = [r for r in self._raw_inputs if r != raw]
        self._notify_subscribers(raw)
        print(f'資料已刪除{self._raw_inputs}')

    def update_raw(self, old: dict, new: dict):
        try:
            index = self._raw_inputs.index(old)
            self._raw_inputs[index] = new
            self._notify_subscribers(new)
        except ValueError:
            print("找不到要更新的計時器")

    def get_all_raw_inputs(self) -> List[Dict]:
        return self._raw_inputs

    def subscribe(self, callback: Callable[[Dict], None]):
        self._subscribers.append(callback)

    def _notify_subscribers(self, raw: Dict):
        for callback in self._subscribers:
            callback(raw)

    def save_to_file(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._raw_inputs, f, ensure_ascii=False, indent=4)

    def load_from_file(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        self._raw_inputs.clear()
        for item in raw_data:
            self._raw_inputs.append(item)
            self._notify_subscribers(item)
        print(f'原始資料已匯入：{self._raw_inputs}')


    def get_ui_snapshot(self, raw: Dict) -> Dict:
        return {
            "事件名稱": raw.get("event_name", ""),
            "持續時間": f'{raw.get("duration", 0)} 秒',
            "限制時間": f'{raw.get("limit_time", 0)} 秒',
            "鍵位配置": [
                {"索引": i, "鍵名": key}
                for i, key in enumerate(raw.get("key_labels", []))
                if key and key != "None"
            ]
        }

    def get_timer_add(self):
        pass

# 單例模式（可選）

data_manager = DataManager()