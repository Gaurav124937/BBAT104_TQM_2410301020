from __future__ import annotations

import customtkinter as ctk

from services.theme_manager import set_application_appearance


VALID_MODES = ("System", "Light", "Dark")


def set_appearance_mode(mode: str) -> str:
    normalized = mode.strip().title()

    if normalized not in VALID_MODES:
        raise ValueError(
            f"Invalid appearance mode. Choose one of: {', '.join(VALID_MODES)}."
        )

    return set_application_appearance(normalized)


def get_appearance_mode() -> str:
    current = ctk.get_appearance_mode()
    return current if current in ("Light", "Dark") else "System"
