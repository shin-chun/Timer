from core.manager.data_manager import data_manager


class TimerWindowManager:
    def __init__(self):
        data_manager.subscribe(self.on_timer_added)

    def on_timer_added(self, timer_data: dict):
        print("新計時器已加入：", timer_data)
        # 可在此建立新視窗、更新 UI、重新整理列表等