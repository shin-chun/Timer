# test_timer_factory.py
import unittest
from core.model.timer_factory import KeyState, KeyGroup, KeyMap, TimerConfig

class TestTimerFactory(unittest.TestCase):

    def test_keygroup_serialization(self):
        group = KeyGroup(
            select_key="A",
            members={
                KeyState.LOCK: "L",
                KeyState.ACTIVE: "K"
            }
        )
        data = group.group_to_dict()
        restored = KeyGroup.group_from_dict(data)
        self.assertEqual(group.select_key, restored.select_key)
        self.assertEqual(group.members, restored.members)

    def test_keymap_lookup(self):
        group = KeyGroup(select_key="A", members={KeyState.LOCK: "L"})
        keymap = KeyMap(groups={"A": group})
        self.assertEqual(keymap.get_group_by_select("A"), group)
        self.assertEqual(keymap.get_lock_in_group("A"), "L")
        self.assertEqual(keymap.get(KeyState.LOCK), "L")
        self.assertIsNone(keymap.get(KeyState.ACTIVE))

    def test_timerconfig_validation(self):
        group = KeyGroup(select_key="A", members={KeyState.ACTIVE: "K"})
        keymap = KeyMap(groups={"A": group})
        config = TimerConfig(
            event_name="Test",
            limit_time=10,
            duration=5,
            keymap=keymap
        )
        self.assertTrue(config.is_valid())

    def test_timerconfig_serialization(self):
        group = KeyGroup(select_key="A", members={KeyState.ACTIVE: "K"})
        keymap = KeyMap(groups={"A": group})
        config = TimerConfig(
            event_name="Test",
            limit_time=10,
            duration=5,
            keymap=keymap
        )
        data = config.config_to_dict()
        restored = TimerConfig.config_from_dict(data)
        self.assertEqual(config.event_name, restored.event_name)
        self.assertEqual(config.limit_time, restored.limit_time)
        self.assertEqual(config.duration, restored.duration)
        self.assertEqual(
            config.keymap.get(KeyState.ACTIVE),
            restored.keymap.get(KeyState.ACTIVE)
        )

if __name__ == "__main__":
    unittest.main()