import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.filedialog as filedialog
from typing import Callable
from tgc.gui.widgets import EntryWithContext, RichLogBox

class SearchView(ttk.Frame):
    """
    Main Search View featuring Group File Picker, Target User Input,
    Real-time Progress bar, Start/Cancel controls, and Output Log.
    """

    def __init__(self, master, get_i18n_func: Callable[[str], str], tg_service, config_mgr, **kwargs):
        super().__init__(master, padding=20, **kwargs)
        self.get_i18n = get_i18n_func
        self.tg_service = tg_service
        self.config_mgr = config_mgr

        self.group_file_path = self.config_mgr.get("last_group_file", "")
        self.is_searching = False

        self._build_ui()

    def _build_ui(self):
        # 1. Configuration / Input Card
        self.input_card = ttk.Labelframe(self, text="Search Parameters", padding=15)
        self.input_card.pack(fill=X, pady=(0, 10))

        # Group File Selection
        self.file_title_label = ttk.Label(self.input_card, text=self.get_i18n("file_label"))
        self.file_title_label.pack(anchor="w")

        self.file_row = ttk.Frame(self.input_card)
        self.file_row.pack(fill=X, pady=(2, 8))

        self.choose_file_btn = ttk.Button(
            self.file_row,
            text=self.get_i18n("choose_file_btn"),
            command=self._on_choose_file,
            bootstyle="outline-primary"
        )
        self.choose_file_btn.pack(side=LEFT)

        self.file_status_label = ttk.Label(
            self.file_row,
            text=self._get_file_status_text(),
            font=("Helvetica", 9, "italic")
        )
        self.file_status_label.pack(side=LEFT, padx=(10, 0))

        # Target Username Input
        self.target_label = ttk.Label(self.input_card, text=self.get_i18n("target_label"))
        self.target_label.pack(anchor="w", pady=(5, 0))

        self.target_entry = EntryWithContext(self.input_card, self.get_i18n)
        self.target_entry.pack(fill=X, pady=(2, 8))

        # Control Buttons (Start / Cancel)
        self.btn_row = ttk.Frame(self.input_card)
        self.btn_row.pack(fill=X, pady=(5, 0))

        self.start_btn = ttk.Button(
            self.btn_row,
            text=self.get_i18n("start_btn"),
            command=self._on_start_search,
            bootstyle="success"
        )
        self.start_btn.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        self.cancel_btn = ttk.Button(
            self.btn_row,
            text=self.get_i18n("cancel_btn"),
            command=self._on_cancel_search,
            bootstyle="danger",
            state="disabled"
        )
        self.cancel_btn.pack(side=RIGHT, fill=X, expand=True, padx=(5, 0))

        # 2. Progress Indicator Section
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(fill=X, pady=(0, 10))

        self.progress_label = ttk.Label(
            self.progress_frame,
            text=self.get_i18n("progress_label", 0, 0),
            font=("Helvetica", 9, "bold")
        )
        self.progress_label.pack(anchor="w", pady=(0, 2))

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode="determinate",
            bootstyle="success-striped"
        )
        self.progress_bar.pack(fill=X)

        # 3. Output Log Box
        self.log_box = RichLogBox(self, self.get_i18n, height=14)
        self.log_box.pack(fill=BOTH, expand=True)

    def _get_file_status_text(self) -> str:
        if self.group_file_path and os.path.exists(self.group_file_path):
            filename = os.path.basename(self.group_file_path)
            return self.get_i18n("file_selected", filename)
        return self.get_i18n("file_not_selected")

    def _on_choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Group List Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.group_file_path = file_path
            self.config_mgr.set("last_group_file", file_path)
            self.file_status_label.config(text=self._get_file_status_text())

    def _on_start_search(self):
        target = self.target_entry.get().strip()

        if not self.group_file_path or not os.path.exists(self.group_file_path):
            self.log_box.append(self.get_i18n("no_group_file"), "warning")
            return

        if not target:
            self.log_box.append(self.get_i18n("no_target_username"), "warning")
            return

        self.is_searching = True
        self.start_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress_bar.config(value=0)
        self.progress_label.config(text=self.get_i18n("progress_label", 0, 0))
        self.log_box.clear()

        self.tg_service.start_search(self.group_file_path, target)

    def _on_cancel_search(self):
        if self.is_searching:
            self.cancel_btn.config(state="disabled")
            self.tg_service.cancel_search()

    def update_progress(self, current: int, total: int):
        if total > 0:
            pct = (current / total) * 100
            self.progress_bar.config(value=pct)
            self.progress_label.config(text=self.get_i18n("progress_label", current, total))

    def on_search_finished(self, success: bool):
        self.is_searching = False
        self.start_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def update_texts(self):
        self.input_card.config(text="Search Parameters")
        self.file_title_label.config(text=self.get_i18n("file_label"))
        self.choose_file_btn.config(text=self.get_i18n("choose_file_btn"))
        self.file_status_label.config(text=self._get_file_status_text())
        self.target_label.config(text=self.get_i18n("target_label"))
        self.start_btn.config(text=self.get_i18n("start_btn"))
        self.cancel_btn.config(text=self.get_i18n("cancel_btn"))
        self.progress_label.config(text=self.get_i18n("progress_label", int(self.progress_bar["value"]), 100))
