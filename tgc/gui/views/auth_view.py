import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Callable, Any
from tgc.gui.widgets import EntryWithContext, RichLogBox

class AuthView(ttk.Frame):
    """
    Step-by-step Authentication View handling API ID/Hash, Phone Number,
    SMS Verification Code, and 2FA Password steps.
    """

    def __init__(self, master, get_i18n_func: Callable[[str], str], tg_service, config_mgr, **kwargs):
        super().__init__(master, padding=20, **kwargs)
        self.get_i18n = get_i18n_func
        self.tg_service = tg_service
        self.config_mgr = config_mgr

        self._build_ui()

    def _build_ui(self):
        # 1. API Credentials Card / Frame
        self.api_card = ttk.Labelframe(self, text="Telegram API Setup", padding=15)
        self.api_card.pack(fill=X, pady=(0, 10))

        self.api_id_label = ttk.Label(self.api_card, text=self.get_i18n("api_id_label"))
        self.api_id_label.pack(anchor="w")
        self.api_id_entry = EntryWithContext(self.api_card, self.get_i18n)
        self.api_id_entry.insert(0, str(self.config_mgr.get("api_id", "")))
        self.api_id_entry.pack(fill=X, pady=(2, 8))

        self.api_hash_label = ttk.Label(self.api_card, text=self.get_i18n("api_hash_label"))
        self.api_hash_label.pack(anchor="w")
        self.api_hash_entry = EntryWithContext(self.api_card, self.get_i18n)
        self.api_hash_entry.insert(0, str(self.config_mgr.get("api_hash", "")))
        self.api_hash_entry.pack(fill=X, pady=(2, 8))

        self.connect_btn = ttk.Button(
            self.api_card,
            text=self.get_i18n("connect_btn"),
            command=self._on_connect,
            bootstyle="success"
        )
        self.connect_btn.pack(fill=X, pady=5)

        # 2. Login Flow Frames (Phone, Code, 2FA)
        self.login_card = ttk.Labelframe(self, text="Account Authentication", padding=15)

        # Phone sub-frame
        self.phone_frame = ttk.Frame(self.login_card)
        self.phone_label = ttk.Label(self.phone_frame, text=self.get_i18n("phone_label"))
        self.phone_label.pack(anchor="w")
        self.phone_entry = EntryWithContext(self.phone_frame, self.get_i18n)
        self.phone_entry.pack(fill=X, pady=(2, 8))
        self.send_code_btn = ttk.Button(
            self.phone_frame,
            text=self.get_i18n("send_code_btn"),
            command=self._on_send_code,
            bootstyle="primary"
        )
        self.send_code_btn.pack(fill=X, pady=5)

        # Verification Code sub-frame
        self.code_frame = ttk.Frame(self.login_card)
        self.code_label = ttk.Label(self.code_frame, text=self.get_i18n("code_label"))
        self.code_label.pack(anchor="w")
        self.code_entry = EntryWithContext(self.code_frame, self.get_i18n)
        self.code_entry.pack(fill=X, pady=(2, 8))
        self.login_code_btn = ttk.Button(
            self.code_frame,
            text=self.get_i18n("login_btn"),
            command=self._on_login_code,
            bootstyle="success"
        )
        self.login_code_btn.pack(fill=X, pady=5)

        # 2FA Password sub-frame
        self.password_frame = ttk.Frame(self.login_card)
        self.password_label = ttk.Label(self.password_frame, text=self.get_i18n("password_label"))
        self.password_label.pack(anchor="w")
        self.password_entry = EntryWithContext(self.password_frame, self.get_i18n, show="*")
        self.password_entry.pack(fill=X, pady=(2, 8))
        self.login_pwd_btn = ttk.Button(
            self.password_frame,
            text=self.get_i18n("login_btn"),
            command=self._on_login_password,
            bootstyle="warning"
        )
        self.login_pwd_btn.pack(fill=X, pady=5)

        # 3. Log Box
        self.log_box = RichLogBox(self, self.get_i18n, height=8)
        self.log_box.pack(fill=BOTH, expand=True, pady=(10, 0))

    def _on_connect(self):
        api_id = self.api_id_entry.get().strip()
        api_hash = self.api_hash_entry.get().strip()

        if not api_id or not api_hash:
            self.log_box.append(self.get_i18n("no_api") + "\n", "warning")
            return

        self.config_mgr.update({"api_id": api_id, "api_hash": api_hash})
        self.tg_service.connect(api_id, api_hash)

    def _on_send_code(self):
        phone = self.phone_entry.get().strip()
        if not phone:
            self.log_box.append(self.get_i18n("no_phone") + "\n", "warning")
            return

        self.send_code_btn.config(state="disabled")
        self.tg_service.send_code(phone)

    def _on_login_code(self):
        code = self.code_entry.get().strip()
        if not code:
            self.log_box.append(self.get_i18n("no_code") + "\n", "warning")
            return

        self.login_code_btn.config(state="disabled")
        self.tg_service.login(code=code)

    def _on_login_password(self):
        password = self.password_entry.get().strip()
        if not password:
            self.log_box.append("Please enter your 2FA password.\n", "warning")
            return

        self.login_pwd_btn.config(state="disabled")
        self.tg_service.login(password=password)

    # --- Step State Transitions ---

    def show_phone_step(self):
        self.api_card.pack_forget()
        self.login_card.pack(fill=X, pady=(0, 10))
        self.code_frame.pack_forget()
        self.password_frame.pack_forget()
        self.phone_frame.pack(fill=X)
        self.send_code_btn.config(state="normal")

    def show_code_step(self):
        self.phone_frame.pack_forget()
        self.password_frame.pack_forget()
        self.code_frame.pack(fill=X)
        self.login_code_btn.config(state="normal")

    def show_2fa_step(self):
        self.phone_frame.pack_forget()
        self.code_frame.pack_forget()
        self.password_frame.pack(fill=X)
        self.login_pwd_btn.config(state="normal")

    def reset_to_api_step(self):
        self.login_card.pack_forget()
        self.api_card.pack(fill=X, pady=(0, 10))
        self.send_code_btn.config(state="normal")
        self.login_code_btn.config(state="normal")
        self.login_pwd_btn.config(state="normal")

    def update_texts(self):
        self.api_id_label.config(text=self.get_i18n("api_id_label"))
        self.api_hash_label.config(text=self.get_i18n("api_hash_label"))
        self.connect_btn.config(text=self.get_i18n("connect_btn"))

        self.phone_label.config(text=self.get_i18n("phone_label"))
        self.send_code_btn.config(text=self.get_i18n("send_code_btn"))

        self.code_label.config(text=self.get_i18n("code_label"))
        self.login_code_btn.config(text=self.get_i18n("login_btn"))

        self.password_label.config(text=self.get_i18n("password_label"))
        self.login_pwd_btn.config(text=self.get_i18n("login_btn"))
