# 📁 Timer 專案結構說明
```
Timer/
├── assets/
│   └── sound/                         # 音效資源庫（提示音、倒數結束音等）
│       └── cooldown_complete.mp3
├── core/
│   ├── gui/                           # GUI 子模組（視窗、按鈕、UI 元件）
│   │   ├── __init__.py
│   │   ├── edit_window.py             # 編輯計時器視窗（輸入事件、鍵位設定）
│   │   ├── key_map.py                 # 鍵位對應結構（狀態 → 鍵）
│   │   └── timer_window.py            # 計時器視窗（顯示倒數時間）
│   ├── hotkey/                        # 熱鍵模組（鍵盤監聽與觸發）
│   │   ├── __init__.py
│   │   └── listen_key.py              # 全域鍵盤監聽器（偵測鍵盤輸入）
│   └── manager/                       # 管理模組（資料、視窗、計時器）
│       ├── __init__.py
│       ├── data_manager.py            # 資料中心（儲存 TimerConfig、通知訂閱者）
│       ├── edit_window_manager.py     # 編輯視窗管理器（開啟/關閉編輯視窗）
│       ├── key_map.py                 # 鍵位資料管理（可能與 GUI 分離）
│       ├── timer_window_manager.py    # 計時器視窗管理器（啟動/停止計時器）
│       └── timer_manager.py           # 計時器執行管理（倒數邏輯、狀態控制）
├── model/
│   └── timer_factory.py               # Timer 實例工廠（根據 config 建立 timer）
├── main.py                            # 專案進入點（主程式）
├── pyproject.toml                     # 建構與依賴設定（Poetry）
├── readme.md                          # 專案說明文件
├── requirements.txt                   # 套件需求清單（pip 用）
└── timer_config.py                    # 計時器設定資料結構（封裝 event_name、keymap 等）