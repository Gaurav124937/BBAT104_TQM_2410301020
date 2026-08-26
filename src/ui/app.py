import customtkinter as ctk
from database.schema import initialize_database
from services.theme_manager import initialize_theme_system,apply_ttk_theme
from ui.books_view import BooksView
from ui.calendar_view import CalendarView
from ui.dashboard_view import DashboardView
from ui.issue_view import IssueView
from ui.members_view import MembersView
from ui.return_view import ReturnView
from ui.records_view import RecordsView
from ui.settings_view import SettingsView

class LibraryApp(ctk.CTk):
    def __init__(self):
        initialize_database(); initialize_theme_system()
        super().__init__(); self.title("Library Management System"); self.geometry("1280x820"); self.minsize(900,650)
        apply_ttk_theme(); self.grid_columnconfigure(1,weight=1); self.grid_rowconfigure(0,weight=1); self.current_page="Dashboard"; self._build_shell(); self.show_page(self.current_page)
    def _build_shell(self):
        side=ctk.CTkFrame(self,width=210,corner_radius=0); side.grid(row=0,column=0,sticky="nsew"); side.grid_propagate(False)
        ctk.CTkLabel(side,text="Library Manager",font=ctk.CTkFont(size=21,weight="bold")).pack(pady=(28,26))
        for page in ("Dashboard","Books","Members","Issue Book","Return Book","Records","Calendar","Settings"):
            ctk.CTkButton(side,text=page,height=38,command=lambda p=page:self.show_page(p)).pack(fill="x",padx=18,pady=5)
        ctk.CTkLabel(side,text="Q03: Improve Usability",font=ctk.CTkFont(size=11)).pack(side="bottom",pady=18); self.sidebar=side
        self.content=ctk.CTkFrame(self,corner_radius=0); self.content.grid(row=0,column=1,sticky="nsew"); self.content.grid_columnconfigure(0,weight=1); self.content.grid_rowconfigure(0,weight=1)
    def _rebuild(self):
        # Keep the main Tk root alive. Rebuild only its child widgets so the
        # selected theme is applied everywhere without destroying the root.
        for widget in self.winfo_children():
            widget.destroy()

        self._build_shell()
        self.show_page(self.current_page)

    def show_page(self,page):
        self.current_page=page
        for w in self.content.winfo_children(): w.destroy()
        views={"Dashboard":DashboardView,"Books":BooksView,"Members":MembersView,"Issue Book":IssueView,"Return Book":ReturnView,"Records":RecordsView,"Calendar":CalendarView}
        if page in views:
            v=views[page](self.content); v.grid(row=0,column=0,sticky="nsew"); return
        if page=="Settings":
            v=SettingsView(self.content,on_database_changed=lambda:self.show_page("Dashboard"),on_appearance_changed=self._rebuild); v.grid(row=0,column=0,sticky="nsew"); return
        f=ctk.CTkFrame(self.content,fg_color="transparent"); f.grid(row=0,column=0,sticky="nsew")
        ctk.CTkLabel(f,text=page,font=ctk.CTkFont(size=30,weight="bold")).pack(anchor="w",padx=28,pady=(28,10))
        ctk.CTkLabel(f,text=f"{page} module will be implemented in the next development step.").pack(anchor="w",padx=28,pady=28)

if __name__=="__main__": LibraryApp().mainloop()
