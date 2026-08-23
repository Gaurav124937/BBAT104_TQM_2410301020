from __future__ import annotations

import customtkinter as ctk
from tkinter import ttk


def apply_ttk_theme() -> None:
    """Keep classic ttk widgets visually aligned with CustomTkinter."""
    style = ttk.Style()

    try:
        style.theme_use("clam")
    except Exception:
        pass

    dark = ctk.get_appearance_mode() == "Dark"

    background = "#2b2b2b" if dark else "#f5f5f5"
    foreground = "#f2f2f2" if dark else "#1a1a1a"
    field = "#343638" if dark else "#ffffff"
    selected = "#1f6aa5"
    border = "#555555" if dark else "#c7c7c7"

    style.configure(
        "Treeview",
        background=background,
        foreground=foreground,
        fieldbackground=field,
        bordercolor=border,
        rowheight=32,
        font=("Segoe UI", 10),
    )
    style.map(
        "Treeview",
        background=[("selected", selected)],
        foreground=[("selected", "#ffffff")],
    )

    style.configure(
        "Treeview.Heading",
        background=field,
        foreground=foreground,
        bordercolor=border,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Treeview.Heading",
        background=[("active", selected)],
        foreground=[("active", "#ffffff")],
    )


def set_application_appearance(mode: str) -> str:
    normalized = mode.strip().title()
    if normalized not in ("System", "Light", "Dark"):
        raise ValueError("Appearance must be System, Light or Dark.")

    ctk.set_appearance_mode(normalized)
    apply_ttk_theme()
    return normalized
