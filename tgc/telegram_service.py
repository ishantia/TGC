import asyncio
import os
import queue
import threading
import traceback
from typing import Optional, List, Tuple

from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, User
from telethon.errors import (
    SessionPasswordNeededError,
    FloodWaitError,
    PasswordHashInvalidError,
)

class TelegramService:
    """
    Asynchronous Telegram Client controller running in a dedicated background thread.
    Communicates thread-safely with Tkinter via queue.Queue.
    """

    def __init__(self, msg_queue: queue.Queue, session_file: str = "dynamic_session.session"):
        self.queue = msg_queue
        self.session_file = session_file
        self.client: Optional[TelegramClient] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.thread: Optional[threading.Thread] = None
        self._cancel_requested = False
        self._phone: Optional[str] = None
        self._api_id: Optional[int] = None
        self._api_hash: Optional[str] = None

        self._start_event_loop()

    def _start_event_loop(self):
        """Starts background thread running asyncio loop."""
        def run_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()

    def run_async(self, coro):
        """Schedules a coroutine onto the background event loop."""
        if self.loop and self.loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, self.loop)
        return None

    def emit(self, event_type: str, data: any = None, tag: str = "info"):
        """Pushes an event tuple into the thread-safe queue."""
        self.queue.put((event_type, data, tag))

    # --- Connection & Authentication ---

    def connect(self, api_id: str, api_hash: str):
        """Initializes and connects Telethon client."""
        async def _connect():
            try:
                self._api_id = int(api_id)
                self._api_hash = api_hash.strip()

                if self.client:
                    await self.client.disconnect()

                self.client = TelegramClient(self.session_file, self._api_id, self._api_hash)
                await self.client.connect()

                if await self.client.is_user_authorized():
                    me = await self.client.get_me()
                    self.emit("auth_status", True)
                    self.emit("log", ("welcome_message", {}), "success")
                else:
                    self.emit("auth_status", False)
            except Exception as e:
                self.emit("log", ("connection_error", {"e": str(e)}), "error")
                self.emit("auth_status", False)

        self.run_async(_connect())

    def check_session(self, api_id: str, api_hash: str):
        """Checks if active session is already authorized."""
        async def _check():
            try:
                val_api_id = int(api_id) if api_id and str(api_id).isdigit() else 12345
                val_api_hash = api_hash if api_hash else "placeholder"

                if self.client:
                    await self.client.disconnect()

                self.client = TelegramClient(self.session_file, val_api_id, val_api_hash)
                await self.client.connect()

                if await self.client.is_user_authorized():
                    me = await self.client.get_me()
                    username = me.username or me.first_name or "User"
                    self.emit("session_valid", username)
                    self.emit("log", ("welcome_message", {}), "success")
                else:
                    await self.client.disconnect()
                    self.emit("session_invalid", None)
            except Exception as e:
                err_str = str(e)
                if "database is locked" in err_str.lower():
                    self.emit("log", ("database_locked", {}), "error")
                else:
                    self.emit("log", ("session_check_error", {"e": err_str}), "error")
                self.emit("session_invalid", None)

        self.run_async(_check())

    def send_code(self, phone: str):
        """Requests verification code via SMS/Telegram app."""
        async def _send():
            try:
                self._phone = phone.strip()
                if not self.client:
                    self.emit("log", ("connecting", {}), "info")
                    return

                if not self.client.is_connected():
                    await self.client.connect()

                await self.client.send_code_request(self._phone)
                self.emit("code_sent", self._phone)
            except FloodWaitError as e:
                self.emit("log", ("flood_wait", {"seconds": e.seconds}), "error")
                self.emit("auth_error", f"FloodWait: Wait {e.seconds}s")
            except Exception as e:
                err_str = str(e)
                if "database is locked" in err_str.lower():
                    self.emit("log", ("database_locked", {}), "error")
                else:
                    self.emit("log", ("error_sending_code", {"e": err_str}), "error")
                self.emit("auth_error", err_str)

        self.run_async(_send())

    def login(self, code: str = "", password: str = ""):
        """Completes login using code or 2FA password."""
        async def _login():
            try:
                self.emit("log", ("logging_in", {}), "info")
                if not password:
                    await self.client.sign_in(phone=self._phone, code=code.strip())
                else:
                    await self.client.sign_in(password=password.strip())

                me = await self.client.get_me()
                self.emit("login_success", me.username or me.first_name)
                self.emit("log", ("welcome_message", {}), "success")
            except SessionPasswordNeededError:
                self.emit("2fa_required", None)
            except PasswordHashInvalidError:
                self.emit("log", ("invalid_2fa", {}), "error")
                self.emit("auth_error", "Invalid 2FA password")
            except Exception as e:
                err_str = str(e)
                self.emit("log", ("login_error", {"e": err_str}), "error")
                self.emit("auth_error", err_str)

        self.run_async(_login())

    def logout(self):
        """Disconnects client and removes local session file."""
        async def _logout():
            if self.client:
                await self.client.disconnect()
                self.client = None
            if os.path.exists(self.session_file):
                try:
                    os.remove(self.session_file)
                except Exception as e:
                    print(f"Error removing session file: {e}")
            self.emit("logged_out", None)
            self.emit("log", ("logout_message", {}), "warning")

        self.run_async(_logout())

    # --- Search Engine ---

    def cancel_search(self):
        """Triggers cancellation flag for active group search."""
        self._cancel_requested = True

    def start_search(self, group_file_path: str, target_username: str):
        """Scans groups asynchronously and streams results back to queue."""
        self._cancel_requested = False

        async def _search():
            try:
                self.emit("search_started", None)
                self.emit("log", ("starting_search", {}), "info")

                if not self.client or not self.client.is_connected():
                    if self.client:
                        await self.client.connect()
                    else:
                        self.emit("log", ("not_authorized", {}), "error")
                        self.emit("search_finished", False)
                        return

                if not await self.client.is_user_authorized():
                    self.emit("log", ("not_authorized", {}), "error")
                    self.emit("search_finished", False)
                    return

                # Read groups file
                self.emit("log", ("reading_file", {"path": group_file_path}), "info")
                try:
                    with open(group_file_path, "r", encoding="utf-8") as f:
                        group_ids = [line.strip() for line in f if line.strip()]
                    self.emit("log", ("loaded_groups", {"count": len(group_ids)}), "success")
                except Exception as e:
                    self.emit("log", ("error_reading_file", {"e": str(e)}), "error")
                    self.emit("search_finished", False)
                    return

                if not group_ids:
                    self.emit("log", ("no_group_file", {}), "warning")
                    self.emit("search_finished", False)
                    return

                # Resolve target entity first
                try:
                    target_entity = await self.client.get_entity(target_username.strip())
                    if not isinstance(target_entity, User):
                        self.emit("log", ("invalid_target", {"target": target_username}), "error")
                        self.emit("search_finished", False)
                        return
                except Exception as e:
                    self.emit("log", ("invalid_target", {"target": f"{target_username} ({e}) supreme"}), "error")
                    self.emit("search_finished", False)
                    return

                total_groups = len(group_ids)
                found_count = 0

                for idx, group_id in enumerate(group_ids, 1):
                    if self._cancel_requested:
                        self.emit("log", ("search_cancelled", {}), "warning")
                        self.emit("search_finished", True)
                        return

                    self.emit("progress", (idx, total_groups))
                    self.emit("log", ("checking_group", {"idx": idx, "total": total_groups, "group": group_id}), "info")

                    try:
                        entity = await self.client.get_entity(group_id)
                        if not isinstance(entity, (Channel, Chat)):
                            self.emit("log", ("invalid_group", {"group": group_id}), "warning")
                            continue

                        # Check participants
                        user_is_member = False
                        try:
                            participants = await self.client.get_participants(entity, limit=1000)
                            user_is_member = any(p.id == target_entity.id for p in participants)
                        except Exception:
                            # Fallback if participant list restricted
                            pass

                        if user_is_member:
                            found_count += 1
                            group_title = getattr(entity, 'title', str(group_id))
                            self.emit("log", ("user_found", {
                                "user": target_entity.username or target_entity.id,
                                "title": group_title,
                                "group": group_id
                            }), "success")

                            # Fetch recent messages
                            try:
                                messages = await self.client.get_messages(entity, limit=100)
                                user_msgs = [m for m in messages if m.sender_id == target_entity.id][:3]
                                if user_msgs:
                                    self.emit("log", ("last_messages", {"user": target_entity.username or target_entity.id}), "info")
                                    for msg in user_msgs:
                                        if msg.message:
                                            link = f"https://t.me/{group_id}/{msg.id}" if not str(group_id).startswith("-100") else f"https://t.me/c/{str(group_id)[4:]}/{msg.id}"
                                            self.emit("log", ("message_link", {"link": link}), "link")
                                else:
                                    self.emit("log", ("no_messages", {"user": target_entity.username or target_entity.id}), "info")
                            except Exception as e:
                                pass
                        else:
                            group_title = getattr(entity, 'title', str(group_id))
                            self.emit("log", ("user_not_found_in_group", {
                                "user": target_entity.username or target_entity.id,
                                "title": group_title,
                                "group": group_id
                            }), "info")

                    except FloodWaitError as e:
                        self.emit("log", ("flood_wait", {"seconds": e.seconds}), "error")
                        await asyncio.sleep(min(e.seconds, 5))
                    except Exception as e:
                        self.emit("log", ("search_error", {"group": group_id, "e": str(e)}), "error")

                    await asyncio.sleep(0.1)

                if found_count == 0:
                    self.emit("log", ("user_not_found", {}), "warning")
                else:
                    self.emit("log", ("search_completed", {}), "success")

                self.emit("search_finished", True)

            except Exception as e:
                self.emit("log", ("search_error", {"group": "Global", "e": str(e)}), "error")
                self.emit("log", ("search_error_traceback", {"tb": traceback.format_exc()}), "error")
                self.emit("search_finished", False)

        self.run_async(_search())
