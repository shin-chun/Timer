# manager/key_map.py
from dataclasses import dataclass, field
from typing import Optional, Dict
from enum import Enum


class KeyState(Enum):
    IDLE = "IDLE"
    SELECT = "SELECT"
    LOCK = "LOCK"
    ACTIVE = "ACTIVE"
    SELECT2 = "SELECT2"
    LOCK2 = "LOCK2"
    ACTIVE2 = "ACTIVE2"


@dataclass
class KeyMap:
    keys: Dict[KeyState, str] = field(default_factory=dict)

    def get(self, state: KeyState) -> Optional[str]:
        return self.keys.get(state)

    def to_dict(self) -> Dict[str, str]:
        return {state.value: key for state, key in self.keys.items()}
