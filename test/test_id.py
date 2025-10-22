import json

events = [
    {
        "event_name": "影子",
        "duration": 60,
        "limit_time": 3,
        "key_labels": [
            "Key.shift_r", "Key.left", "Key.ctrl_l",
            "Key.alt_l", "None", "Key.backspace"
        ]
    },
    {
        "event_name": "百鬼",
        "duration": 25,
        "limit_time": 3,
        "key_labels": [
            "Key.shift_r", "Key.down", "w",
            "e", "f", "v"
        ]
    },
    {
        "event_name": "餘暉",
        "duration": 10,
        "limit_time": 3,
        "key_labels": [
            "Key.shift_r", "Key.up", "Key.ctrl_l",
            "Key.alt_l", "None", "None"
        ]
    },
    {
        "event_name": "覺醒",
        "duration": 15,
        "limit_time": 1,
        "key_labels": [
            "None", "None", "Key.ctrl_l",
            "Key.alt_l", "None", "None"
        ]
    }
]

# 加上識別碼
for i, event in enumerate(events, start=1):
    event["event_id"] = i

# 印出結果
print(json.dumps(events, ensure_ascii=False, indent=2))