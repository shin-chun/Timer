from pynput import keyboard
from threading import Thread

class HotkeyListener:
    def __init__(self, timer_manager):
        self.timer_manager = timer_manager
        self.listener = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        thread = Thread(target=self.listener.start, daemon=True)
        thread.start()
        print("🎧 HotkeyListener 已啟動")

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None
            print("🛑 HotkeyListener 已停止")

    def on_press(self, key):
        if not self.running:
            return

        try:
            key_name = self.resolve_key_name(key)
            print(f"🎹 鍵盤輸入：{key_name}")

            if key_name == "f8":
                print("🔁 偵測到 F8，執行冷卻重置")
                self.timer_manager.cooldown_manager.reset_all_cooldowns()
                return

            self.timer_manager.input_key(key_name)
        except Exception as e:
            print(f"❌ 鍵盤監聽錯誤：{e}")

    def resolve_key_name(self, key):
        if isinstance(key, keyboard.Key):
            mapping = {
                keyboard.Key.ctrl_l: "Left Ctrl",
                keyboard.Key.ctrl_r: "Right Ctrl",
                keyboard.Key.shift_l: "Left Shift",
                keyboard.Key.shift_r: "Right Shift",
                keyboard.Key.alt_l: "Left Alt",
                keyboard.Key.alt_r: "Right Alt",
                keyboard.Key.enter: "Enter",
                keyboard.Key.space: "Space",
                keyboard.Key.esc: "Esc",
                keyboard.Key.tab: "Tab",
                keyboard.Key.backspace: "Backspace",
                keyboard.Key.up: "Up Arrow",
                keyboard.Key.down: "Down Arrow",
                keyboard.Key.left: "Left Arrow",
                keyboard.Key.right: "Right Arrow",
            }
            return mapping.get(key, key.name)
        else:
            return str(key).replace("'", "")