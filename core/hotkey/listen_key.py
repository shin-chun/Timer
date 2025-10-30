from pynput import keyboard
from threading import Thread

class HotkeyListener:
    def __init__(self, timer_manager):
        self.timer_manager = timer_manager
        self.listener = None
        self.running = False
        print(f"[DEBUG] TimerManager 實例：{id(timer_manager)}")

    def start(self):
        if self.running:
            return
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()  # ✅ 已經是非阻塞，不需要包 Thread

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
            print(f"🎹 鍵盤輸入：{key}")  # ✅ 這裡會印出 Key.shift_r、'a' 等原始格式

            if key == keyboard.Key.f8:
                print("🔁 偵測到 F8，執行冷卻重置")
                self.timer_manager.reset_all_cooldowns()
                return
            key_name = str(key).replace("'", "")  # ✅ 保留 Key.ctrl_l 格式
            self.timer_manager.match_sequence(key_name)  # ✅ 傳入原始 pynput key 物件
        except Exception as e:
            print(f"❌ 鍵盤監聽錯誤：{e}")

