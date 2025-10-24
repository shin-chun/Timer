import sys
import threading
import time

from typing import Dict

from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QApplication

from core.manager.data_manager import data_manager
from core.manager.timer_manager import TimerManager
from core.model.timer_factory import KeyState, STATE_COLOR_MAP

class TimerWindow(QWidget):
    def __init__(self, name, cooldown_seconds, timer_manager: TimerManager, state: KeyState=KeyState.IDLE):
        super().__init__()
        self.name = name
        self.cooldown_seconds = cooldown_seconds
        self.remaining = cooldown_seconds
        self.state = state
        self.state_cycle = list(KeyState)
        self.state_index = 0

        # 加入 QTimer 每秒切換狀態
        # self.cycle_timer = QTimer(self)
        # self.cycle_timer.timeout.connect(self.cycle_state)
        # self.cycle_timer.start(1000)  # 每 1000 毫秒執行一次

        self._dragging = False
        self._drag_offset = QPoint()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = QFont("Arial", 14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(f'background-color: white;')
        text = f"{self.name}：{self.remaining}s"
        self.label.setText(text)
        self.adjust_width(text)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)
        # self.timer.start(1000)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedHeight(50)

        data_manager.subscribe(self.on_timer_updated)
        timer_manager.tick.connect(self.on_tick)
        # self.on_tick()

        # self.update_label()

    def on_timer_updated(self, raw: Dict):
        if raw.get("event_name") == self.name:
            self.cooldown_seconds = raw.get("duration", self.cooldown_seconds)
            self.remaining = self.cooldown_seconds
            self.update_label()

    def on_tick(self):
        if not self.timer.isActive():
            self.timer.start(1000)

    def update_label(self):
        color = STATE_COLOR_MAP.get(self.state, 'white')
        if self.remaining > 0 and self.timer.isActive():
            self.remaining -= 1
        else:
            self.timer.stop()
            if self.timer.isActive():
                print('tick')
            else:
                print('stop')

        text = f"{self.name}：{self.remaining}s"
        self.label.setText(text)
        self.label.setStyleSheet(f"background-color: {color}; color: black;")
        self.adjust_width(text)

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

