from __future__ import annotations
import customtkinter as ctk
from services.dashboard_service import get_dashboard_stats, get_recent_issues, get_recent_returns

class DashboardView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(3, weight=1)
        self._build_header()
        self._build_cards()
        self._build_activity()
        self.refresh()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=24, pady=(24, 8))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Dashboard Overview",
                     font=ctk.CTkFont(size=30, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="Quick overview of current library activity",
                     font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w")
        ctk.CTkButton(header, text="Refresh", width=100,
                      command=self.refresh).grid(row=0, column=1, rowspan=2, padx=(10, 0))

    def _build_cards(self):
        self.cards = {}
        items = [
            ("total_books", "Total Books"),
            ("available_books", "Available Copies"),
            ("issued_books", "Currently Issued"),
            ("total_members", "Total Members"),
            ("overdue_books", "Overdue Books"),
            ("returned_today", "Returned Today"),
        ]
        for idx, (key, title) in enumerate(items):
            row, col = 1 + idx // 3, idx % 3
            card = ctk.CTkFrame(self, corner_radius=14)
            card.grid(row=row, column=col, sticky="nsew",
                      padx=(24 if col == 0 else 8, 8 if col < 2 else 24), pady=8)
            ctk.CTkLabel(card, text=title,
                         font=ctk.CTkFont(size=14)).pack(anchor="w", padx=18, pady=(16, 4))
            label = ctk.CTkLabel(card, text="0",
                                 font=ctk.CTkFont(size=30, weight="bold"))
            label.pack(anchor="w", padx=18, pady=(0, 16))
            self.cards[key] = label

    def _build_activity(self):
        left = ctk.CTkFrame(self)
        left.grid(row=3, column=0, columnspan=2, sticky="nsew",
                  padx=(24, 8), pady=(8, 24))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(left, text="Recent Issues",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(
                     row=0, column=0, padx=16, pady=(14, 8), sticky="w")
        self.issue_box = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.issue_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        right = ctk.CTkFrame(self)
        right.grid(row=3, column=2, sticky="nsew",
                   padx=(8, 24), pady=(8, 24))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(right, text="Recent Returns",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(
                     row=0, column=0, padx=16, pady=(14, 8), sticky="w")
        self.return_box = ctk.CTkScrollableFrame(right, fg_color="transparent")
        self.return_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def _clear(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def refresh(self):
        stats = get_dashboard_stats()
        for key, label in self.cards.items():
            label.configure(text=str(stats[key]))

        self._clear(self.issue_box)
        issues = get_recent_issues()
        if not issues:
            ctk.CTkLabel(self.issue_box, text="No issue records yet.").pack(anchor="w", padx=8, pady=8)
        else:
            for row in issues:
                ctk.CTkLabel(
                    self.issue_box,
                    text=(f'#{row["issue_id"]}  •  {row["title"]}\n'
                          f'{row["member_name"]}  |  Due: {row["due_date"]}  |  {row["status"]}'),
                    justify="left", anchor="w"
                ).pack(fill="x", padx=8, pady=8)

        self._clear(self.return_box)
        returns = get_recent_returns()
        if not returns:
            ctk.CTkLabel(self.return_box, text="No return records yet.").pack(anchor="w", padx=8, pady=8)
        else:
            for row in returns:
                ctk.CTkLabel(
                    self.return_box,
                    text=(f'#{row["return_id"]}  •  {row["title"]}\n'
                          f'{row["member_name"]}  |  Returned: {row["return_date"]}'),
                    justify="left", anchor="w"
                ).pack(fill="x", padx=8, pady=8)
