from enum import Enum
from dataclasses import dataclass
from tkinter import messagebox
from typing import Dict, Optional
import tkinter as tk
from model.timer_factory import TimerConfig

@dataclass
class KeyMap:
    select: Optional[str] = None
    lock: Optional[str] = None
    active: Optional[str] = None
    sub_active1: Optional[str] = None
    sub_active2: Optional[str] = None
    sub_active3: Optional[str] = None

@dataclass
class TimerConfig:
    event_name : str
    limit_time : int
    duration : int
    keymap : KeyMap

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
        if self.keymap is None:
            messagebox.showerror("錯誤", "請設定有效的按鍵狀態")
            return False
        return True




keymap = KeyMap('a', 'b', 'c', 'd', 'e', 'f')
a = TimerConfig('測試', -1, 0, keymap=keymap)
a.is_valid()

print(a)
print(a.keymap, type(a.keymap))
print(a.keymap.select, type(a.keymap.select))
print(a.keymap.lock)
print(keymap.select)


# 定義 KeyState 枚舉
# class KeyState(Enum):
#     IDLE = 0
#     SELECT = 1
#     LOCK = 2
#     ACTIVE = 3
#
#
# # 定義 KeyGroup 資料類別
# @dataclass
# class KeyGroup:
#     select_key: str
#     members: Dict[KeyState, str]
#
#     def group_to_dict(self):
#         return {
#             'select_key': self.select_key,
#             'members': {state.name: key for state, key in self.members.items()}
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
# # 建立測試資料
# group = KeyGroup(
#     select_key="A",
#     members={
#         KeyState.IDLE: "",
#         KeyState.SELECT: "A",
#         KeyState.LOCK: "B",
#         KeyState.ACTIVE: "C"
#     }
# )
#
# # 呼叫 group_to_dict 並印出結果與類型
# result = group.group_to_dict()
# print("輸出資料：", result)
# print("資料類型：", type(result))
# print("members 類型：", type(result["members"]))
# print("members 中的 key 類型：", [type(k) for k in result["members"].keys()])
# print("members 中的 value 類型：", [type(v) for v in result["members"].values()])


