from dataclasses import dataclass, field
from enum import Enum
from tkinter import messagebox
from typing import Optional, List
import uuid

from PySide6.QtWidgets import QWidget

from core.manager.timer_manager import TimerManager


# from pefile import set_format


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

    def config_to_dict(self) -> dict:
        return {
            'event_name' : self.event_name,
            'data.duration' : self.duration,
            'select' : self.select,
            'lock' : self.lock,
            'active' : self.active,
            'sub_active1' : self.sub_active1,
            'sub_active2' : self.sub_active2,
            'sub_active3' : self.sub_active3
        }
COLOR_MAP= {
    'select' : 'yellow',
    'lock' : 'red',
    'active' : 'gray',
    'sub_active1' : 'gray',
    'sub_active2' : 'gray',
    'sub_active3' : 'gray',
    'default' : 'white'
}

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
B = TimerConfig(
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

class TestManager:
    def __init__(self, state: KeyState=KeyState.IDLE):
        self.state = state
        self.id = []

    def match_sequence(self, key):
        config_list_data = self.get_data()
        for config in config_list_data:
            if config.select == 'None' and config.lock == 'None':
                if key == config.active or key == config.sub_active1 or key == config.sub_active2 or key == config.sub_active3:
                    print(config)
            elif key == config.select:
                if self.id:
                    self.id.clear()
                    self.state = KeyState.SELECT
                else:
                    self.state = KeyState.SELECT
            elif key == config.lock and self.state == KeyState.SELECT:
                self.id.append(config.uuid)
                self.state = KeyState.LOCK
            elif key == config.active and self.state == KeyState.LOCK:
                for _ in self.id:
                    if self.id[0] == config.uuid:
                        self.id.clear()
                        print(config)

    def get_data(self) -> list[TimerConfig]:
        raw_configs = config_list
        return raw_configs




def test(config: List[TimerConfig]):
    test_manager = TestManager()
    key_input = ['w', 'Key.shift_r','Key.left', 'Key.up', 'Key.ctrl_l' ]
    for k in key_input:
        test_manager.match_sequence(k)

    for i, c in enumerate(config):
        print(f"[{i}] TimerConfig id: {id(c)}")
        for k, v in c.__dict__.items():
            print(f"{k}: {v}")

def test_config(data):
    print(f'這是測試：{data[0]}')


for config in config_list:
    a = config
    print(a.uuid)




