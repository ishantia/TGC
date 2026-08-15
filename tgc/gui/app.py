import os
import queue
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from tgc.config import ConfigManager
from tgc.i18n import I18nManager, LANGUAGES
from tgc.telegram_service import TelegramService
from tgc.gui.views.auth_view import AuthView
from tgc.gui.views.search_view import SearchView

class TGCApp(ttk.Window):
    """
    Main Application Window managing themes, header bar, views switching,
    and thread-safe queue event processing.
    """

    def __init__(self):
        # Load configuration
        self.config_mgr = ConfigManager()

        # Initialize window with saved theme
        saved_theme = self.config_mgr.get("theme", "darkly")
        super().__init__(
            title="TGC – Telegram Group Checker",
            themename=saved_theme,
            minsize=(550, 700)
        )
        self.geometry("600x750")

        # Initialize i18n
        self.i18n = I18nManager(self.config_mgr.get("language", "en"))

        # Message Queue for thread-safe UI updates
        self.queue = queue.Queue()

        # Initialize Telegram Service worker
        self.tg_service = TelegramService(
            msg_queue=self.queue,
            session_file=self.config_mgr.get("session_file", "dynamic_session.session")
        )

        self.is_authenticated = False

        self._build_header()
        self._build_container()

        # Update styling colors for current theme
        self._apply_theme_colors()

        # Start queue consumer loop
        self.after(50, self._process_queue)

        # Check existing session on boot
        self._check_initial_session()

        # Window closing handler
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_header(self):
        """Constructs top action bar (Title, Language, Theme, Logout)."""
        self.header_frame = ttk.Frame(self, padding=(15, 10, 15, 5))
        self.header_frame.pack(fill=X)

        # App Title / Logo
        self.title_label = ttk.Label(
            self.header_frame,
            text=self.i18n.get("app_title"),
            font=("Helvetica", 14, "bold")
        )
        self.title_label.pack(side=LEFT)

        # Action Controls Container
        self.controls_frame = ttk.Frame(self.header_frame)
        self.controls_frame.pack(side=RIGHT)

        # Language Selector
        lang_names = {
            "en": "English 🇬🇧",
            "fa": "فارسی 🇮🇷",
            "zh": "中文 🇨🇳",
            "de": "Deutsch 🇩🇪"
        }
        rev_lang_names = {v: k for k, v in lang_names.items()}

        curr_code = self.i18n.current_lang
        self.lang_var = tk.StringVar(value=lang_names.get(curr_code, "English 🇬🇧"))

        self.lang_combo = ttk.Combobox(
            self.controls_frame,
            textvariable=self.lang_var,
            values=list(lang_names.values()),
            state="readonly",
            width=12
        )
        self.lang_combo.pack(side=LEFT, padx=(0, 5))
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self._on_change_language(rev_lang_names.get(self.lang_var.get(), "en")))

        # Theme Toggle Button
        self.theme_btn = ttk.Button(
            self.controls_frame,
            text="🌙" if self.style.theme.name == "darkly" else "☀️",
            command=self._toggle_theme,
            bootstyle="outline-secondary",
            width=3
        )
        self.theme_btn.pack(side=LEFT, padx=(0, 5))

        # Logout Button
        self.logout_btn = ttk.Button(
            self.controls_frame,
            text=self.i18n.get("logout_btn"),
            command=self._on_logout,
            bootstyle="danger-outline"
        )

    def _build_container(self):
        """Constructs main views container."""
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=True)

        self.auth_view = AuthView(
            self.container,
            get_i18n_func=self.i18n.get,
            tg_service=self.tg_service,
            config_mgr=self.config_mgr
        )

        self.search_view = SearchView(
            self.container,
            get_i18n_func=self.i18n.get,
            tg_service=self.tg_service,
            config_mgr=self.config_mgr
        )

    def show_auth_view(self):
        self.search_view.pack_forget()
        self.auth_view.pack(fill=BOTH, expand=True)
        self.logout_btn.pack_forget()
        self.is_authenticated = False

    def show_search_view(self):
        self.auth_view.pack_forget()
        self.search_view.pack(fill=BOTH, expand=True)
        self.logout_btn.pack(side=LEFT)
        self.is_authenticated = True

    def _check_initial_session(self):
        api_id = self.config_mgr.get("api_id", "")
        api_hash = self.config_mgr.get("api_hash", "")
        self.show_auth_view()
        self.tg_service.check_session(api_id, api_hash)

    def _on_logout(self):
        self.tg_service.logout()

    def _toggle_theme(self):
        current_theme = self.style.theme.name
        new_theme = "flatly" if current_theme == "darkly" else "darkly"
        self.style.theme_use(new_theme)
        self.config_mgr.set("theme", new_theme)
        self.theme_btn.config(text="🌙" if new_theme == "darkly" else "☀️")
        self._apply_theme_colors()

    def _apply_theme_colors(self):
        is_dark = self.style.theme.name == "darkly"
        self.auth_view.log_box.update_colors_for_theme(is_dark)
        self.search_view.log_box.update_colors_for_theme(is_dark)

    def _on_change_language(self, lang_code: str):
        self.i18n.set_language(lang_code)
        self.config_mgr.set("language", lang_code)

        # Refresh titles & views
        self.title(self.i18n.get("app_title"))
        self.title_label.config(text=self.i18n.get("app_title"))
        self.logout_btn.config(text=self.i18n.get("logout_btn"))

        self.auth_view.update_texts()
        self.search_view.update_texts()

    def _process_queue(self):
        """Pumps events from background Telegram worker thread every 50ms."""
        try:
            while True:
                event_type, data, tag = self.queue.get_nowait()
                self._handle_event(event_type, data, tag)
        except queue.Empty:
            pass
        finally:
            self.after(50, self._process_queue)

    def _handle_event(self, event_type: str, data: any, tag: str):
        if event_type == "log":
            key, params = data
            formatted_text = self.i18n.get(key, **params)
            target_box = self.search_view.log_box if self.is_authenticated else self.auth_view.log_box
            target_box.append(formatted_text, tag)

        elif event_type == "session_valid":
            self.show_search_view()
            self.search_view.log_box.append(self.i18n.get("welcome_message"), "success")

        elif event_type == "session_invalid":
            self.show_auth_view()

        elif event_type == "auth_status":
            if data:
                self.show_search_view()
            else:
                self.auth_view.show_phone_step()

        elif event_type == "code_sent":
            self.auth_view.show_code_step()

        elif event_type == "2fa_required":
            self.auth_view.show_2fa_step()

        elif event_type == "login_success":
            self.show_search_view()

        elif event_type == "logged_out":
            self.show_auth_view()
            self.auth_view.reset_to_api_step()

        elif event_type == "progress":
            current, total = data
            self.search_view.update_progress(current, total)

        elif event_type == "search_started":
            pass

        elif event_type == "search_finished":
            self.search_view.on_search_finished(data)

    def _on_close(self):
        self.destroy()

    def run(self):
        self.mainloop()
