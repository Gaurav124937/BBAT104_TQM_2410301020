import customtkinter as ctk
from tkinter import messagebox
from services.database_admin import initialize_library_database, reset_library_database
from services.theme_manager import get_selected_theme,get_selected_appearance,set_theme,set_appearance,THEMES

class SettingsView(ctk.CTkFrame):
    def __init__(self,master,on_database_changed=None,on_appearance_changed=None):
        super().__init__(master,fg_color="transparent")
        self.on_database_changed=on_database_changed; self.on_appearance_changed=on_appearance_changed
        self.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(self,text="Settings",font=ctk.CTkFont(size=30,weight="bold")).grid(row=0,column=0,padx=30,pady=(30,8),sticky="w")
        card=ctk.CTkFrame(self,corner_radius=12); card.grid(row=1,column=0,sticky="ew",padx=30,pady=16); card.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(card,text="Appearance",font=ctk.CTkFont(size=20,weight="bold")).grid(row=0,column=0,padx=20,pady=(18,4),sticky="w")
        row=ctk.CTkFrame(card,fg_color="transparent"); row.grid(row=1,column=0,padx=20,pady=(0,20),sticky="w")
        ctk.CTkLabel(row,text="Mode",font=ctk.CTkFont(weight="bold")).pack(side="left",padx=(0,10))
        self.mode=ctk.CTkSegmentedButton(row,values=["System","Light","Dark"],command=self._mode); self.mode.set(get_selected_appearance()); self.mode.pack(side="left",padx=(0,25))
        ctk.CTkLabel(row,text="Theme",font=ctk.CTkFont(weight="bold")).pack(side="left",padx=(0,10))
        self.theme=ctk.CTkComboBox(row,values=list(THEMES.keys()),width=150,command=self._theme); self.theme.set(get_selected_theme()); self.theme.pack(side="left")
        db=ctk.CTkFrame(self,corner_radius=12); db.grid(row=2,column=0,sticky="ew",padx=30,pady=(12,24)); db.grid_columnconfigure(0,weight=1)
        ctk.CTkLabel(db,text="Database Management",font=ctk.CTkFont(size=20,weight="bold")).grid(row=0,column=0,padx=20,pady=(18,4),sticky="w")
        ctk.CTkButton(db,text="Initialize Database",width=190,command=self._init).grid(row=1,column=0,padx=20,pady=(10,8),sticky="w")
        ctk.CTkButton(db,text="Reset Database",width=160,command=self._reset).grid(row=2,column=0,padx=20,pady=(0,20),sticky="w")
    def _schedule_appearance_refresh(self):
        if self.on_appearance_changed:
            try:
                self.winfo_toplevel().focus_set()
            except Exception:
                pass
            self.after(500, self.on_appearance_changed)

    def _mode(self,v):
        try: set_appearance(v); self._schedule_appearance_refresh()
        except ValueError as e: messagebox.showerror("Appearance Error",str(e))
    def _theme(self,v):
        try: set_theme(v); self._schedule_appearance_refresh()
        except ValueError as e: messagebox.showerror("Theme Error",str(e))
    def _init(self):
        try: initialize_library_database(); messagebox.showinfo("Database Ready","Database initialization completed successfully.")
        except Exception as e: messagebox.showerror("Database Error",str(e))
    def _reset(self):
        if not messagebox.askyesno("Reset Database","This permanently deletes all library records. Continue?",icon="warning"): return
        try: reset_library_database()
        except Exception as e: messagebox.showerror("Reset Failed",str(e)); return
        self.on_database_changed and self.on_database_changed()
        messagebox.showinfo("Database Reset","Database reset successfully.")
