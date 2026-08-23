from __future__ import annotations

import json
from pathlib import Path
from tkinter import ttk
import customtkinter as ctk

ROOT = Path(__file__).resolve().parents[2]
THEMES_DIR = ROOT / "themes"
SETTINGS = ROOT / "database" / "app_settings.json"

THEMES = {
    "Blue": THEMES_DIR / "blue.json",
    "Green": THEMES_DIR / "green.json",
    "Purple": THEMES_DIR / "purple.json",
}


def _load_preferences() -> dict:
    if not SETTINGS.exists():
        return {"theme": "Blue", "appearance": "System"}
    try:
        data = json.loads(SETTINGS.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"theme": "Blue", "appearance": "System"}
    except (OSError, json.JSONDecodeError):
        return {"theme": "Blue", "appearance": "System"}


def _save_preferences(data: dict) -> None:
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_selected_theme() -> str:
    value = _load_preferences().get("theme", "Blue")
    return value if value in THEMES else "Blue"


def get_selected_appearance() -> str:
    value = _load_preferences().get("appearance", "System")
    return value if value in ("System", "Light", "Dark") else "System"


def set_theme(theme_name: str) -> str:
    normalized = theme_name.strip().title()
    if normalized not in THEMES:
        raise ValueError("Choose Blue, Green or Purple.")

    ctk.set_default_color_theme(str(THEMES[normalized]))
    preferences = _load_preferences()
    preferences["theme"] = normalized
    _save_preferences(preferences)
    return normalized


def set_appearance(appearance: str) -> str:
    normalized = appearance.strip().title()
    if normalized not in ("System", "Light", "Dark"):
        raise ValueError("Choose System, Light or Dark.")

    ctk.set_appearance_mode(normalized)
    preferences = _load_preferences()
    preferences["appearance"] = normalized
    _save_preferences(preferences)
    apply_ttk_theme()
    return normalized


def initialize_theme_system() -> None:
    set_theme(get_selected_theme())
    set_appearance(get_selected_appearance())


def apply_ttk_theme() -> None:
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    dark = ctk.get_appearance_mode() == "Dark"
    background = "#2B2B2B" if dark else "#F5F5F5"
    foreground = "#F2F2F2" if dark else "#1A1A1A"
    field = "#343A42" if dark else "#FFFFFF"
    selected = "#1F6AA5"

    style.configure(
        "Treeview",
        background=background,
        foreground=foreground,
        fieldbackground=field,
        rowheight=32,
    )
    style.map(
        "Treeview",
        background=[("selected", selected)],
        foreground=[("selected", "#FFFFFF")],
    )
    style.configure(
        "Treeview.Heading",
        background=field,
        foreground=foreground,
        relief="flat",
    )
