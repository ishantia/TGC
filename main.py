import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from telethon.sync import TelegramClient
from telethon.tl.types import Channel, Chat, User
from telethon.errors import SessionPasswordNeededError, FloodWaitError, PasswordHashInvalidError
import asyncio
import threading
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import traceback
import os

# --- Global Variables ---
api_id = None
api_hash = None
client = None
phone = None
group_file_path = None
password_label = None
login_output_box = None
search_output_box = None
session_file = "dynamic_session.session"
loop = asyncio.new_event_loop()
current_language = "en"  # Default language

# --- Language Dictionaries ---
LANGUAGES = {
    "en": {
        "title": "TGC By @ishantia",
        "api_id_label": "API ID:",
        "api_hash_label": "API HASH:",
        "connect_btn": "Connect to Telegram",
        "phone_label": "Phone Number:",
        "send_code_btn": "Send Code",
        "code_label": "Verification Code:",
        "password_label": "Two-Factor Password (if enabled)",
        "login_btn": "Login",
        "file_label": "Select Group File:",
        "choose_file_btn": "Choose File",
        "file_selected": "Selected: {}",
        "file_not_selected": "No file selected",
        "target_label": "Target Username/ID:",
        "start_btn": "Start",
        "logout_btn": "Log Out",
        "theme_btn": "Toggle Dark/Light",
        "language_label": "Language:",
        "back_btn": "Back",
        "welcome_message": "✅ Welcome! Connected to Telegram\n",
        "logout_message": "🔒 Logged out. Please connect again.\n",
        "no_target_username": "⚠️ Please enter a target username.\n",
        "starting_search": "🔄 Starting search...\n",
        "connecting": "🔌 Connecting to Telegram...\n",
        "not_authorized": "❌ User not authorized. Please log in again.\n",
        "no_group_file": "⚠️ Please select a group file\n",
        "reading_file": "📂 Reading group file: {}\n",
        "loaded_groups": "✅ Loaded {} group IDs\n",
        "error_reading_file": "❌ Error reading file: {}\n",
        "checking_group": "🔍 Checking group: {}\n",
        "invalid_group": "⚠️ {} is not a valid group/channel\n",
        "invalid_target": "❌ Invalid target user: {}\n",
        "user_found": "\n✅ {} is a member of {} (@{})\n",
        "last_messages": "📩 Last messages from {}:\n",
        "message_link": "🔗 {}\n",
        "no_messages": "ℹ️ No recent messages from {}\n",
        "user_not_found_in_group": "❌ {} is not a member of {} (@{})\n",
        "user_not_found": "❌ Target user not found in any groups.\n",
        "search_completed": "✅ Search completed.\n",
        "search_error": "❌ Search Error: {}\n",
        "search_error_traceback": "Traceback: {}\n",
        "no_phone": "Please enter a phone number",
        "flood_wait": "Flood wait: Please try again after {} seconds",
        "error_sending_code": "Error sending code: {}",
        "database_locked": "❌ Database is locked. Please delete dynamic_session.session file and try again.\n",
        "no_code": "Please enter the verification code",
        "logging_in": "🔄 Logging in...\n",
        "invalid_2fa": "❌ Invalid two-factor authentication password\n",
        "login_error": "❌ Login Error: {}\n",
        "no_api": "Please enter both API ID and API HASH",
        "connection_error": "Connection Error: {}",
        "session_check_error": "❌ Session Check Error: {}\n",
        "app_error": "Application Error: {}"
    },
    "fa": {
        "title": "بررسی‌کننده گروه تلگرام",
        "api_id_label": "شناسه API:",
        "api_hash_label": "هش API:",
        "connect_btn": "اتصال به تلگرام",
        "phone_label": "شماره تلفن:",
        "send_code_btn": "ارسال کد",
        "code_label": "کد تأیید:",
        "password_label": "رمز دو مرحله‌ای (در صورت فعال بودن)",
        "login_btn": "ورود",
        "file_label": "انتخاب فایل گروه:",
        "choose_file_btn": "انتخاب فایل",
        "file_selected": "انتخاب شد: {}",
        "file_not_selected": "هیچ فایلی انتخاب نشده",
        "target_label": "نام کاربری/شناسه هدف:",
        "start_btn": "شروع",
        "logout_btn": "خروج",
        "theme_btn": "تغییر حالت تیره/روشن",
        "language_label": "زبان:",
        "back_btn": "بازگشت",
        "welcome_message": "✅ خوش آمدید! به تلگرام متصل شدید\n",
        "logout_message": "🔒 خارج شدید. لطفاً دوباره متصل شوید.\n",
        "no_target_username": "⚠️ لطفاً یک نام کاربری وارد کنید.\n",
        "starting_search": "🔄 شروع جستجو...\n",
        "connecting": "🔌 در حال اتصال به تلگرام...\n",
        "not_authorized": "❌ کاربر مجاز نیست. لطفاً دوباره وارد شوید.\n",
        "no_group_file": "⚠️ لطفاً یک فایل گروه انتخاب کنید\n",
        "reading_file": "📂 خواندن فایل گروه: {}\n",
        "loaded_groups": "✅ {} شناسه گروه بارگذاری شد\n",
        "error_reading_file": "❌ خطا در خواندن فایل: {}\n",
        "checking_group": "🔍 بررسی گروه: {}\n",
        "invalid_group": "⚠️ {} یک گروه/کانال معتبر نیست\n",
        "invalid_target": "❌ کاربر هدف نامعتبر: {}\n",
        "user_found": "\n✅ {} عضو گروه {} است (@{})\n",
        "last_messages": "📩 آخرین پیام‌ها از {}:\n",
        "message_link": "🔗 {}\n",
        "no_messages": "ℹ️ پیام جدیدی از {} وجود ندارد\n",
        "user_not_found_in_group": "❌ {} عضو گروه {} نیست (@{})\n",
        "user_not_found": "❌ کاربر هدف در هیچ گروهی پیدا نشد.\n",
        "search_completed": "✅ جستجو تکمیل شد.\n",
        "search_error": "❌ خطای جستجو: {}\n",
        "search_error_traceback": "جزئیات خطا: {}\n",
        "no_phone": "لطفاً شماره تلفن را وارد کنید",
        "flood_wait": "محدودیت زمانی: لطفاً بعد از {} ثانیه دوباره امتحان کنید",
        "error_sending_code": "خطا در ارسال کد: {}",
        "database_locked": "❌ دیتابیس قفل است. لطفاً فایل dynamic_session.session را حذف کنید و دوباره امتحان کنید.\n",
        "no_code": "لطفاً کد تأیید را وارد کنید",
        "logging_in": "🔄 در حال ورود...\n",
        "invalid_2fa": "❌ رمز دو مرحله‌ای نامعتبر است\n",
        "login_error": "❌ خطای ورود: {}\n",
        "no_api": "لطفاً هر دو شناسه API و هش API را وارد کنید",
        "connection_error": "خطای اتصال: {}",
        "session_check_error": "❌ خطای بررسی سشن: {}\n",
        "app_error": "خطای برنامه: {}"
    },
    "zh": {
        "title": "Telegram 群组检查器",
        "api_id_label": "API ID：",
        "api_hash_label": "API Hash：",
        "connect_btn": "连接到 Telegram",
        "phone_label": "电话号码：",
        "send_code_btn": "发送验证码",
        "code_label": "验证码：",
        "password_label": "双重认证密码（如果启用）",
        "login_btn": "登录",
        "file_label": "选择群组文件：",
        "choose_file_btn": "选择文件",
        "file_selected": "已选择：{}",
        "file_not_selected": "未选择文件",
        "target_label": "目标用户名/ID：",
        "start_btn": "开始",
        "logout_btn": "退出",
        "theme_btn": "切换深色/浅色模式",
        "language_label": "语言：",
        "back_btn": "返回",
        "welcome_message": "✅ 欢迎！已连接到 Telegram\n",
        "logout_message": "🔒 已退出。请重新连接。\n",
        "no_target_username": "⚠️ 请输入目标用户名。\n",
        "starting_search": "🔄 开始搜索...\n",
        "connecting": "🔌 正在连接到 Telegram...\n",
        "not_authorized": "❌ 用户未授权。请重新登录。\n",
        "no_group_file": "⚠️ 请选择一个群组文件\n",
        "reading_file": "📂 读取群组文件：{}\n",
        "loaded_groups": "✅ 已加载 {} 个群组 ID\n",
        "error_reading_file": "❌ 读取文件错误：{}\n",
        "checking_group": "🔍 检查群组：{}\n",
        "invalid_group": "⚠️ {} 不是有效的群组/频道\n",
        "invalid_target": "❌ 无效的目标用户：{}\n",
        "user_found": "\n✅ {} 是 {} 的成员 (@{})\n",
        "last_messages": "📩 来自 {} 的最后消息：\n",
        "message_link": "🔗 {}\n",
        "no_messages": "ℹ️ {} 没有最近消息\n",
        "user_not_found_in_group": "❌ {} 不是 {} 的成员 (@{})\n",
        "user_not_found": "❌ 在任何群组中未找到目标用户。\n",
        "search_completed": "✅ 搜索完成。\n",
        "search_error": "❌ 搜索错误：{}\n",
        "search_error_traceback": "错误详情：{}\n",
        "no_phone": "请输入电话号码",
        "flood_wait": "限流等待：请在 {} 秒后重试",
        "error_sending_code": "发送验证码错误：{}",
        "database_locked": "❌ 数据库已锁定。请删除 dynamic_session.session 文件后重试。\n",
        "no_code": "请输入验证码",
        "logging_in": "🔄 正在登录...\n",
        "invalid_2fa": "❌ 双重认证密码无效\n",
        "login_error": "❌ 登录错误：{}\n",
        "no_api": "请同时输入 API ID 和 API Hash",
        "connection_error": "连接错误：{}",
        "session_check_error": "❌ 会话检查错误：{}\n",
        "app_error": "应用程序错误：{}"
    },
    "de": {
        "title": "Telegram Gruppenprüfer",
        "api_id_label": "API ID:",
        "api_hash_label": "API Hash:",
        "connect_btn": "Mit Telegram verbinden",
        "phone_label": "Telefonnummer:",
        "send_code_btn": "Code senden",
        "code_label": "Verifizierungscode:",
        "password_label": "Zwei-Faktor-Passwort (falls aktiviert)",
        "login_btn": "Anmelden",
        "file_label": "Gruppendatei auswählen:",
        "choose_file_btn": "Datei auswählen",
        "file_selected": "Ausgewählt: {}",
        "file_not_selected": "Keine Datei ausgewählt",
        "target_label": "Ziel-Benutzername/ID:",
        "start_btn": "Start",
        "logout_btn": "Abmelden",
        "theme_btn": "Dunkel/Hell umschalten",
        "language_label": "Sprache:",
        "back_btn": "Zurück",
        "welcome_message": "✅ Willkommen! Mit Telegram verbunden\n",
        "logout_message": "🔒 Abgemeldet. Bitte erneut verbinden.\n",
        "no_target_username": "⚠️ Bitte geben Sie einen Ziel-Benutzernamen ein.\n",
        "starting_search": "🔄 Suche starten...\n",
        "connecting": "🔌 Verbinde mit Telegram...\n",
        "not_authorized": "❌ Benutzer nicht autorisiert. Bitte erneut anmelden.\n",
        "no_group_file": "⚠️ Bitte wählen Sie eine Gruppendatei aus\n",
        "reading_file": "📂 Lese Gruppendatei: {}\n",
        "loaded_groups": "✅ {} Gruppen-IDs geladen\n",
        "error_reading_file": "❌ Fehler beim Lesen der Datei: {}\n",
        "checking_group": "🔍 Überprüfe Gruppe: {}\n",
        "invalid_group": "⚠️ {} ist keine gültige Gruppe/Kanal\n",
        "invalid_target": "❌ Ungültiger Ziel-Benutzer: {}\n",
        "user_found": "\n✅ {} ist Mitglied von {} (@{})\n",
        "last_messages": "📩 Letzte Nachrichten von {}:\n",
        "message_link": "🔗 {}\n",
        "no_messages": "ℹ️ Keine aktuellen Nachrichten von {}\n",
        "user_not_found_in_group": "❌ {} ist kein Mitglied von {} (@{})\n",
        "user_not_found": "❌ Ziel-Benutzer in keiner Gruppe gefunden.\n",
        "search_completed": "✅ Suche abgeschlossen.\n",
        "search_error": "❌ Suchfehler: {}\n",
        "search_error_traceback": "Fehlerdetails: {}\n",
        "no_phone": "Bitte geben Sie eine Telefonnummer ein",
        "flood_wait": "Flut-Wartezeit: Bitte nach {} Sekunden erneut versuchen",
        "error_sending_code": "Fehler beim Senden des Codes: {}",
        "database_locked": "❌ Datenbank gesperrt. Bitte löschen Sie die Datei dynamic_session.session und versuchen Sie es erneut.\n",
        "no_code": "Bitte geben Sie den Verifizierungscode ein",
        "logging_in": "🔄 Anmelden...\n",
        "invalid_2fa": "❌ Ungültiges Zwei-Faktor-Passwort\n",
        "login_error": "❌ Anmeldefehler: {}\n",
        "no_api": "Bitte geben Sie sowohl API ID als auch API Hash ein",
        "connection_error": "Verbindungsfehler: {}",
        "session_check_error": "❌ Sitzungsprüfungsfehler: {}\n",
        "app_error": "Anwendungsfehler: {}"
    }
}

# --- Context Menu Setup ---
def add_context_menu(entry):
    context_menu = tk.Menu(entry, tearoff=0)
    context_menu.add_command(label=LANGUAGES[current_language]["cut"] if "cut" in LANGUAGES[current_language] else "Cut", command=lambda: entry.event_generate("<<Cut>>"))
    context_menu.add_command(label=LANGUAGES[current_language]["copy"] if "copy" in LANGUAGES[current_language] else "Copy", command=lambda: entry.event_generate("<<Copy>>"))
    context_menu.add_command(label=LANGUAGES[current_language]["paste"] if "paste" in LANGUAGES[current_language] else "Paste", command=lambda: entry.event_generate("<<Paste>>"))

    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)

    entry.bind("<Button-3>", show_context_menu)

# --- Theme Color Update ---
def update_theme_colors():
    theme = app.style.theme.name
    if theme == "darkly":
        login_output_box.config(background="#2C3E50", foreground="white", insertbackground="white")
        search_output_box.config(background="#2C3E50", foreground="white", insertbackground="white")
        file_label.config(foreground="white")
    else:  # flatly
        login_output_box.config(background="#F8F9FA", foreground="#2C3E50", insertbackground="#2C3E50")
        search_output_box.config(background="#F8F9FA", foreground="#2C3E50", insertbackground="#2C3E50")
        file_label.config(foreground="#2C3E50")

# --- Telegram Worker ---
def telegram_worker(target_username):
    search_output_box.delete("1.0", tk.END)
    search_output_box.insert(tk.END, LANGUAGES[current_language]["starting_search"])
    app.update()

    async def run():
        try:
            search_output_box.insert(tk.END, LANGUAGES[current_language]["connecting"])
            app.update()
            if not client.is_connected():
                await client.connect()
            if not await client.is_user_authorized():
                search_output_box.insert(tk.END, LANGUAGES[current_language]["not_authorized"])
                return

            search_output_box.insert(tk.END, LANGUAGES[current_language]["reading_file"].format(group_file_path))
            if not group_file_path:
                search_output_box.insert(tk.END, LANGUAGES[current_language]["no_group_file"])
                return

            try:
                with open(group_file_path, 'r', encoding='utf-8') as file:
                    group_ids = [line.strip() for line in file if line.strip()]
                search_output_box.insert(tk.END, LANGUAGES[current_language]["loaded_groups"].format(len(group_ids)))
            except Exception as e:
                search_output_box.insert(tk.END, LANGUAGES[current_language]["error_reading_file"].format(e))
                return

            found = False
            for group_id in group_ids:
                try:
                    search_output_box.insert(tk.END, LANGUAGES[current_language]["checking_group"].format(group_id))
                    app.update()
                    entity = await client.get_entity(group_id)
                    if not isinstance(entity, (Channel, Chat)):
                        search_output_box.insert(tk.END, LANGUAGES[current_language]["invalid_group"].format(group_id))
                        continue

                    target_user = await client.get_entity(target_username)
                    if not isinstance(target_user, User):
                        search_output_box.insert(tk.END, LANGUAGES[current_language]["invalid_target"].format(target_username))
                        continue

                    participants = await client.get_participants(entity, limit=1000)
                    user_is_member = any(p.id == target_user.id for p in participants)

                    if user_is_member:
                        found = True
                        search_output_box.insert(tk.END, LANGUAGES[current_language]["user_found"].format(
                            target_user.username or target_user.id, entity.title, group_id))
                        
                        messages = await client.get_messages(entity, limit=100)
                        user_messages = [msg for msg in messages if msg.sender_id == target_user.id][:3]
                        
                        if user_messages:
                            search_output_box.insert(tk.END, LANGUAGES[current_language]["last_messages"].format(
                                target_user.username or target_user.id))
                            for msg in user_messages:
                                if msg.message:
                                    link = f"https://t.me/{group_id}/{msg.id}"
                                    search_output_box.insert(tk.END, LANGUAGES[current_language]["message_link"].format(link))
                        else:
                            search_output_box.insert(tk.END, LANGUAGES[current_language]["no_messages"].format(
                                target_user.username or target_user.id))
                    else:
                        search_output_box.insert(tk.END, LANGUAGES[current_language]["user_not_found_in_group"].format(
                            target_user.username or target_user.id, entity.title, group_id))

                    app.update()  # Update GUI after each group
                    await asyncio.sleep(0.1)  # Small delay to allow GUI to breathe

                except Exception as e:
                    search_output_box.insert(tk.END, LANGUAGES[current_language]["search_error"].format(e))

            if not found:
                search_output_box.insert(tk.END, LANGUAGES[current_language]["user_not_found"])
            else:
                search_output_box.insert(tk.END, LANGUAGES[current_language]["search_completed"])

        except Exception as e:
            search_output_box.insert(tk.END, LANGUAGES[current_language]["search_error"].format(e))
            search_output_box.insert(tk.END, LANGUAGES[current_language]["search_error_traceback"].format(traceback.format_exc()))

    def run_async():
        loop.run_until_complete(run())
        app.after(0, lambda: search_btn.config(state="normal"))  # Re-enable button after search

    threading.Thread(target=run_async, daemon=True).start()

# --- Functions ---
def start_search():
    target_username = input_entry.get().strip()
    if not target_username:
        search_output_box.delete("1.0", tk.END)
        search_output_box.insert(tk.END, LANGUAGES[current_language]["no_target_username"])
        return

    search_btn.config(state="disabled")
    main_frame.pack_forget()
    search_frame.pack(fill=BOTH, expand=True)
    search_output_box.pack(pady=10, fill=BOTH, expand=True)
    threading.Thread(target=lambda: telegram_worker(target_username), daemon=True).start()

def go_back():
    search_frame.pack_forget()
    main_frame.pack(fill=BOTH, expand=True)

def select_file():
    global group_file_path
    group_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if group_file_path:
        file_label.config(text=LANGUAGES[current_language]["file_selected"].format(group_file_path.split('/')[-1]))
    else:
        file_label.config(text=LANGUAGES[current_language]["file_not_selected"])

def connect_telegram():
    global api_id, api_hash, client
    api_id = api_id_entry.get().strip()
    api_hash = api_hash_entry.get().strip()

    if not api_id or not api_hash:
        messagebox.showerror("Error", LANGUAGES[current_language]["no_api"])
        return

    try:
        if client is not None:
            client.disconnect()
        client = TelegramClient(session_file, int(api_id), api_hash, loop=loop)
        show_login_frame()
    except Exception as e:
        messagebox.showerror("Error", LANGUAGES[current_language]["connection_error"].format(e))

def send_code():
    global phone, client
    phone = phone_entry.get().strip()
    if not phone:
        messagebox.showerror("Error", LANGUAGES[current_language]["no_phone"])
        return

    try:
        if not client.is_connected():
            client.connect()
        client.send_code_request(phone)
        phone_frame.pack_forget()
        code_frame.pack(fill=X, pady=5)
        login_output_box.pack(pady=10, fill=BOTH, expand=True)
    except FloodWaitError as e:
        messagebox.showerror("Error", LANGUAGES[current_language]["flood_wait"].format(e.seconds))
    except Exception as e:
        messagebox.showerror("Error", LANGUAGES[current_language]["error_sending_code"].format(e))
        if "database is locked" in str(e).lower():
            login_output_box.delete("1.0", tk.END)
            login_output_box.insert(tk.END, LANGUAGES[current_language]["database_locked"])

def login():
    global client
    code = code_entry.get().strip()
    password = password_entry.get().strip()

    if not code and not password:
        messagebox.showerror("Error", LANGUAGES[current_language]["no_code"])
        return

    login_btn_code.config(state="disabled")
    login_btn_password.config(state="disabled")
    login_output_box.delete("1.0", tk.END)
    login_output_box.insert(tk.END, LANGUAGES[current_language]["logging_in"])
    app.update()

    try:
        if not password:  # First attempt with code
            client.sign_in(phone=phone, code=code)
        else:  # Second attempt with 2FA password
            client.sign_in(password=password)

        login_frame.pack_forget()
        login_output_box.pack_forget()
        main_frame.pack(fill=BOTH, expand=True)
        login_output_box.delete("1.0", tk.END)
        login_output_box.insert(tk.END, LANGUAGES[current_language]["welcome_message"])
    except SessionPasswordNeededError:
        password_label.config(text=LANGUAGES[current_language]["password_label"])
        code_frame.pack_forget()
        password_frame.pack(fill=X, pady=5)
        login_output_box.pack(pady=10, fill=BOTH, expand=True)
    except PasswordHashInvalidError:
        messagebox.showerror("Error", LANGUAGES[current_language]["invalid_2fa"])
        login_output_box.delete("1.0", tk.END)
        login_output_box.insert(tk.END, LANGUAGES[current_language]["invalid_2fa"])
        password_entry.delete(0, tk.END)  # Clear password field
        login_btn_code.config(state="normal")
        login_btn_password.config(state="normal")
    except Exception as e:
        messagebox.showerror("Error", LANGUAGES[current_language]["login_error"].format(e))
        login_output_box.delete("1.0", tk.END)
        login_output_box.insert(tk.END, LANGUAGES[current_language]["login_error"].format(e))
    finally:
        login_btn_code.config(state="normal")
        login_btn_password.config(state="normal")

def logout():
    global client
    if client:
        client.disconnect()
        client = None
        if os.path.exists(session_file):
            os.remove(session_file)
    login_frame.pack_forget()
    main_frame.pack(fill=BOTH, expand=True)
    login_output_box.delete("1.0", tk.END)
    login_output_box.insert(tk.END, LANGUAGES[current_language]["logout_message"])
    connect_telegram()

def check_session():
    global client
    try:
        if client is not None:
            client.disconnect()
        client = TelegramClient(session_file, api_id or 123, api_hash or "placeholder", loop=loop)
        client.connect()
        if client.is_user_authorized():
            login_output_box.delete("1.0", tk.END)
            login_output_box.insert(tk.END, LANGUAGES[current_language]["welcome_message"])
            login_frame.pack_forget()
            main_frame.pack(fill=BOTH, expand=True)
            return True
        client.disconnect()
    except Exception as e:
        login_output_box.delete("1.0", tk.END)
        login_output_box.insert(tk.END, LANGUAGES[current_language]["session_check_error"].format(e))
        if "database is locked" in str(e).lower():
            login_output_box.insert(tk.END, LANGUAGES[current_language]["database_locked"])
    return False

def show_login_frame():
    main_frame.pack_forget()
    login_frame.pack(fill=BOTH, expand=True)
    phone_frame.pack(fill=X, pady=5)
    login_output_box.pack(pady=10, fill=BOTH, expand=True)

def toggle_theme():
    current_theme = app.style.theme.name
    new_theme = "flatly" if current_theme == "darkly" else "darkly"
    app.style.theme_use(new_theme)
    update_theme_colors()

def change_language(event):
    global current_language
    current_language = language_combobox.get()
    if current_language == "English":
        current_language = "en"
    elif current_language == "فارسی":
        current_language = "fa"
    elif current_language == "中文":
        current_language = "zh"
    elif current_language == "Deutsch":
        current_language = "de"

    # Update all UI elements
    app.title(LANGUAGES[current_language]["title"])
    api_id_label.config(text=LANGUAGES[current_language]["api_id_label"])
    api_hash_label.config(text=LANGUAGES[current_language]["api_hash_label"])
    connect_btn.config(text=LANGUAGES[current_language]["connect_btn"])
    phone_label.config(text=LANGUAGES[current_language]["phone_label"])
    send_code_btn.config(text=LANGUAGES[current_language]["send_code_btn"])
    code_label.config(text=LANGUAGES[current_language]["code_label"])
    password_label.config(text="")
    login_btn_code.config(text=LANGUAGES[current_language]["login_btn"])
    login_btn_password.config(text=LANGUAGES[current_language]["login_btn"])
    file_label.config(text=LANGUAGES[current_language]["file_label"])
    file_btn.config(text=LANGUAGES[current_language]["choose_file_btn"])
    file_label.config(text=LANGUAGES[current_language]["file_not_selected"] if not group_file_path else LANGUAGES[current_language]["file_selected"].format(group_file_path.split('/')[-1]))
    target_label.config(text=LANGUAGES[current_language]["target_label"])
    search_btn.config(text=LANGUAGES[current_language]["start_btn"])
    logout_btn.config(text=LANGUAGES[current_language]["logout_btn"])
    theme_btn.config(text=LANGUAGES[current_language]["theme_btn"])
    language_label.config(text=LANGUAGES[current_language]["language_label"])
    back_btn.config(text=LANGUAGES[current_language]["back_btn"])

# --- GUI ---
try:
    asyncio.set_event_loop(loop)
    app = ttk.Window(themename="darkly")
    app.title(LANGUAGES[current_language]["title"])
    app.geometry("500x600")
    app.resizable(False, False)

    # Login Frame
    login_frame = ttk.Frame(app, padding=20)
    phone_frame = ttk.Frame(login_frame)
    code_frame = ttk.Frame(login_frame)
    password_frame = ttk.Frame(login_frame)

    phone_label = ttk.Label(phone_frame, text=LANGUAGES[current_language]["phone_label"])
    phone_label.pack(anchor="w")
    phone_entry = ttk.Entry(phone_frame)
    phone_entry.pack(fill=X, pady=5)
    add_context_menu(phone_entry)
    send_code_btn = ttk.Button(phone_frame, text=LANGUAGES[current_language]["send_code_btn"], command=send_code, bootstyle="success")
    send_code_btn.pack(pady=5, fill=X)

    code_label = ttk.Label(code_frame, text=LANGUAGES[current_language]["code_label"])
    code_label.pack(anchor="w")
    code_entry = ttk.Entry(code_frame)
    code_entry.pack(fill=X, pady=5)
    add_context_menu(code_entry)
    login_btn_code = ttk.Button(code_frame, text=LANGUAGES[current_language]["login_btn"], command=login, bootstyle="success")
    login_btn_code.pack(pady=5, fill=X)

    password_label = ttk.Label(password_frame, text="")
    password_label.pack(anchor="w")
    password_entry = ttk.Entry(password_frame)
    password_entry.pack(fill=X, pady=5)
    add_context_menu(password_entry)
    login_btn_password = ttk.Button(password_frame, text=LANGUAGES[current_language]["login_btn"], command=login, bootstyle="success")
    login_btn_password.pack(pady=5, fill=X)

    login_output_box = tk.Text(login_frame, height=12, wrap="word", font=("Consolas", 10))

    # Main Frame (Input Fields)
    main_frame = ttk.Frame(app, padding=20)
    api_id_label = ttk.Label(main_frame, text=LANGUAGES[current_language]["api_id_label"])
    api_id_label.pack(anchor="w")
    api_id_entry = ttk.Entry(main_frame)
    api_id_entry.pack(fill=X, pady=5)
    add_context_menu(api_id_entry)

    api_hash_label = ttk.Label(main_frame, text=LANGUAGES[current_language]["api_hash_label"])
    api_hash_label.pack(anchor="w")
    api_hash_entry = ttk.Entry(main_frame)
    api_hash_entry.pack(fill=X, pady=5)
    add_context_menu(api_hash_entry)

    connect_btn = ttk.Button(main_frame, text=LANGUAGES[current_language]["connect_btn"], command=connect_telegram, bootstyle="success")
    connect_btn.pack(pady=5, fill=X)

    file_label = ttk.Label(main_frame, text=LANGUAGES[current_language]["file_label"])
    file_label.pack(anchor="w")
    file_btn = ttk.Button(main_frame, text=LANGUAGES[current_language]["choose_file_btn"], command=select_file, bootstyle="primary")
    file_btn.pack(pady=5, fill=X)
    file_label = ttk.Label(main_frame, text=LANGUAGES[current_language]["file_not_selected"])
    file_label.pack(anchor="w")

    target_label = ttk.Label(main_frame, text=LANGUAGES[current_language]["target_label"])
    target_label.pack(anchor="w")
    input_entry = ttk.Entry(main_frame)
    input_entry.pack(fill=X, pady=5)
    add_context_menu(input_entry)

    search_btn = ttk.Button(main_frame, text=LANGUAGES[current_language]["start_btn"], command=start_search, bootstyle="info")
    search_btn.pack(pady=5, fill=X)

    logout_btn = ttk.Button(main_frame, text=LANGUAGES[current_language]["logout_btn"], command=logout, bootstyle="danger")
    logout_btn.pack(pady=5, fill=X)

    theme_btn = ttk.Button(main_frame, text=LANGUAGES[current_language]["theme_btn"], command=toggle_theme, bootstyle="warning", style="TButton")
    theme_btn.pack(pady=5, fill=X)
    theme_btn.configure(style="Large.TButton")

    language_label = ttk.Label(main_frame, text=LANGUAGES[current_language]["language_label"])
    language_label.pack(anchor="w")
    language_combobox = ttk.Combobox(main_frame, values=["English", "فارسی", "中文", "Deutsch"], state="readonly")
    language_combobox.set("English")
    language_combobox.pack(fill=X, pady=5)
    language_combobox.bind("<<ComboboxSelected>>", change_language)

    # Search Frame (Results)
    search_frame = ttk.Frame(app, padding=20)
    back_btn = ttk.Button(search_frame, text=LANGUAGES[current_language]["back_btn"], command=go_back, bootstyle="secondary")
    back_btn.pack(pady=5, fill=X)
    search_output_box = tk.Text(search_frame, height=15, wrap="word", font=("Consolas", 10))

    app.style.configure("Large.TButton", font=("Helvetica", 12, "bold"), padding=10)

    if not check_session():
        main_frame.pack(fill=BOTH, expand=True)
        login_output_box.pack(pady=10, fill=BOTH, expand=True)

    update_theme_colors()
    app.mainloop()

except Exception as e:
    print(f"Error in mainloop: {e}")
    messagebox.showerror("Error", LANGUAGES[current_language]["app_error"].format(e))
finally:
    if client is not None:
        client.disconnect()
