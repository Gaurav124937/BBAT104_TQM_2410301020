from tkinter import ttk
import customtkinter as ctk
from services.records_service import search_records,get_record_summary

class RecordsView(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master,fg_color="transparent")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(3,weight=1)
        ctk.CTkLabel(self,text="Library Records",font=ctk.CTkFont(size=28,weight="bold")).grid(row=0,column=0,padx=24,pady=(22,4),sticky="w")
        ctk.CTkLabel(self,text="Unified history of issued, overdue and returned books").grid(row=1,column=0,padx=24,pady=(0,12),sticky="w")
        self._summary()
        self._filters()
        self._table()
        self.refresh()

    def _summary(self):
        f=ctk.CTkFrame(self,fg_color="transparent"); f.grid(row=2,column=0,padx=24,pady=(0,12),sticky="ew")
        for i in range(4): f.grid_columnconfigure(i,weight=1)
        self.cards={}
        for i,(k,t) in enumerate((("total","Total"),("active","Active"),("overdue","Overdue"),("returned","Returned"))):
            c=ctk.CTkFrame(f,corner_radius=10); c.grid(row=0,column=i,sticky="ew",padx=4)
            ctk.CTkLabel(c,text=t).pack(anchor="w",padx=12,pady=(9,1))
            v=ctk.CTkLabel(c,text="0",font=ctk.CTkFont(size=22,weight="bold")); v.pack(anchor="w",padx=12,pady=(0,9))
            self.cards[k]=v

    def _filters(self):
        f=ctk.CTkFrame(self); f.grid(row=3,column=0,sticky="new",padx=24,pady=(0,10)); f.grid_columnconfigure(0,weight=1)
        self.search=ctk.CTkEntry(f,placeholder_text="Search book, member, issue ID or return ID"); self.search.grid(row=0,column=0,sticky="ew",padx=10,pady=10)
        self.search.bind("<KeyRelease>",lambda _e:self._refresh_table())
        self.status=ctk.CTkComboBox(f,values=["All","Active","Overdue","Returned"],width=130,command=lambda _v:self._refresh_table()); self.status.set("All"); self.status.grid(row=0,column=1,padx=(0,8),pady=10)
        ctk.CTkButton(f,text="Refresh",width=90,command=self.refresh).grid(row=0,column=2,padx=(0,8),pady=10)
        ctk.CTkButton(f,text="Clear",width=80,command=self._clear).grid(row=0,column=3,padx=(0,10),pady=10)

    def _table(self):
        frame=ctk.CTkFrame(self); frame.grid(row=4,column=0,sticky="nsew",padx=24,pady=(0,24)); frame.grid_columnconfigure(0,weight=1); frame.grid_rowconfigure(0,weight=1)
        cols=("issue","book","member","issue_date","due_date","status","return","return_date")
        self.tree=ttk.Treeview(frame,columns=cols,show="headings")
        heads={"issue":"Issue ID","book":"Book","member":"Member","issue_date":"Issue Date","due_date":"Due Date","status":"Status","return":"Return ID","return_date":"Return Date"}
        widths={"issue":80,"book":240,"member":200,"issue_date":110,"due_date":110,"status":100,"return":85,"return_date":110}
        for c in cols: self.tree.heading(c,text=heads[c]); self.tree.column(c,width=widths[c],anchor="center",minwidth=70)
        sy=ttk.Scrollbar(frame,orient="vertical",command=self.tree.yview); sx=ttk.Scrollbar(frame,orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=sy.set,xscrollcommand=sx.set)
        self.tree.grid(row=0,column=0,sticky="nsew"); sy.grid(row=0,column=1,sticky="ns"); sx.grid(row=1,column=0,sticky="ew")

    def _clear(self):
        self.search.delete(0,"end"); self.status.set("All"); self._refresh_table()

    def _refresh_table(self):
        for x in self.tree.get_children(): self.tree.delete(x)
        for r in search_records(self.search.get(),self.status.get()):
            self.tree.insert("", "end", values=(r["issue_id"],r["book_title"],r["member_name"],r["issue_date"],r["due_date"],r["status"],r["return_id"] or "-",r["return_date"] or "-"))

    def refresh(self):
        s=get_record_summary()
        for k,v in s.items(): self.cards[k].configure(text=str(v))
        self._refresh_table()
