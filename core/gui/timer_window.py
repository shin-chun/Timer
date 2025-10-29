import sys
import threading
import time
import uuid
from tkinter.constants import ACTIVE

from typing import Dict, List

from PySide6.QtCore import Qt, QPoint, QTimer, Slot
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QApplication

from core.manager.data_manager import data_manager, DataManager
from core.manager.timer_manager import TimerManager
from core.model.timer_factory import KeyState, STATE_COLOR_MAP, TimerConfig
from functools import partial


class TimerWindow(QWidget):
    def __init__(self, event_name, duration, uuid_win, timer_manager: TimerManager, state: KeyState=KeyState.IDLE, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.event_name = event_name
        self.duration = duration
        self.uuid_win = uuid_win
        self.remaining = duration
        self.state = state

        self.state_index = 0

        self.timer_manager = timer_manager

        # 加入 QTimer 每秒切換狀態
        # self.cycle_timer = QTimer(self)
        # self.cycle_timer.timeout.connect(self.cycle_state)
        # self.cycle_timer.start(1000)  # 每 1000 毫秒執行一次
        # self.state_cycle = list(KeyState)

        self._dragging = False
        self._drag_offset = QPoint()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = QFont("Arial", 14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(f'background-color: white;')
        text = f"{self.event_name}：{self.remaining}s"
        self.label.setText(text)
        self.adjust_width(text)

        self.timer = QTimer(self)
        self.timer.timerId()
        self.timer_manager.tick.connect(self.on_tick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedHeight(50)

        self.config_data = []
        data_manager.subscribe(self.on_timer_updated)

        print(f'{self.event_name}:{self.timer.timerId}->{self.uuid_win}')

        # print(f'on_tick:{id(self.on_tick)}  window:{id(self.label)}, timer:{id(self.timer)}, timer_manager:{id(self.timer_manager)}')


    def on_timer_updated(self, config_list: List[TimerConfig]):
        print(f'config_list: {config_list}')
        for config in config_list:
            if config.event_name == self.event_name:
                self.duration = config.duration

    def on_tick(self, trigger_id: str):
        if trigger_id == str(self.uuid_win):
            if self.timer.isActive():
                print(self.timer.id)
                print('啟動中，滾')
                return
            elif not self.timer.isActive() and self.timer.timerId:
                print(f"[DEBUG] {self.event_name} 收到 tick，開始倒數")
                self.remaining = self.duration
                self.timer.timeout.connect(self.update_label)
                self.timer.start(1000)
                print(self.timer.id)
                return

        # try:
        #     if not self.timer.isActive():
        #         self.timer.start(1000)
        #         self.timer.timeout.connect(self.update_label)
        # except Exception as e:
        #     print(f"[ERROR] on_tick 發生錯誤：{e}")

    def update_label(self):
        color = STATE_COLOR_MAP.get(self.state, 'white')
        text = f"{self.event_name}：{self.remaining}s"
        self.label.setText(text)
        if self.remaining > 0 and self.timer.isActive():
            self.remaining -= 1
            self.label.setText(text)
            self.adjust_width(text)
            self.label.setStyleSheet(f"background-color: {color}; color: black;")
        else:
            self.timer.stop()
            print('時間停止')
            self.label.setText(f'{self.event_name} : {self.duration}s')

    def adjust_width(self, text: str):
        font = self.label.font()
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(text)
        padding = 40
        total_width = text_width + padding
        self.setFixedWidth(total_width)
        self.label.setFixedWidth(total_width - 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging:
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            event.accept()

    def set_state(self, state: KeyState):
        self.state = state
        self.update_label()


    # def cycle_state(self):
    #     self.state_index = (self.state_index + 1) % len(self.state_cycle)
    #     self.state = self.state_cycle[self.state_index]
    #     self.update_label()




# def simulate_tick(manager: TimerManager):
#     print("🔔 tick emitted")
#     manager.tick.emit()
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     # 建立 manager 與 window
#     manager = TimerManager()
#     window = TimerWindow(name="測試事件", cooldown_seconds=10, timer_manager=manager)
#     window.show()
#
#     # 啟動 tick 模擬器（非 GUI thread）
#     threading.Thread(target=simulate_tick, args=(manager,), daemon=True).start()
#
#     sys.exit(app.exec())

