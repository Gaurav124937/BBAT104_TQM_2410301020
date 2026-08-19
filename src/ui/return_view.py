from __future__ import annotations

from tkinter import messagebox, ttk

import customtkinter as ctk

from services.issue_service import search_active_issues
from services.return_service import return_book, search_returned_books


class ReturnView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.selected_active_issue_id: int | None = None
        self.selected_return_id: int | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self._build_header()
        self._build_active_section()
        self._build_history_section()
        self.refresh()

    def _build_header(self):
        ctk.CTkLabel(
            self,
            text="Return Book",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).grid(row=0, column=0, padx=24, pady=(20, 10), sticky="w")

    def _build_active_section(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 12))
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="Active Issues",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=12, pady=(12, 5), sticky="w")

        self.active_search = ctk.CTkEntry(
            frame,
            placeholder_text="Search active issues",
        )
        self.active_search.grid(row=1, column=0, padx=12, pady=10, sticky="ew")
        self.active_search.bind("<KeyRelease>", lambda _event: self._refresh_active())

        ctk.CTkButton(
            frame,
            text="Return Selected Book",
            command=self._return_selected,
        ).grid(row=1, column=1, padx=12, pady=10)

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 14))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = (
            "issue_id",
            "book",
            "member",
            "issue_date",
            "due_date",
            "status",
        )
        self.active_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
        )

        headings = {
            "issue_id": "Issue ID",
            "book": "Book",
            "member": "Member",
            "issue_date": "Issue Date",
            "due_date": "Due Date",
            "status": "Status",
        }

        for column in columns:
            self.active_tree.heading(column, text=headings[column])
            self.active_tree.column(column, width=130, anchor="center")

        self.active_tree.column("book", width=250)
        self.active_tree.column("member", width=220)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.active_tree.yview,
        )
        self.active_tree.configure(yscrollcommand=scrollbar.set)

        self.active_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.active_tree.bind("<<TreeviewSelect>>", self._on_active_select)

    def _build_history_section(self):
        label = ctk.CTkLabel(
            self,
            text="Returned Books History",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        label.grid(row=3, column=0, padx=24, pady=(5, 8), sticky="w")

        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=4, column=0, sticky="ew", padx=24, pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)

        self.history_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search returned books",
        )
        self.history_search.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.history_search.bind("<KeyRelease>", lambda _event: self._refresh_history())

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            command=self.refresh,
        ).grid(row=0, column=1, padx=(0, 10), pady=10)

        history_frame = ctk.CTkFrame(self)
        history_frame.grid(row=5, column=0, sticky="nsew", padx=24, pady=(0, 24))
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(0, weight=1)

        columns = (
            "return_id",
            "issue_id",
            "book",
            "member",
            "issue_date",
            "due_date",
            "return_date",
        )
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
        )

        headings = {
            "return_id": "Return ID",
            "issue_id": "Issue ID",
            "book": "Book",
            "member": "Member",
            "issue_date": "Issue Date",
            "due_date": "Due Date",
            "return_date": "Return Date",
        }

        for column in columns:
            self.history_tree.heading(column, text=headings[column])
            self.history_tree.column(column, width=120, anchor="center")

        self.history_tree.column("book", width=240)
        self.history_tree.column("member", width=200)

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_tree.yview,
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _on_active_select(self, _event=None):
        selection = self.active_tree.selection()
        if selection:
            self.selected_active_issue_id = int(
                self.active_tree.item(selection[0], "values")[0]
            )
        else:
            self.selected_active_issue_id = None

    def _return_selected(self):
        if self.selected_active_issue_id is None:
            messagebox.showwarning(
                "Select Issue",
                "Please select an active issue first.",
            )
            return

        values = self.active_tree.item(
            self.active_tree.selection()[0],
            "values",
        )

        confirmed = messagebox.askyesno(
            "Confirm Return",
            f"Return '{values[1]}' issued to '{values[2]}'?",
        )
        if not confirmed:
            return

        try:
            return_book(self.selected_active_issue_id)
        except Exception as exc:
            messagebox.showerror("Unable to Return Book", str(exc))
            return

        messagebox.showinfo("Success", "Book returned successfully.")
        self.selected_active_issue_id = None
        self.refresh()

    def _refresh_active(self):
        for item in self.active_tree.get_children():
            self.active_tree.delete(item)

        for row in search_active_issues(self.active_search.get()):
            self.active_tree.insert(
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

    def _refresh_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for row in search_returned_books(self.history_search.get()):
            self.history_tree.insert(
                "",
                "end",
                values=(
                    row["return_id"],
                    row["issue_id"],
                    row["title"],
                    row["member_name"],
                    row["issue_date"],
                    row["due_date"],
                    row["return_date"],
                ),
            )

    def refresh(self):
        self._refresh_active()
        self._refresh_history()
