# manager/timer_factory.py
import uuid

from dataclasses import dataclass, field
from tkinter import messagebox
from typing import Optional, Dict
from enum import Enum

class KeyState(Enum):
    IDLE = 0
    SELECT = 1
    LOCK = 2
    ACTIVE = 3


@dataclass
class TimerConfig:
    event_name : str
    limit_time : int
    duration : int
    select: Optional[str] = None
    lock: Optional[str] = None
    active: Optional[str] = None
    sub_active1: Optional[str] = None
    sub_active2: Optional[str] = None
    sub_active3: Optional[str] = None
    uuid: 'uuid.UUID' = field(default_factory=uuid.uuid4)

    def is_valid(self) -> bool:
        if not self.event_name or not self.event_name.strip():
            messagebox.showerror("錯誤", "事件名稱不能為空")
            return False
        if self.duration <= 0:
            messagebox.showerror("錯誤", "持續時間必須大於 0")
            return False
        if self.limit_time < 0:
            messagebox.showerror("錯誤", "限制時間不能為負值")
            return False
        return True

    def config_to_dict(self, raw_confing_list) -> dict:
        config_dict = {}
        for raw in raw_confing_list:
            raw.event_name = self.event_name
            raw.duration = self.duration
            raw.select = self.select
            raw.lock = self.lock
            raw.active = self.active
            raw.sub_active1 = self.sub_active1
            raw.sub_active2 = self.sub_active2
            raw.sub_active3 = self.sub_active3
        return config_dict





STATE_COLOR_MAP= {
    'select' : 'yellow',
    'lock' : 'red',
    'active' : 'gray',
    'sub_active1' : 'gray',
    'sub_active2' : 'gray',
    'sub_active3' : 'gray',
    'default' : 'white'
}

# class KeyState(Enum):
#     IDLE = 0
#     SELECT = 1
#     LOCK = 2
#     ACTIVE = 3
#
# STATE_COLOR_MAP = {
#     KeyState.IDLE: "white",
#     KeyState.SELECT: "yellow",
#     KeyState.LOCK: "red",
#     KeyState.ACTIVE: "gray",
# }
#
# @dataclass
# class KeyGroup:
#     select_key: str
#     members: Dict[KeyState, str]  # 包含 LOCK, ACTIVE 等
#
#     def group_to_dict(self) -> dict:
#         return {
#             "select_key": self.select_key,
#             "members": {state.name: key for state, key in self.members.items()}
#         }
#
#     @classmethod
#     def group_from_dict(cls, data: dict) -> "KeyGroup":
#         members_raw = data.get("members", {})
#         members = {
#             KeyState[k]: v for k, v in members_raw.items()
#             if k in KeyState.__members__ and v
#         }
#
#         return cls(
#             select_key=data.get("select_key", ""),
#             members=members
#         )
#
#
# @dataclass
# class KeyMap:
#     groups: Dict[str, KeyGroup] = field(default_factory=dict)
#
#     def get_group_by_select(self, select_key: str) -> Optional[KeyGroup]:
#         return self.groups.get(select_key)
#
#     def get_lock_in_group(self, select_key: str) -> Optional[str]:
#         group = self.get_group_by_select(select_key)
#         if group:
#             return group.members.get(KeyState.LOCK)
#
#     def get(self, state: KeyState) -> Optional[str]:
#         # 提供單鍵查詢（非群組）
#         for group in self.groups.values():
#             if state in group.members:
#                 return group.members[state]
#         return None
#
#     def map_to_dict(self) -> dict:
#         return {
#             group_id: group.group_to_dict()
#             for group_id, group in self.groups.items()
#         }
#
#     @classmethod
#     def map_from_dict(cls, data: dict) -> "KeyMap":
#         groups = {
#             group_id: KeyGroup.group_from_dict(group_data)
#             for group_id, group_data in data.items()
#         }
#         return cls(groups=groups)
#
# @dataclass
# class TimerConfig:
#     event_name: str
#     limit_time: int
#     duration: int
#     keymap: KeyMap
#
#     def is_valid(self) -> bool:
#         """檢查是否為有效的 Timer 設定"""
#         return (
#             bool(self.event_name.strip()) and
#             self.duration > 0 and
#             self.limit_time >= 0
#             # self.keymap.get(KeyState.IDLE) is not None
#         )
#
#     def config_to_dict(self) -> dict:
#         """轉換為可序列化的 dict 結構"""
#         return {
#             "event_name": self.event_name,
#             "limit_time": self.limit_time,
#             "duration": self.duration,
#             "keymap": self.keymap.map_to_dict()
#         }
#
#     @classmethod
#     def config_from_dict(cls, data: dict) -> "TimerConfig":
#         keymap_data = data.get("keymap", {})
#         group_data = keymap_data.get("groups", {})  # ✅ 修正這裡
#         keymap = KeyMap.map_from_dict(group_data)
#         return cls(
#             event_name=data.get("event_name", ""),
#             limit_time=data.get("limit_time", 0),
#             duration=data.get("duration", 0),
#             keymap=keymap
#         )
#
# class KeyMapBuilder:
#     @staticmethod
#     def from_key_labels(key_labels: list[str], group_size: int = 3) -> KeyMap:
#         groups = {}
#         for i in range(0, len(key_labels), group_size):
#             group_labels = key_labels[i:i+group_size]
#             clean_labels = [k for k in group_labels if k != "None"]
#             if not clean_labels:
#                 continue
#
#             select_key = clean_labels[0]
#             members = {}
#
#             if len(clean_labels) > 1:
#                 members[KeyState.LOCK] = clean_labels[1]
#             if len(clean_labels) > 2:
#                 members[KeyState.ACTIVE] = clean_labels[2]
#
#             group = KeyGroup(select_key=select_key, members=members)
#             groups[f"group_{i // group_size}"] = group
#
#         return KeyMap(groups=groups)