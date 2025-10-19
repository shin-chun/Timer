from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer, QTime

class TimeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tick 計時器")

        # 建立 UI 元件
        self.label = QLabel("目前時間：", self)
        self.label.setStyleSheet("font-size: 24px;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 建立 QTimer，每秒觸發一次
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每 1000 毫秒觸發一次

        self.update_time()  # 初始化顯示一次

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.label.setText(f"目前時間：{current_time}")

if __name__ == "__main__":
    app = QApplication([])
    widget = TimeWidget()
    widget.show()
    app.exec()