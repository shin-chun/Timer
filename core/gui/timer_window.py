import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QApplication
from enum import Enum

class CooldownState(Enum):
    IDLE = 0
    SELECTED = 1
    LOCKED = 2
    TRIGGERED = 3

STATE_COLOR_MAP = {
    CooldownState.IDLE: "white",
    CooldownState.SELECTED: "yellow",
    CooldownState.LOCKED: "red",
    CooldownState.TRIGGERED: "gray"
}

class TimerWindow(QWidget):
    def __init__(self, name: str, cooldown_seconds: int):
        super().__init__()
        self.name = name
        self.cooldown_seconds = cooldown_seconds
        self.remaining = cooldown_seconds
        self.state = CooldownState.IDLE

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

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedHeight(50)

        self.update_label()

    def update_label(self):
        color = STATE_COLOR_MAP.get(self.state, "white")
        text = f"{self.name}：{self.remaining}s"
        self.label.setText(text)
        self.label.setStyleSheet(f"background-color: {color}; border: 1px solid black; color: black;")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 建立一個測試用 TimerWindow
    window = TimerWindow(name="測試", cooldown_seconds=10)
    window.set_state(CooldownState.IDLE)
    window.set_remaining(10)
    window.show()

    sys.exit(app.exec())
