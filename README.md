# 💫 TGC – Telegram Group Checker (v2.0) 💫

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telethon](https://img.shields.io/badge/Telethon-Async-blueviolet.svg)](https://github.com/LonamiWebs/Telethon)
[![ttkbootstrap](https://img.shields.io/badge/UI-ttkbootstrap-orange.svg)](https://github.com/israel-dryer/ttkbootstrap)

A powerful, modern, and thread-safe Python GUI application built to inspect user membership and recent activity across Telegram groups and channels asynchronously.

Developed by **[@ishantia](https://github.com/ishantia)**.

---

## ⚡️ Key Features

- 🔌 **Async Telegram Integration**: Uses Telethon running on a dedicated background event loop thread.
- 🛡️ **Thread-Safe Architecture**: Non-blocking GUI powered by thread-safe message queues (no frozen windows or thread crashes).
- 🔐 **Step-by-Step Authentication**:
  - API ID & API Hash configuration
  - Phone number verification code (SMS/App)
  - Two-Factor Authentication (2FA) password support
- 📊 **Real-Time Progress & Controls**:
  - Live progress bar and group ratio counter (`Progress: 5/20 groups`)
  - **Cancel Search** button to cleanly stop ongoing operations at any time
- 💬 **Rich Activity Inspection**:
  - Finds target member in public and private groups/channels
  - Extracts and displays recent user messages
  - Clickable direct message links (`https://t.me/...`)
- 💾 **Persistent Config & Session Management**: Automatically saves API ID, Hash, theme, language, and last opened group file path locally in `config.json`.
- 🌙 **Dynamic Theme System**: Seamless toggle between **Darkly** 🌙 and **Flatly** ☀️ modern themes.
- 🌐 **Multi-Language Support**:
  - English 🇬🇧
  - Persian (فارسی) 🇮🇷
  - Chinese (中文) 🇨🇳
  - German (Deutsch) 🇩🇪

---

## 🏗️ Project Architecture

```
TGC/
├── tgc/                     # Core Python Package
│   ├── __init__.py          # Package initialization (v2.0.0)
│   ├── config.py            # Local settings & credentials persistence
│   ├── i18n.py              # Internationalization & localized strings
│   ├── telegram_service.py  # Thread-safe async Telethon background worker
│   └── gui/                 # User Interface Components
│       ├── __init__.py
│       ├── app.py           # Main window application (TGCApp)
│       ├── widgets.py       # Custom widgets (RichLogBox, Context Menu, Entry)
│       └── views/
│           ├── auth_view.py   # Login & Authentication view
│           └── search_view.py # Group scanner & results view
├── main.py                  # Entry point script
├── README.md                # Documentation
└── LICENSE                  # License file
```

---

## 🛠️ Requirements

- **Python 3.10+**
- **Telethon**
- **ttkbootstrap**

### Install Dependencies:

```bash
pip install telethon ttkbootstrap
```

---

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ishantia/TGC.git
   cd TGC
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Authenticate**:
   - Enter your **API ID** and **API Hash** (obtained from [my.telegram.org](https://my.telegram.org)).
   - Enter your phone number (e.g. `+1234567890`).
   - Enter the SMS/Telegram verification code.
   - Enter your 2FA Password if enabled.

4. **Search Groups**:
   - Click **Choose File** to pick a `.txt` file containing group/channel usernames or IDs (one per line).
   - Enter target username or User ID.
   - Click **Start Search**.

---

## 📂 Group File Format (`.txt`)

Create a text file containing group IDs or usernames (one entry per line):

```text
@group_username_1
@group_username_2
-1001234567890
group_username_3
```

---

## 🔐 Security & Privacy

- **Never share** your `API ID`, `API HASH`, or `dynamic_session.session` file.
- `config.json` and `dynamic_session.session` are git-ignored by default to prevent accidental credential commits.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
