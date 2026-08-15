import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
from typing import Callable, Optional

class EntryWithContext(ttk.Entry):
    """Entry widget with a right-click context menu (Cut, Copy, Paste)."""

    def __init__(self, master, get_i18n_func: Optional[Callable[[str], str]] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.get_i18n = get_i18n_func or (lambda k: k.capitalize())
        self.context_menu = tk.Menu(self, tearoff=0)
        self.bind("<Button-3>", self._show_context_menu)

    def _show_context_menu(self, event):
        self.context_menu.delete(0, tk.END)
        self.context_menu.add_command(label=self.get_i18n("cut"), command=lambda: self.event_generate("<<Cut>>"))
        self.context_menu.add_command(label=self.get_i18n("copy"), command=lambda: self.event_generate("<<Copy>>"))
        self.context_menu.add_command(label=self.get_i18n("paste"), command=lambda: self.event_generate("<<Paste>>"))
        self.context_menu.post(event.x_root, event.y_root)


class RichLogBox(ttk.Frame):
    """
    Enhanced Rich Log Box with Scrollbar, colored text styling tags,
    clickable hyperlinks, right-click menu, and clear button.
    """

    def __init__(self, master, get_i18n_func: Optional[Callable[[str], str]] = None, height: int = 12, **kwargs):
        super().__init__(master, **kwargs)
        self.get_i18n = get_i18n_func or (lambda k: k)

        # Container setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Text Widget
        self.text_area = tk.Text(
            self,
            height=height,
            wrap="word",
            font=("Consolas", 10),
            padx=10,
            pady=10,
            bd=0,
            relief="flat"
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.text_area.yview, bootstyle="round")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        # Configure Color Tags
        self.text_area.tag_config("info", foreground="#3498DB")
        self.text_area.tag_config("success", foreground="#2ECC71")
        self.text_area.tag_config("warning", foreground="#F39C12")
        self.text_area.tag_config("error", foreground="#E74C3C")
        self.text_area.tag_config("link", foreground="#1ABC9C", underline=1)

        # Bind link click handler
        self.text_area.tag_bind("link", "<Button-1>", self._on_link_click)
        self.text_area.tag_bind("link", "<Enter>", lambda e: self.text_area.config(cursor="hand2"))
        self.text_area.tag_bind("link", "<Leave>", lambda e: self.text_area.config(cursor=""))

        # Context Menu
        self.context_menu = tk.Menu(self.text_area, tearoff=0)
        self.text_area.bind("<Button-3>", self._show_context_menu)

    def _show_context_menu(self, event):
        self.context_menu.delete(0, tk.END)
        self.context_menu.add_command(label=self.get_i18n("copy"), command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.context_menu.add_command(label=self.get_i18n("clear_log_btn"), command=self.clear)
        self.context_menu.post(event.x_root, event.y_root)

    def _on_link_click(self, event):
        try:
            index = self.text_area.index(f"@{event.x},{event.y}")
            line = self.text_area.get(f"{index} linestart", f"{index} lineend")
            if "http" in line:
                url = line[line.find("http"):].strip()
                webbrowser.open(url)
        except Exception as e:
            print(f"Error opening link: {e}")

    def append(self, content: str, tag: str = "info"):
        """Inserts text content into log box with specified color tag."""
        self.text_area.insert(tk.END, content, tag)
        self.text_area.see(tk.END)

    def clear(self):
        """Clears all text from log box."""
        self.text_area.delete("1.0", tk.END)

    def update_colors_for_theme(self, is_dark: bool):
        """Updates text area background and default text color for dark/light themes."""
        if is_dark:
            self.text_area.config(background="#1E272C", foreground="#ECF0F1", insertbackground="white")
            self.text_area.tag_config("info", foreground="#5DADE2")
            self.text_area.tag_config("success", foreground="#52BE80")
            self.text_area.tag_config("warning", foreground="#F5B041")
            self.text_area.tag_config("error", foreground="#EC7063")
            self.text_area.tag_config("link", foreground="#48C9B0", underline=1)
        else:
            self.text_area.config(background="#F8F9FA", foreground="#2C3E50", insertbackground="#2C3E50")
            self.text_area.tag_config("info", foreground="#2980B9")
            self.text_area.tag_config("success", foreground="#27AE60")
            self.text_area.tag_config("warning", foreground="#D35400")
            self.text_area.tag_config("error", foreground="#C0392B")
            self.text_area.tag_config("link", foreground="#16A085", underline=1)
