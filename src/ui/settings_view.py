from tkinter import messagebox

import customtkinter as ctk

from services.database_admin import (
    initialize_library_database,
    reset_library_database,
)


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, on_database_changed=None):
        super().__init__(master, fg_color="transparent")
        self.on_database_changed = on_database_changed

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=30, weight="bold"),
        ).grid(row=0, column=0, padx=30, pady=(30, 8), sticky="w")

        ctk.CTkLabel(
            self,
            text="Database Management",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=1, column=0, padx=30, pady=(20, 8), sticky="w")

        ctk.CTkLabel(
            self,
            text=(
                "Use Initialize Database to create any missing tables.\n"
                "Use Reset Database only during development/testing to remove "
                "all library records and restart IDs from 1."
            ),
            justify="left",
            wraplength=700,
        ).grid(row=2, column=0, padx=30, pady=(0, 20), sticky="w")

        ctk.CTkButton(
            self,
            text="Initialize Database",
            width=220,
            height=42,
            command=self._initialize_database,
        ).grid(row=3, column=0, padx=30, pady=10, sticky="w")

        ctk.CTkButton(
            self,
            text="Reset Database",
            width=220,
            height=42,
            command=self._reset_database,
        ).grid(row=4, column=0, padx=30, pady=10, sticky="w")

        ctk.CTkLabel(
            self,
            text="Warning: Reset Database permanently deletes all Books, Members, Issues and Returns.",
            text_color="red",
            wraplength=700,
            justify="left",
        ).grid(row=5, column=0, padx=30, pady=(15, 10), sticky="w")

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
        confirmed = messagebox.askyesno(
            "Reset Database",
            (
                "This will permanently delete ALL Books, Members, Issues "
                "and Returns.\n\n"
                "After reset, new IDs will start from 1.\n\n"
                "Do you want to continue?"
            ),
            icon="warning",
        )

        if not confirmed:
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
