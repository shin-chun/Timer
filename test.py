from _thread import lock
from dataclasses import dataclass
from enum import Enum

import select

from core.manager.data_manager import data_manager


class KeyState(Enum):
    IDLE = 0
    SELECT = 1
    LOCK = 2
    ACTIVE = 3
    SUB_ACTIVE1 = 4
    SUB_ACTIVE2 = 5
    SUB_ACTIVE3 = 6


@dataclass
class KeyGroup:
    select : str
    lock : str
    active : str
    sub_active1 : str
    sub_active2 : str
    sub_active3 : str

    def group_to_dict(self):
        return {
            'select' : self.select,
            'lock' : self.lock,
            'active' : self.active,
            'sub_active1' : self.sub_active1,
            'sub_active2' : self.sub_active2,
            'sub_active3' : self.sub_active3,
        }

data_manager.get_all_raw_inputs()
class TimerManager:
    def __init__(self, ):
        self.group = KeyGroup('a', 'b', 'c', 'd', 'e', 'f')

    def get_data(self):
        return self.group

# 正確使用方式
tm = TimerManager()
a = tm.get_data()
print(a.group_to_dict().keys())




