from typing import Optional, Dict, Tuple

class Event:
    def __init__(self, group: str, lock_key: str, trigger_key: str, name: str):
        self.group = group
        self.lock_key = lock_key
        self.trigger_key = trigger_key
        self.name = name

class EventManager:
    def __init__(self):
        self.events: Dict[Tuple[str, str], Event] = {}  # (group, trigger_key) → Event
        self.locked_groups: Dict[str, str] = {}         # group → current lock_key
        self.selected_group: Optional[str] = None       # 使用者目前選擇的群組

    def register_event(self, group: str, lock_key: str, trigger_key: str, name: str):
        self.events[(group, trigger_key)] = Event(group, lock_key, trigger_key, name)

    def input_key(self, key: str):
        # Step 1: 選擇群組（若輸入鍵是群組名稱）
        group_names = {event.group for event in self.events.values()}
        if key in group_names:
            self.selected_group = key
            print(f"✅ 選擇群組：{key}")
            return

        # Step 2: 鎖定群組（若輸入鍵是某事件的鎖定鍵）
        if self.selected_group:
            possible_locks = {
                event.lock_key for event in self.events.values()
                if event.group == self.selected_group
            }
            if key in possible_locks:
                self.locked_groups[self.selected_group] = key
                print(f"🔒 群組 {self.selected_group} 已被鎖定（鎖定鍵：{key}）")
                return

        # Step 3: 嘗試觸發事件（需選擇群組）
        if self.selected_group:
            event_key = (self.selected_group, key)
            if event_key in self.events:
                event = self.events[event_key]
                locked_key = self.locked_groups.get(self.selected_group)
                if locked_key == event.lock_key:
                    print(f"✅ 觸發事件：「{event.name}」")
                elif locked_key is None:
                    print(f"⛔ 群組 {self.selected_group} 尚未鎖定，無法觸發「{event.name}」")
                else:
                    print(f"⛔ 群組 {self.selected_group} 鎖定於其他事件（鎖定鍵：{locked_key}），無法觸發「{event.name}」")
                return

        print(f"❌ 無法識別的輸入：{key}")

manager = EventManager()
manager.register_event("A", "left", "B", "事件一：A群組的B鍵")
manager.register_event("A", "down", "C", "事件二：A群組的C鍵")
manager.register_event("K", "right", "D", "事件三：K群組的D鍵")

print("\n🔹 輸入 A（選擇群組）")
manager.input_key("A")

print("\n🔹 輸入 left（鎖定 A 群組）")
manager.input_key("left")

print("\n🔹 輸入 B（應該可以觸發事件一）")
manager.input_key("B")

print("\n🔹 輸入 C（應該無法觸發事件二）")
manager.input_key("C")

print("\n🔹 輸入 K（選擇群組 K）")
manager.input_key("K")

print("\n🔹 輸入 right（鎖定 K 群組）")
manager.input_key("right")

print("\n🔹 輸入 D（應該可以觸發事件三）")
manager.input_key("D")