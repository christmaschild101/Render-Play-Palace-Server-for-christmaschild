"""Account creator GUI — creates the server owner account.

Run locally before deploying to Render:
    uv run python server/account_creator.py

The config (config.toml) can then be committed to git and pushed to Render.
The owner account is stored in PostgreSQL (DATABASE_URL) and persists across deploys.
"""

import asyncio
import sys
from pathlib import Path

import wx

_MODULE_DIR = Path(__file__).parent
_REPO_ROOT = _MODULE_DIR.parent


class AccountCreatorApp(wx.App):
    def OnInit(self):
        dlg = AccountCreatorDialog(None)
        dlg.ShowModal()
        dlg.Destroy()
        return False


class AccountCreatorDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="PlayPalace Account Creator", size=(500, 350))

        self._create_ui()
        self.CenterOnScreen()

    def _create_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label="Create Server Owner Account")
        title_font = title.GetFont()
        title_font.PointSize += 4
        title_font = title_font.Bold()
        title.SetFont(title_font)
        sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)

        # Username
        user_label = wx.StaticText(panel, label="&Username:")
        sizer.Add(user_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self._username = wx.TextCtrl(panel, name="username")
        sizer.Add(self._username, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Password
        pass_label = wx.StaticText(panel, label="&Password:")
        sizer.Add(pass_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self._password = wx.TextCtrl(panel, style=wx.TE_PASSWORD, name="password")
        sizer.Add(self._password, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Confirm password
        confirm_label = wx.StaticText(panel, label="Con&firm Password:")
        sizer.Add(confirm_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self._confirm = wx.TextCtrl(panel, style=wx.TE_PASSWORD, name="confirm password")
        sizer.Add(self._confirm, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._create_btn = wx.Button(panel, wx.ID_OK, "&Create Account")
        self._create_btn.SetDefault()
        btn_sizer.Add(self._create_btn, 0, wx.RIGHT, 5)
        cancel_btn = wx.Button(panel, wx.ID_CANCEL, "&Cancel")
        btn_sizer.Add(cancel_btn, 0)
        sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)

        # Status output (read-only, accessible)
        status_label = wx.StaticText(panel, label="&Status:")
        sizer.Add(status_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self._status = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
            size=(-1, 80),
            name="status output",
        )
        sizer.Add(self._status, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        panel.SetSizer(sizer)

        # Events
        self._create_btn.Bind(wx.EVT_BUTTON, self._on_create)
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CANCEL))

        self._username.SetFocus()

    def _log(self, text: str):
        """Append text to the status output and yield to the event loop."""
        self._status.AppendText(text + "\n")
        wx.SafeYield()

    def _on_create(self, event):
        username = self._username.GetValue().strip()
        password = self._password.GetValue()
        confirm = self._confirm.GetValue()

        if not username:
            self._log("ERROR: Username cannot be empty.")
            self._username.SetFocus()
            return
        if not password:
            self._log("ERROR: Password cannot be empty.")
            self._password.SetFocus()
            return
        if password != confirm:
            self._log("ERROR: Passwords do not match.")
            self._confirm.SetFocus()
            return
        if len(username) < 3:
            self._log("ERROR: Username must be at least 3 characters.")
            self._username.SetFocus()
            return
        if len(password) < 8:
            self._log("ERROR: Password must be at least 8 characters.")
            self._password.SetFocus()
            return

        self._log("Connecting to PostgreSQL (DATABASE_URL)...")
        self._create_btn.Enable(False)
        wx.SafeYield()

        try:
            from server.cli import bootstrap_owner

            async def _do_bootstrap():
                return await bootstrap_owner(
                    username=username,
                    password=password,
                    locale="en",
                    force=True,
                    quiet=True,
                )

            action = asyncio.run(_do_bootstrap())
            self._log(f"SUCCESS: {action} server owner '{username}'.")
            self._log("")
            self._log("The owner account is stored in PostgreSQL and persists across deploys.")
            self._log("You can now commit the config and re-deploy:")
            self._log("  git add -f server/config.toml")
            self._log("  git commit -m 'Update server config'")
            self._log("  git push")
        except Exception as exc:
            self._log(f"ERROR: {exc}")
        finally:
            self._create_btn.Enable(True)
            self._username.SetFocus()


if __name__ == "__main__":
    app = AccountCreatorApp(redirect=False)
    app.MainLoop()
