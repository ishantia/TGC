🌟TGC – Telegram Group Checker🌟
A powerful Python GUI tool to check user membership and recent messages in Telegram groups. It requires Telegram API credentials and a login to work. The tool comes with features like multi-language support, dark/light themes, and session management.

✨ Features
🔌 Telegram API Connection: Connect to Telegram using your API ID and API Hash.

📱 Secure Login: Log in securely with your phone number and 2FA if enabled.

📂 Group Management: Load group IDs from a text file for easy management.

🔍 User Search: Search for a target user across multiple groups.

💬 Message History: See the last messages from the target user.

🌐 Multi-language Support: Use the app in English 🇬🇧, Persian 🇮🇷, Chinese 🇨🇳, or German 🇩🇪.

🌙 Themes: Toggle between Dark and Light themes.

💾 Persistent Sessions: The app uses dynamic session files to remember your login.

🛠 Requirements
Python 3.10+

Telethon

ttkbootstrap

To install the necessary dependencies, run the following command:

Bash

pip install telethon ttkbootstrap
🚀 Getting Started
Clone the repository:

Bash

git clone https://github.com/ishantia/TGC.git
cd TGC
Run the application:

Bash

python main.py
How to Use:
Enter your API ID and API Hash.

Enter your phone number and the verification code you receive.

Enter your 2FA password if you have one.

Select a group file (.txt with one group ID per line).

Enter the target username or ID.

Click "Start" to see the results in the output box.

📁 Group File Format
Make sure your text file has one group or channel ID per line:

group1
group2
group3
⚠️ Each line must contain a valid group or channel ID.

🔐 Security Tips
Keep your API credentials and session file private.

DO NOT commit your .env or dynamic_session.session file to your repository.

Use a .gitignore file to prevent this:

dynamic_session.session
.env
__pycache__/
