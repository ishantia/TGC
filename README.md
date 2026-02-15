# 💫 TGC – Telegram Group Checker 💫

Administrator
#CloudSnap2023
A powerful Python GUI tool to check user membership and recent messages in Telegram groups. Requires Telegram API credentials and login. Multi-language, dark/light themes, and session management included.

## ⚡️ Features

- 🔌 Connect to Telegram using API ID & API Hash

- 📱 Login with phone number & 2FA if enabled

- 📂 Load group IDs from a text file

- 🔍 Search a target user across multiple groups

- 💬 Show last messages from the user

- 🌐 Multi-language support: English 🇬🇧, Persian 🇮🇷, Chinese 🇨🇳, German 🇩🇪

- 🌙 Toggle Dark/Light theme

- 💾 Persistent session management with a dynamic session file

## 🛠 Requirements

Python 3.10+

Telethon

ttkbootstrap

Install dependencies:

```
pip install telethon ttkbootstrap
```

## 🚀 Getting Started

- Clone the repository -

```
git clone https://github.com/ishantia/TGC.git
```

- Now go to cloned directory and run the GUI -

```
cd TGC
python main.py
```

- Login with Telegram:

  - Enter your API ID & API Hash

  - Enter your phone number

  - Type the verification code

  - Enter 2FA password if enabled

- Select a group file (.txt with one group ID per line)

- Enter target username/ID

- Click Start to see results in the output box

## 📁 Group File Format

```
group1
group2
group3
```

- ⚠️ Each line is a group or channel ID.

## 🔐 Security Tips

- Keep your API credentials & session file private

- Do not commit .env or dynamic_session.session

- Use a .gitignore file:

```
dynamic_session.session
.env
__pycache__/
```

## 🌍 Languages Supported

- English 🇬🇧

- Persian 🇮🇷

- Chinese 🇨🇳

- German 🇩🇪

Change language anytime from the GUI dropdown.
