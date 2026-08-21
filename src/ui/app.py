import customtkinter as ctk
from database.schema import initialize_database
from ui.books_view import BooksView
from ui.dashboard_view import DashboardView
from ui.issue_view import IssueView
from ui.members_view import MembersView
from ui.return_view import ReturnView
from ui.settings_view import SettingsView

class LibraryApp(ctk.CTk):
    def __init__(self) -> None:
        initialize_database()
        super().__init__()
        self.title("Library Management System")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_content()
        self.show_page("Dashboard")

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        ctk.CTkLabel(sidebar, text="Library Manager",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(35, 30))
        for label in ["Dashboard", "Books", "Members", "Issue Book", "Return Book", "Records", "Calendar", "Settings"]:
            ctk.CTkButton(sidebar, text=label, height=40,
                          command=lambda page=label: self.show_page(page)
                          ).pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(sidebar, text="Q03: Improve Usability",
                     font=ctk.CTkFont(size=12)).pack(side="bottom", pady=20)

    def _build_content(self):
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, page: str):
        self._clear_content()
        views = {
            "Dashboard": DashboardView,
            "Books": BooksView,
            "Members": MembersView,
            "Issue Book": IssueView,
            "Return Book": ReturnView,
        }
        if page in views:
            view = views[page](self.content)
            view.grid(row=0, column=0, sticky="nsew")
            return
        if page == "Settings":
            view = SettingsView(self.content, on_database_changed=lambda: self.show_page("Dashboard"))
            view.grid(row=0, column=0, sticky="nsew")
            return

        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(frame, text=page,
                     font=ctk.CTkFont(size=30, weight="bold")).pack(anchor="w", padx=30, pady=(30, 10))
        ctk.CTkLabel(frame, text=f"{page} module will be implemented in the next development step.",
                     font=ctk.CTkFont(size=16)).pack(anchor="w", padx=30, pady=30)
