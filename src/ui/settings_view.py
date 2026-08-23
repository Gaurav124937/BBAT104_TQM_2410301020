from __future__ import annotations

from tkinter import messagebox

import customtkinter as ctk

from services.appearance_service import set_appearance_mode
from services.database_admin import (
    initialize_library_database,
    reset_library_database,
)


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, on_database_changed=None, on_appearance_changed=None):
        super().__init__(master, fg_color="transparent")
        self.on_database_changed = on_database_changed
        self.on_appearance_changed = on_appearance_changed

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=30, weight="bold"),
        ).grid(row=0, column=0, padx=30, pady=(30, 8), sticky="w")

        appearance_card = ctk.CTkFrame(self, corner_radius=12)
        appearance_card.grid(row=1, column=0, sticky="ew", padx=30, pady=(16, 12))
        appearance_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            appearance_card,
            text="Appearance",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=(18, 4), sticky="w")

        ctk.CTkLabel(
            appearance_card,
            text="Choose the application appearance. It applies globally.",
        ).grid(row=1, column=0, padx=20, pady=(0, 14), sticky="w")

        mode_row = ctk.CTkFrame(appearance_card, fg_color="transparent")
        mode_row.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

        ctk.CTkLabel(
            mode_row,
            text="Mode:",
            font=ctk.CTkFont(weight="bold"),
        ).pack(side="left", padx=(0, 12))

        self.appearance_menu = ctk.CTkSegmentedButton(
            mode_row,
            values=["System", "Light", "Dark"],
            command=self._change_appearance,
        )
        self.appearance_menu.set("System")
        self.appearance_menu.pack(side="left")

        database_card = ctk.CTkFrame(self, corner_radius=12)
        database_card.grid(row=2, column=0, sticky="ew", padx=30, pady=(12, 24))
        database_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            database_card,
            text="Database Management",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=(18, 4), sticky="w")

        ctk.CTkLabel(
            database_card,
            text=(
                "Initialize creates missing tables without removing data. "
                "Reset permanently deletes all library records."
            ),
            justify="left",
            wraplength=850,
        ).grid(row=1, column=0, padx=20, pady=(0, 16), sticky="w")

        buttons = ctk.CTkFrame(database_card, fg_color="transparent")
        buttons.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

        ctk.CTkButton(
            buttons,
            text="Initialize Database",
            width=190,
            height=40,
            command=self._initialize_database,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            buttons,
            text="Reset Database",
            width=160,
            height=40,
            command=self._reset_database,
        ).pack(side="left")

    def _change_appearance(self, value: str) -> None:
        try:
            set_appearance_mode(value)
            if self.on_appearance_changed:
                self.on_appearance_changed()
        except ValueError as exc:
            messagebox.showerror("Appearance Error", str(exc))

    def _initialize_database(self) -> None:
        try:
            initialize_library_database()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        messagebox.showinfo(
            "Database Ready",
            "Database initialization completed successfully.",
        )

    def _reset_database(self) -> None:
        if not messagebox.askyesno(
            "Reset Database",
            (
                "This will permanently delete ALL Books, Members, "
                "Issues and Returns.\n\n"
                "After reset, new IDs will start from 1.\n\n"
                "Do you want to continue?"
            ),
            icon="warning",
        ):
            return

        try:
            reset_library_database()
        except Exception as exc:
            messagebox.showerror("Database Reset Failed", str(exc))
            return

        if self.on_database_changed:
            self.on_database_changed()

        messagebox.showinfo(
            "Database Reset",
            "Database reset successfully. New records will start from ID 1.",
        )
