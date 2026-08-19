from __future__ import annotations

from datetime import date, timedelta
from tkinter import messagebox, ttk

import customtkinter as ctk

from services.issue_service import (
    get_available_books,
    get_members,
    issue_book,
    search_active_issues,
)


class IssueView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.selected_issue_id: int | None = None
        self.book_map = {}
        self.member_map = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._build_header()
        self._build_form()
        self._build_toolbar()
        self._build_table()
        self._load_choices()
        self.refresh_issues()

    def _build_header(self):
        ctk.CTkLabel(
            self,
            text="Issue Book",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).grid(row=0, column=0, padx=24, pady=(20, 10), sticky="w")

    def _build_form(self):
        form = ctk.CTkFrame(self)
        form.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 12))
        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(form, text="Book").grid(row=0, column=0, padx=10, pady=12, sticky="w")
        self.book_combo = ctk.CTkComboBox(form, values=["No books available"])
        self.book_combo.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        ctk.CTkLabel(form, text="Member").grid(row=0, column=2, padx=10, pady=12, sticky="w")
        self.member_combo = ctk.CTkComboBox(form, values=["No members available"])
        self.member_combo.grid(row=0, column=3, padx=10, pady=12, sticky="ew")

        ctk.CTkLabel(form, text="Due Date").grid(row=1, column=0, padx=10, pady=12, sticky="w")
        self.due_date_entry = ctk.CTkEntry(form, placeholder_text="YYYY-MM-DD")
        self.due_date_entry.grid(row=1, column=1, padx=10, pady=12, sticky="ew")
        self.due_date_entry.insert(0, (date.today() + timedelta(days=14)).isoformat())

        ctk.CTkButton(
            form,
            text="Issue Book",
            command=self._issue_selected_book,
        ).grid(row=1, column=2, columnspan=2, padx=10, pady=12, sticky="ew")

    def _build_toolbar(self):
        toolbar = ctk.CTkFrame(self)
        toolbar.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 12))
        toolbar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search active issues by book, member or ID",
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda _event: self.refresh_issues())

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=100,
            command=self._load_choices_and_refresh,
        ).grid(row=0, column=1, padx=(0, 10), pady=10)

    def _build_table(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=3, column=0, sticky="nsew", padx=24, pady=(0, 24))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        columns = (
            "issue_id",
            "book",
            "member",
            "issue_date",
            "due_date",
            "status",
        )
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        headings = {
            "issue_id": "Issue ID",
            "book": "Book",
            "member": "Member",
            "issue_date": "Issue Date",
            "due_date": "Due Date",
            "status": "Status",
        }
        widths = {
            "issue_id": 80,
            "book": 270,
            "member": 220,
            "issue_date": 120,
            "due_date": 120,
            "status": 100,
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load_choices(self):
        books = get_available_books()
        self.book_map = {
            f'{row["book_id"]} - {row["title"]} ({row["available_quantity"]} available)': row["book_id"]
            for row in books
        }
        self.book_combo.configure(values=list(self.book_map) or ["No books available"])
        self.book_combo.set(next(iter(self.book_map), "No books available"))

        members = get_members()
        self.member_map = {
            f'{row["member_id"]} - {row["name"]} ({row["course"]})': row["member_id"]
            for row in members
        }
        self.member_combo.configure(values=list(self.member_map) or ["No members available"])
        self.member_combo.set(next(iter(self.member_map), "No members available"))

    def _load_choices_and_refresh(self):
        self._load_choices()
        self.refresh_issues()

    def _issue_selected_book(self):
        book_id = self.book_map.get(self.book_combo.get())
        member_id = self.member_map.get(self.member_combo.get())

        if book_id is None:
            messagebox.showwarning("Book Required", "Please select an available book.")
            return

        if member_id is None:
            messagebox.showwarning("Member Required", "Please select a member.")
            return

        try:
            issue_id = issue_book(
                book_id=book_id,
                member_id=member_id,
                due_date=self.due_date_entry.get(),
            )
        except Exception as exc:
            messagebox.showerror("Unable to Issue Book", str(exc))
            return

        messagebox.showinfo("Success", f"Book issued successfully.\nIssue ID: {issue_id}")
        self._load_choices()
        self.refresh_issues()

    def _on_select(self, _event=None):
        selection = self.tree.selection()
        if selection:
            self.selected_issue_id = int(
                self.tree.item(selection[0], "values")[0]
            )
        else:
            self.selected_issue_id = None

    def refresh_issues(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in search_active_issues(self.search_entry.get()):
            self.tree.insert(
                "",
                "end",
                values=(
                    row["issue_id"],
                    row["title"],
                    row["member_name"],
                    row["issue_date"],
                    row["due_date"],
                    row["status"],
                ),
            )
