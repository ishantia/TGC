TGC (Telegram Group Checker)

A Python GUI tool to check user membership and recent messages in Telegram groups. Requires Telegram API credentials and login. Supports multiple languages, dark/light themes, and session management using Telethon and ttkbootstrap.

Features

Connect to Telegram using API ID and API Hash

Login with phone number and two-factor authentication (2FA) if enabled

Load a list of group IDs from a text file

Search for a target user in multiple groups

Display if the user is a member and their last messages

Multi-language support: English, Persian, Chinese, German

Dark/light theme toggle

Persistent session management with a dynamic session file

Requirements

Python 3.10+

Telethon

ttkbootstrap

Install dependencies with:

pip install telethon ttkbootstrap

Getting Started

Clone the repository:

git clone https://github.com/ishantia/TGC.git
cd TGC


Run the GUI:

python main.py


Enter your Telegram credentials:

API ID and API Hash (from my.telegram.org
)

Phone number

Verification code sent to your account

2FA password if enabled

Select a group file (a .txt file with one group ID per line)

Enter the target username/ID

Start the search to see results in the output box

Usage Notes

The tool creates a dynamic session file (dynamic_session.session) to persist login sessions

Do not share your session file or API credentials

Limit search queries to avoid FloodWait errors from Telegram

Only the first 1000 participants are checked per group (adjustable in the code)

Supported File Format

The group file should be a simple text file, one group ID per line:

group1
group2
group3

Security Tips

Keep your API ID, API Hash, and session file private

Do not commit .env or session files to public repositories

Use a .gitignore file to ignore temporary or sensitive files:

dynamic_session.session
.env
__pycache__/

Languages

The GUI supports:

English (en)

Persian (fa)

Chinese (zh)

German (de)

You can change the language at any time using the dropdown in the main GUI.

License

MIT License – see LICENSE
 for details
