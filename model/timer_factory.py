# manager/timer_factory.py
from dataclasses import dataclass, field
from typing import Optional, Dict
from enum import Enum
from core.gui.timer_window import CooldownState

class KeyState(Enum):
    IDLE = "IDLE"
    SELECT = "SELECT"
    LOCK = "LOCK"
    ACTIVE = "ACTIVE"
    SUB_ACTIVE1 = "SUB_ACTIVE1"
    SUB_ACTIVE2 = "SUB_ACTIVE2"
    SUB_ACTIVE3 = "SUB_ACTIVE3"

KEYSTATE_TO_COOLDOWN = {
    KeyState.IDLE: CooldownState.IDLE,
    KeyState.SELECT: CooldownState.SELECTED,
    KeyState.LOCK: CooldownState.LOCKED,
    KeyState.ACTIVE: CooldownState.TRIGGERED,
    # 其他對應視需求補上
}

@dataclass
class KeyGroup:
    select_key: str
    members: Dict[KeyState, str]  # 包含 LOCK, ACTIVE 等

    def to_dict(self) -> dict:
        return {
            "select_key": self.select_key,
            "members": {state.name: key for state, key in self.members.items()}
        }

    @classmethod
    def from_dict(cls, data: dict) -> "KeyGroup":
        members_raw = data.get("members", {})
        members = {
            KeyState[k]: v for k, v in members_raw.items()
            if k in KeyState.__members__ and v
        }

        return cls(
            select_key=data.get("select_key", ""),
            members=members
        )



@dataclass
class KeyMap:
    groups: Dict[str, KeyGroup] = field(default_factory=dict)

    def get_group_by_select(self, select_key: str) -> Optional[KeyGroup]:
        return self.groups.get(select_key)

    def get_lock_in_group(self, select_key: str) -> Optional[str]:
        group = self.get_group_by_select(select_key)
        if group:
            return group.members.get(KeyState.LOCK)

    def get(self, state: KeyState) -> Optional[str]:
        # 提供單鍵查詢（非群組）
        for group in self.groups.values():
            if state in group.members:
                return group.members[state]
        return None

    def to_dict(self) -> dict:
        return {
            group_id: group.to_dict()
            for group_id, group in self.groups.items()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "KeyMap":
        groups = {
            group_id: KeyGroup.from_dict(group_data)
            for group_id, group_data in data.items()
        }
        return cls(groups=groups)

@dataclass
class TimerConfig:
    event_name: str
    limit_time: int
    duration: int
    keymap: KeyMap

    def is_valid(self) -> bool:
        """檢查是否為有效的 Timer 設定"""
        return (
            bool(self.event_name.strip()) and
            self.duration > 0 and
            self.limit_time >= 0 and
            self.keymap.get(KeyState.ACTIVE) is not None
        )

    def to_dict(self) -> dict:
        """轉換為可序列化的 dict 結構"""
        return {
            "event_name": self.event_name,
            "limit_time": self.limit_time,
            "duration": self.duration,
            "keymap": self.keymap.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TimerConfig":
        keymap_data = data.get("keymap", {})
        keymap = KeyMap.from_dict(keymap_data)
        return cls(
            event_name=data.get("event_name", ""),
            limit_time=data.get("limit_time", 0),
            duration=data.get("duration", 0),
            keymap=keymap
        )