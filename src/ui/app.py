import customtkinter as ctk
from database.schema import initialize_database

class LibraryApp(ctk.CTk):
    def __init__(self):
        initialize_database()
        super().__init__()
        self.title("Library Management System")
        self.geometry("1100x700")
        self.minsize(900, 600)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        ctk.CTkLabel(sidebar, text="Library Manager", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(35, 30))
        for label in ["Dashboard", "Books", "Members", "Issue Book", "Return Book", "Records", "Calendar", "Settings"]:
            ctk.CTkButton(sidebar, text=label, height=40, command=lambda name=label: self.show_page(name)).pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(sidebar, text="Q03: Improve Usability", font=ctk.CTkFont(size=12)).pack(side="bottom", pady=20)
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.page_title = ctk.CTkLabel(self.content, text="Dashboard", font=ctk.CTkFont(size=28, weight="bold"))
        self.page_title.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="w")
        self.info = ctk.CTkLabel(self.content, text="Base application foundation ready. Feature modules will be added in the next phase.", font=ctk.CTkFont(size=16), wraplength=750, justify="left")
        self.info.grid(row=1, column=0, padx=30, pady=30, sticky="nw")

    def show_page(self, name: str):
        self.page_title.configure(text=name)
        self.info.configure(text=f"{name} module placeholder. Implementation will be added next.")
