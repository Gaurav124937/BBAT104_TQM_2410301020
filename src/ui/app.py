import customtkinter as ctk

from database.schema import initialize_database
from ui.books_view import BooksView
from ui.calendar_view import CalendarView
from ui.dashboard_view import DashboardView
from ui.issue_view import IssueView
from ui.members_view import MembersView
from ui.return_view import ReturnView
from ui.settings_view import SettingsView


class LibraryApp(ctk.CTk):
    def __init__(self):
        initialize_database()

        super().__init__()

        self.title("Library Management System")
        self.geometry("1280x820")
        self.minsize(900, 650)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(
            self,
            width=210,
            corner_radius=0,
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="Library Manager",
            font=ctk.CTkFont(size=21, weight="bold"),
        ).pack(pady=(28, 26))

        for page in (
            "Dashboard",
            "Books",
            "Members",
            "Issue Book",
            "Return Book",
            "Records",
            "Calendar",
            "Settings",
        ):
            ctk.CTkButton(
                sidebar,
                text=page,
                height=38,
                command=lambda selected=page: self.show_page(selected),
            ).pack(
                fill="x",
                padx=18,
                pady=5,
            )

        ctk.CTkLabel(
            sidebar,
            text="Q03: Improve Usability",
            font=ctk.CTkFont(size=11),
        ).pack(
            side="bottom",
            pady=18,
        )

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
        )
        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
        )
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.show_page("Dashboard")

    def show_page(self, page: str):
        for widget in self.content.winfo_children():
            widget.destroy()

        views = {
            "Dashboard": DashboardView,
            "Books": BooksView,
            "Members": MembersView,
            "Issue Book": IssueView,
            "Return Book": ReturnView,
            "Calendar": CalendarView,
        }

        if page in views:
            view = views[page](self.content)
            view.grid(
                row=0,
                column=0,
                sticky="nsew",
            )
            return

        if page == "Settings":
            view = SettingsView(
                self.content,
                on_database_changed=lambda: self.show_page("Dashboard"),
            )
            view.grid(
                row=0,
                column=0,
                sticky="nsew",
            )
            return

        frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent",
        )
        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        ctk.CTkLabel(
            frame,
            text=page,
            font=ctk.CTkFont(size=30, weight="bold"),
        ).pack(
            anchor="w",
            padx=28,
            pady=(28, 10),
        )

        ctk.CTkLabel(
            frame,
            text=f"{page} module will be implemented in the next development step.",
        ).pack(
            anchor="w",
            padx=28,
            pady=28,
        )


if __name__ == "__main__":
    LibraryApp().mainloop()
