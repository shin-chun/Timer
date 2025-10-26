from dataclasses import dataclass, field
from enum import Enum
from tkinter import messagebox
from typing import Optional
import uuid

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


config_list = [
    TimerConfig(
            event_name='影子',
            limit_time= 3,
            duration=60,
            select='Key.shift_r',
            lock='Key.left',
            active='Key.ctrl_l',
            sub_active1='Key.alt_l',
            sub_active2='None',
            sub_active3='None'
    ),
    TimerConfig(
        event_name='餘暉',
        limit_time= 3,
        duration=25,
        select='Key.shift_r',
        lock='Key.up',
        active='Key.ctrl_l',
        sub_active1='Key.alt_l',
        sub_active2='None',
        sub_active3='None',
    ),
    TimerConfig(
        event_name='百鬼',
        limit_time=3,
        duration=10,
        select='Key.shift_r',
        lock='Key.down',
        active='w',
        sub_active1='e',
        sub_active2='f',
        sub_active3='c'
    ),
    TimerConfig(
        event_name='覺醒',
        limit_time=3,
        duration=25,
        select='None',
        lock='None',
        active='w',
        sub_active1='e',
        sub_active2='f',
        sub_active3='c'
    )
]

a = []
def match_sequence(key):
    for config in config_list:
        if key == config.select:
            if a is not None:
                a.clear()
        elif key == config.lock:
            a.append(config.uuid)
        elif key == config.active:
            for _ in a:
                if a[0] == config.uuid:
                    a.clear()
                    print(config)
                    print(f'影子的uuid:{config.uuid}')
        elif config.select and config.lock == 'None':
            if key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3:
                print(config)
                print(f'覺醒的uuid:{config.uuid}')


key_input = ['Key.shift_r', 'Key.down', 'Key.shift_r', 'Key.left', 'c', 'Key.ctrl_l', 'w']
for k in key_input:
    match_sequence(k)

print(config_list[0].uuid)
print(config_list[3].uuid)
print(a)

# for i, c in enumerate(config):
#     print(f"[{i}] TimerConfig id: {id(c)}")
#     for k, v in c.__dict__.items():
#         print(f"{k}: {v}")


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


