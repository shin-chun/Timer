test_tuple = ('a', 'b', 'c' ,'d')
A, B, C, D = test_tuple
print(A, B, C, D)


# from enum import Enum
# from dataclasses import dataclass
# from typing import Dict
#
#
# # 定義 KeyState 枚舉
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


