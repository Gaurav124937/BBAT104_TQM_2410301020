from __future__ import annotations

import customtkinter as ctk


VALID_MODES = ("System", "Light", "Dark")


def set_appearance_mode(mode: str) -> str:
    """
    Apply a CustomTkinter appearance mode globally.

    Valid values are System, Light and Dark.
    Returns the normalized value that was applied.
    """
    normalized = mode.strip().title()

    if normalized not in VALID_MODES:
        raise ValueError(
            f"Invalid appearance mode. Choose one of: {', '.join(VALID_MODES)}."
        )

    ctk.set_appearance_mode(normalized)
    return normalized


def get_appearance_mode() -> str:
    """Return the current CustomTkinter appearance mode."""
    current = ctk.get_appearance_mode()

    # CustomTkinter reports the currently resolved mode for System.
    # The settings screen will default to System until persistence is added.
    if current not in ("Light", "Dark"):
        return "System"

    return current
