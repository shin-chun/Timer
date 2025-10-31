from typing import  List

from PySide6.QtCore import QSettings
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy

from core.manager.data_manager import data_manager
from core.manager.timer_manager import TimerManager
from core.model.timer_factory import KeyState, STATE_COLOR_MAP, TimerConfig

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from core.utils.resource import resource_path



class TimerWindow(QWidget):
    def __init__(self, event_name, duration, uuid_win, timer_manager: TimerManager, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.event_name = event_name
        self.duration = duration
        self.uuid_win = uuid_win
        self.remaining = duration

        self.state_index = 0

        self.timer_manager = timer_manager

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
        self.timer_manager.tick.connect(self.on_tick)
        self.timer_manager.key_state.connect(self.update_background)
        self.timer_manager.reset_all.connect(self.reset_cooldown)
        self.timer_manager.reset_background.connect(self.reset_background)

        self.timer.timeout.connect(self.update_label)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedHeight(50)

        self.config_data_list = []

        data_manager.subscribe(self.on_timer_updated)

        self.restore_position()

    def on_timer_updated(self, config_data_list: List[TimerConfig]):
        self.config_data_list = [timer_config for timer_config in config_data_list]
        print(f'timer_window的資料{self.config_data_list}')

    def on_tick(self, trigger_id: str):
        if trigger_id != str(self.uuid_win):
            return
        elif self.timer.isActive():
            return
        elif trigger_id == str(self.uuid_win) and not self.timer.isActive():
            self.remaining = self.duration
            self.timer.start(1000)
            return

    def update_label(self):
        text = f"{self.event_name}：{self.remaining}s"
        self.label.setText(text)
        self.adjust_width(text)


        if self.remaining > 0 and self.timer.isActive():
            self.remaining -= 1
        else:
            self.timer.stop()
            self.label.setStyleSheet(f"background-color: #90ee90; color: black;")
            self.label.setText(f'{self.event_name} : {self.duration}s')
            QTimer.singleShot(0, self._play_sound)

    def update_background(self, trigger_id: str, state: KeyState):
        color = STATE_COLOR_MAP.get(state, 'white')
        if trigger_id == str(self.uuid_win):
            if not self.timer.isActive():
                self.label.setStyleSheet(f"background-color: {color}; color: black;")
            else:
                self.label.setStyleSheet(f"background-color: gray; color: black;")

    def reset_background(self, trigger_id: str):
        if not self.timer.isActive():
            self.label.setStyleSheet(f"background-color: white; color: black;")

    def reset_cooldown(self):
        if hasattr(self, "player") and self.player is not None:
            self.player.stop()
        #     print("[DEBUG] 音效已停止")
        #
        # print(f"[Window] {self.event_name} 重置冷卻時間")
        self.remaining = self.duration
        self.label.setText(f"{self.event_name}：{self.remaining}s")
        self.label.setStyleSheet("background-color: white; color: black;")
        self.timer.stop()

    def _play_sound(self):
        try:
            sound_path = resource_path("assets/sound/cooldown_complete.mp3")

            # 建立播放器與音效輸出，綁定在 self 上避免被回收
            self.audio_output = QAudioOutput(self)
            self.player = QMediaPlayer(self)
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(QUrl.fromLocalFile(sound_path))
            self.player.setLoops(1)

            # ✅ 加入播放狀態監聽
            self.player.playbackStateChanged.connect(
                lambda state: print(f"[DEBUG] 播放狀態變更：{state}")
            )

            self.player.play()
            # print(f"[DEBUG] 播放音效：{sound_path}")
        except Exception as e:
            print(f"❌ 播放音效失敗：{e}")

    def adjust_width(self, text: str):
        font = self.label.font()
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(text)
        padding = 40
        total_width = text_width + padding
        self.setFixedWidth(total_width)
        self.label.setFixedWidth(total_width - 20)

    def restore_position(self):
        settings = QSettings("MyApp", "TimerWindow")
        pos = settings.value(f"pos_{self.uuid_win}")
        if pos:
            self.move(pos)

    def closeEvent(self, event):
        settings = QSettings("MyApp", "TimerWindow")
        settings.setValue(f"pos_{self.uuid_win}", self.pos())
        super().closeEvent(event)

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



    # def cycle_state(self):
    #     self.state_index = (self.state_index + 1) % len(self.state_cycle)
    #     self.state = self.state_cycle[self.state_index]
    #     self.update_label()
    #
    #


# def simulate_tick(manager: TimerManager):
#     print("🔔 tick emitted")
#     manager.tick.emit()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     # 建立 manager 與 window
#     manager = TimerManager()
#     window = TimerWindow(event_name="測試事件", duration=10, timer_manager=manager, uuid_win=None)
#     window.show()
#
#     # 啟動 tick 模擬器（非 GUI thread）
#
#     sys.exit(app.exec())

