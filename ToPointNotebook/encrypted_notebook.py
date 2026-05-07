#!/usr/bin/env python3
"""
Encrypted Notebook - A secure note-taking application.
AES-256-GCM encryption with Argon2id key derivation.
No icons. Clean text menus. Modern UI. All features working.
"""
import sys
import os
import json
import uuid
import secrets
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QListWidget, QListWidgetItem, QSplitter,
    QDialog, QLineEdit, QPushButton, QLabel,
    QMessageBox, QFileDialog, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = "ToPoint Notebook"
APP_VERSION = "2.0.0"
SALT_SIZE = 16
IV_SIZE = 12
KEY_SIZE = 32
DEFAULT_FILE = Path.home() / "notebook.enc"


class NoteFormat(Enum):
    TEXT = "text"
    MARKDOWN = "markdown"


@dataclass
class Note:
    id: str
    title: str
    content: str
    fmt: NoteFormat
    created_at: str
    modified_at: str



def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Argon2id(length=KEY_SIZE, salt=salt, iterations=3, lanes=1, memory_cost=65536)
    return kdf.derive(password.encode("utf-8"))


def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = secrets.token_bytes(SALT_SIZE)
    key = derive_key(password, salt)
    iv = secrets.token_bytes(IV_SIZE)
    ct = AESGCM(key).encrypt(iv, data, None)
    return salt + iv + ct


def decrypt_bytes(blob: bytes, password: str) -> bytes:
    salt = blob[:SALT_SIZE]
    iv = blob[SALT_SIZE:SALT_SIZE + IV_SIZE]
    ct = blob[SALT_SIZE + IV_SIZE:]
    key = derive_key(password, salt)
    return AESGCM(key).decrypt(iv, ct, None)


def notes_to_json(notes: Dict[str, Note]) -> str:
    data = {}
    for nid, n in notes.items():
        data[nid] = {
            "id": n.id, "title": n.title, "content": n.content,
            "fmt": n.fmt.value, "created_at": n.created_at,
            "modified_at": n.modified_at,
        }
    return json.dumps({"version": APP_VERSION, "notes": data}, indent=2)


def json_to_notes(text: str) -> Dict[str, Note]:
    obj = json.loads(text)
    notes: Dict[str, Note] = {}
    for nid, d in obj.get("notes", {}).items():
        notes[nid] = Note(
            id=d["id"], title=d["title"], content=d["content"],
            fmt=NoteFormat(d.get("fmt", d.get("format", "text"))),
            created_at=d["created_at"], modified_at=d["modified_at"],
        )
    return notes


def save_to_file(notes: Dict[str, Note], path: Path, password: str) -> None:
    raw = notes_to_json(notes).encode("utf-8")
    path.write_bytes(encrypt_bytes(raw, password))


def load_from_file(path: Path, password: str) -> Dict[str, Note]:
    blob = path.read_bytes()
    raw = decrypt_bytes(blob, password)
    return json_to_notes(raw.decode("utf-8"))



LIGHT_THEME = """
QMainWindow { background: #f5f5f7; color: #1d1d1f; }
QWidget { background: #f5f5f7; color: #1d1d1f; }
QSplitter::handle { background: #e0e0e0; width: 2px; }
QTextEdit {
    background: #ffffff; color: #1d1d1f; border: 1px solid #d2d2d7;
    border-radius: 6px; padding: 8px; font-size: 11pt;
    selection-background-color: #b4d7ff;
}
QListWidget {
    background: #ffffff; color: #1d1d1f; border: 1px solid #d2d2d7;
    border-radius: 6px; padding: 4px; outline: none;
}
QListWidget::item { padding: 8px 12px; border-radius: 4px; margin: 2px 4px; }
QListWidget::item:selected { background: #0071e3; color: #ffffff; }
QListWidget::item:hover { background: #f0f0f5; }
QLineEdit {
    background: #ffffff; color: #1d1d1f; border: 1px solid #d2d2d7;
    border-radius: 6px; padding: 6px 10px; font-size: 10pt;
}
QLineEdit:focus { border: 1px solid #0071e3; }
QPushButton {
    background: #ffffff; color: #1d1d1f; border: 1px solid #d2d2d7;
    border-radius: 6px; padding: 6px 16px; font-size: 10pt;
}
QPushButton:hover { background: #f0f0f5; border-color: #0071e3; }
QPushButton:pressed { background: #e0e0e5; }
QPushButton#newNoteBtn { background: #0071e3; color: #ffffff; border: none; font-weight: bold; }
QPushButton#newNoteBtn:hover { background: #0077ed; }
QLabel { background: transparent; }
QLabel#sectionTitle { font-size: 13pt; font-weight: bold; color: #1d1d1f; }
QMenuBar { background: #ffffff; color: #1d1d1f; border-bottom: 1px solid #d2d2d7; padding: 2px; }
QMenuBar::item { padding: 4px 10px; border-radius: 4px; }
QMenuBar::item:selected { background: #f0f0f5; }
QMenu { background: #ffffff; color: #1d1d1f; border: 1px solid #d2d2d7; border-radius: 6px; padding: 4px; }
QMenu::item { padding: 6px 24px; border-radius: 4px; }
QMenu::item:selected { background: #0071e3; color: #ffffff; }
QMenu::separator { height: 1px; background: #d2d2d7; margin: 4px 8px; }
QStatusBar { background: #ffffff; color: #86868b; border-top: 1px solid #d2d2d7; font-size: 9pt; }
"""

DARK_THEME = """
QMainWindow { background: #1e1e2e; color: #cdd6f4; }
QWidget { background: #1e1e2e; color: #cdd6f4; }
QSplitter::handle { background: #313244; width: 2px; }
QTextEdit {
    background: #181825; color: #cdd6f4; border: 1px solid #313244;
    border-radius: 6px; padding: 8px; font-size: 11pt;
    selection-background-color: #45475a;
}
QListWidget {
    background: #181825; color: #cdd6f4; border: 1px solid #313244;
    border-radius: 6px; padding: 4px; outline: none;
}
QListWidget::item { padding: 8px 12px; border-radius: 4px; margin: 2px 4px; }
QListWidget::item:selected { background: #45475a; color: #cdd6f4; }
QListWidget::item:hover { background: #313244; }
QLineEdit {
    background: #181825; color: #cdd6f4; border: 1px solid #313244;
    border-radius: 6px; padding: 6px 10px; font-size: 10pt;
}
QLineEdit:focus { border: 1px solid #89b4fa; }
QPushButton {
    background: #313244; color: #cdd6f4; border: 1px solid #45475a;
    border-radius: 6px; padding: 6px 16px; font-size: 10pt;
}
QPushButton:hover { background: #45475a; border-color: #89b4fa; }
QPushButton:pressed { background: #585b70; }
QPushButton#newNoteBtn { background: #89b4fa; color: #1e1e2e; border: none; font-weight: bold; }
QPushButton#newNoteBtn:hover { background: #74c7ec; }
QLabel { background: transparent; }
QLabel#sectionTitle { font-size: 13pt; font-weight: bold; color: #cdd6f4; }
QMenuBar { background: #181825; color: #cdd6f4; border-bottom: 1px solid #313244; padding: 2px; }
QMenuBar::item { padding: 4px 10px; border-radius: 4px; }
QMenuBar::item:selected { background: #313244; }
QMenu { background: #1e1e2e; color: #cdd6f4; border: 1px solid #313244; border-radius: 6px; padding: 4px; }
QMenu::item { padding: 6px 24px; border-radius: 4px; }
QMenu::item:selected { background: #45475a; }
QMenu::separator { height: 1px; background: #313244; margin: 4px 8px; }
QStatusBar { background: #181825; color: #a6adc8; border-top: 1px solid #313244; font-size: 9pt; }
"""



class PasswordDialog(QDialog):
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(320, 130)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(message))
        self._input = QLineEdit()
        self._input.setEchoMode(QLineEdit.EchoMode.Password)
        self._input.returnPressed.connect(self.accept)
        lay.addWidget(self._input)
        btn_row = QHBoxLayout()
        ok = QPushButton("OK")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(ok)
        btn_row.addWidget(cancel)
        lay.addLayout(btn_row)
        self._input.setFocus()

    @property
    def password(self) -> str:
        return self._input.text()


class EncryptedNotebook(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.notes: Dict[str, Note] = {}
        self.file_path: Path = DEFAULT_FILE
        self.password: Optional[str] = None
        self.current_note_id: Optional[str] = None
        self.is_locked: bool = True
        self._dark: bool = False
        self._build_ui()
        self._build_menus()
        self._apply_theme()
        self._set_ui_enabled(False)
        self._authenticate()

    def _build_ui(self) -> None:
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(900, 620)
        root = QWidget()
        self.setCentralWidget(root)
        root_lay = QHBoxLayout(root)
        root_lay.setContentsMargins(0, 0, 0, 0)
        root_lay.setSpacing(0)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        root_lay.addWidget(splitter)

        left = QWidget()
        left.setFixedWidth(280)
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(12, 12, 8, 12)
        left_lay.setSpacing(8)

        hdr = QHBoxLayout()
        lbl = QLabel("Notes")
        lbl.setObjectName("sectionTitle")
        hdr.addWidget(lbl)
        hdr.addStretch()
        btn_new = QPushButton("+ New Note")
        btn_new.setObjectName("newNoteBtn")
        btn_new.clicked.connect(self._on_new_note)
        hdr.addWidget(btn_new)
        left_lay.addLayout(hdr)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search notes...")
        self.search_input.textChanged.connect(self._on_filter)
        left_lay.addWidget(self.search_input)

        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self._on_note_clicked)
        left_lay.addWidget(self.note_list)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self._on_save_note)
        btn_del = QPushButton("Delete")
        btn_del.clicked.connect(self._on_delete_note)
        btn_row.addWidget(btn_save)
        btn_row.addWidget(btn_del)
        left_lay.addLayout(btn_row)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(8, 12, 12, 12)
        right_lay.setSpacing(8)
        ehdr = QHBoxLayout()
        elbl = QLabel("Editor")
        elbl.setObjectName("sectionTitle")
        ehdr.addWidget(elbl)
        ehdr.addStretch()
        btn_theme = QPushButton("Toggle Theme")
        btn_theme.clicked.connect(self._on_toggle_theme)
        ehdr.addWidget(btn_theme)
        right_lay.addLayout(ehdr)
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        right_lay.addWidget(self.editor)
        splitter.addWidget(right)
        splitter.setSizes([280, 620])
        self.statusBar().showMessage("Ready")


    def _build_menus(self) -> None:
        mb = self.menuBar()
        fm = mb.addMenu("File")
        self._act(fm, "New Note", "Ctrl+N", self._on_new_note)
        fm.addSeparator()
        self._act(fm, "Open Notebook...", "Ctrl+O", self._on_open_notebook)
        self._act(fm, "Save Notebook", "Ctrl+S", self._on_save_notebook)
        self._act(fm, "Save Notebook As...", "Ctrl+Shift+S", self._on_save_notebook_as)
        fm.addSeparator()
        self._act(fm, "Import File...", "", self._on_import)
        self._act(fm, "Export Note...", "", self._on_export)
        fm.addSeparator()
        self._act(fm, "Lock", "Ctrl+L", self._on_lock)
        self._act(fm, "Exit", "Ctrl+Q", self.close)
        em = mb.addMenu("Edit")
        self._act(em, "Find", "Ctrl+F", self._on_focus_search)
        self._act(em, "Delete Note", "", self._on_delete_note)
        vm = mb.addMenu("View")
        self._act(vm, "Toggle Theme", "Ctrl+T", self._on_toggle_theme)
        self._act(vm, "Preview Markdown", "Ctrl+P", self._on_preview_md)
        hm = mb.addMenu("Help")
        self._act(hm, "About", "", self._on_about)

    @staticmethod
    def _act(menu, text, shortcut, slot):
        a = QAction(text, menu)
        if shortcut:
            a.setShortcut(shortcut)
        a.triggered.connect(slot)
        menu.addAction(a)

    def _set_ui_enabled(self, on: bool) -> None:
        self.note_list.setEnabled(on)
        self.editor.setEnabled(on)
        self.search_input.setEnabled(on)

    def _apply_theme(self) -> None:
        self.setStyleSheet(DARK_THEME if self._dark else LIGHT_THEME)

    def _authenticate(self) -> None:
        if self.file_path.exists():
            dlg = PasswordDialog(self, "Unlock Notebook", "Enter password to unlock:")
        else:
            dlg = PasswordDialog(self, "Create Notebook", "Set a password for your new notebook:")
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.password:
            self._unlock(dlg.password)
        else:
            self.close()

    def _unlock(self, password: str) -> None:
        try:
            self.password = password
            if self.file_path.exists():
                self.notes = load_from_file(self.file_path, password)
            else:
                self.notes = {}
                save_to_file(self.notes, self.file_path, password)
            self.is_locked = False
            self._set_ui_enabled(True)
            self._refresh_list()
            self.statusBar().showMessage(f"Unlocked - {len(self.notes)} notes")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to unlock: {e}")
            self.close()

    def _on_lock(self) -> None:
        self._persist()
        self.is_locked = True
        self.password = None
        self.notes = {}
        self.current_note_id = None
        self.editor.clear()
        self.note_list.clear()
        self._set_ui_enabled(False)
        self.statusBar().showMessage("Locked")
        self._authenticate()

    def _persist(self) -> None:
        if not self.password or self.is_locked:
            return
        try:
            save_to_file(self.notes, self.file_path, self.password)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def _refresh_list(self) -> None:
        self.note_list.clear()
        for note in sorted(self.notes.values(), key=lambda n: n.modified_at, reverse=True):
            item = QListWidgetItem(note.title)
            item.setData(Qt.ItemDataRole.UserRole, note.id)
            self.note_list.addItem(item)

    def _select_note(self, note_id: str) -> None:
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == note_id:
                self.note_list.setCurrentItem(item)
                self._on_note_clicked(item)
                return


    def _on_new_note(self) -> None:
        if self.is_locked:
            return
        title, ok = QInputDialog.getText(self, "New Note", "Note title:", text="New Note")
        if not ok or not title.strip():
            return
        now = datetime.now(timezone.utc).isoformat()
        note = Note(id=str(uuid.uuid4()), title=title.strip(), content="",
                    fmt=NoteFormat.TEXT, created_at=now, modified_at=now)
        self.notes[note.id] = note
        self._persist()
        self._refresh_list()
        self._select_note(note.id)
        self.statusBar().showMessage(f"Created: {note.title}")

    def _on_note_clicked(self, item: QListWidgetItem) -> None:
        nid = item.data(Qt.ItemDataRole.UserRole)
        note = self.notes.get(nid)
        if not note:
            return
        self._save_editor_to_current()
        self.current_note_id = nid
        self.editor.blockSignals(True)
        self.editor.setPlainText(note.content)
        self.editor.blockSignals(False)
        self.statusBar().showMessage(f"Editing: {note.title}")

    def _save_editor_to_current(self) -> None:
        if not self.current_note_id:
            return
        note = self.notes.get(self.current_note_id)
        if note:
            note.content = self.editor.toPlainText()
            note.modified_at = datetime.now(timezone.utc).isoformat()

    def _on_save_note(self) -> None:
        if self.is_locked or not self.current_note_id:
            self.statusBar().showMessage("No note selected")
            return
        self._save_editor_to_current()
        self._persist()
        self._refresh_list()
        if self.current_note_id:
            self._select_note(self.current_note_id)
        self.statusBar().showMessage("Saved")

    def _on_delete_note(self) -> None:
        if self.is_locked or not self.current_note_id:
            return
        note = self.notes.get(self.current_note_id)
        if not note:
            return
        ans = QMessageBox.question(self, "Delete", f"Delete '{note.title}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ans != QMessageBox.StandardButton.Yes:
            return
        del self.notes[self.current_note_id]
        self.current_note_id = None
        self.editor.clear()
        self._persist()
        self._refresh_list()
        self.statusBar().showMessage("Deleted")

    def _on_filter(self, text: str) -> None:
        q = text.lower().strip()
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if not item:
                continue
            note = self.notes.get(item.data(Qt.ItemDataRole.UserRole))
            if note:
                visible = not q or q in note.title.lower() or q in note.content.lower()
                item.setHidden(not visible)

    def _on_focus_search(self) -> None:
        self.search_input.setFocus()
        self.search_input.selectAll()


    def _on_open_notebook(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Notebook", str(Path.home()),
                                              "Encrypted Notebook (*.enc);;All Files (*)")
        if not path:
            return
        self.file_path = Path(path)
        self._persist()
        self._on_lock()

    def _on_save_notebook(self) -> None:
        self._save_editor_to_current()
        self._persist()
        self.statusBar().showMessage("Notebook saved")

    def _on_save_notebook_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save As", str(Path.home() / "notebook.enc"),
                                              "Encrypted Notebook (*.enc);;All Files (*)")
        if path:
            self.file_path = Path(path)
            self._save_editor_to_current()
            self._persist()
            self.statusBar().showMessage(f"Saved as {self.file_path.name}")

    def _on_import(self) -> None:
        if self.is_locked:
            return
        path, _ = QFileDialog.getOpenFileName(self, "Import File", str(Path.home()),
                                              "Text Files (*.txt *.md *.markdown);;All Files (*)")
        if not path:
            return
        try:
            p = Path(path)
            content = p.read_text(encoding="utf-8")
            fmt = NoteFormat.MARKDOWN if p.suffix.lower() in (".md", ".markdown") else NoteFormat.TEXT
            now = datetime.now(timezone.utc).isoformat()
            note = Note(id=str(uuid.uuid4()), title=p.stem, content=content,
                        fmt=fmt, created_at=now, modified_at=now)
            self.notes[note.id] = note
            self._persist()
            self._refresh_list()
            self._select_note(note.id)
            self.statusBar().showMessage(f"Imported: {p.name}")
        except Exception as e:
            QMessageBox.critical(self, "Import Error", str(e))

    def _on_export(self) -> None:
        if self.is_locked or not self.current_note_id:
            return
        note = self.notes.get(self.current_note_id)
        if not note:
            return
        ext = ".md" if note.fmt == NoteFormat.MARKDOWN else ".txt"
        path, _ = QFileDialog.getSaveFileName(self, "Export Note",
                                              str(Path.home() / f"{note.title}{ext}"),
                                              "Text Files (*.txt);;Markdown (*.md);;All Files (*)")
        if path:
            try:
                Path(path).write_text(note.content, encoding="utf-8")
                self.statusBar().showMessage(f"Exported: {Path(path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", str(e))

    def _on_toggle_theme(self) -> None:
        self._dark = not self._dark
        self._apply_theme()
        self.statusBar().showMessage("Dark mode" if self._dark else "Light mode")

    def _on_preview_md(self) -> None:
        if not self.current_note_id:
            return
        note = self.notes.get(self.current_note_id)
        if not note:
            return
        html = self._md_to_html(note.content)
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Preview: {note.title}")
        dlg.resize(600, 450)
        lay = QVBoxLayout(dlg)
        view = QTextEdit()
        view.setReadOnly(True)
        view.setHtml(html)
        lay.addWidget(view)
        btn = QPushButton("Close")
        btn.clicked.connect(dlg.close)
        lay.addWidget(btn)
        dlg.exec()

    @staticmethod
    def _md_to_html(md: str) -> str:
        h = md
        h = re.sub(r"^### (.+)$", r"<h3>\1</h3>", h, flags=re.MULTILINE)
        h = re.sub(r"^## (.+)$", r"<h2>\1</h2>", h, flags=re.MULTILINE)
        h = re.sub(r"^# (.+)$", r"<h1>\1</h1>", h, flags=re.MULTILINE)
        h = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", h)
        h = re.sub(r"\*(.+?)\*", r"<i>\1</i>", h)
        h = re.sub(r"`(.+?)`", r"<code>\1</code>", h)
        h = h.replace("\n", "<br>")
        return f"<html><body style='font-family:sans-serif;padding:12px'>{h}</body></html>"

    def _on_about(self) -> None:
        QMessageBox.about(self, "About",
                          f"{APP_NAME} v{APP_VERSION}\n\n"
                          "Secure note-taking with AES-256-GCM encryption.\n"
                          "Your notes stay local. No cloud. No tracking.")

    def closeEvent(self, event) -> None:
        self._save_editor_to_current()
        self._persist()
        event.accept()


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    window = EncryptedNotebook()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
