# timer_config.py
from dataclasses import dataclass
from core.manager.key_map import KeyMap, KeyState


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
        """從 dict 建立 TimerConfig 實例"""
        from core.manager.key_map import KeyMap, KeyState

        keymap_data = data.get("keymap", {})
        keymap = KeyMap({
            KeyState(k): v for k, v in keymap_data.items() if v
        })

        return cls(
            event_name=data.get("event_name", ""),
            limit_time=data.get("limit_time", 0),
            duration=data.get("duration", 0),
            keymap=keymap
        )