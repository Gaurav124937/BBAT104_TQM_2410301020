from __future__ import annotations

from tkinter import messagebox, ttk

import customtkinter as ctk

from services.member_service import (
    add_member,
    delete_member,
    get_courses,
    get_member,
    search_members,
    update_member,
)


class MembersView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.selected_member_id: int | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_toolbar()
        self._build_table()
        self.refresh_members()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 8))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Members Management",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text="+ Add Member",
            width=130,
            command=self._open_add_dialog,
        ).grid(row=0, column=1, padx=(10, 0))

    def _build_toolbar(self) -> None:
        toolbar = ctk.CTkFrame(self)
        toolbar.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 12))
        toolbar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search by name, phone, email or ID",
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda _event: self.refresh_members())

        self.course_combo = ctk.CTkComboBox(
            toolbar,
            width=170,
            values=["All"],
            command=lambda _value: self.refresh_members(),
        )
        self.course_combo.set("All")
        self.course_combo.grid(row=0, column=1, padx=(0, 10), pady=10)

        ctk.CTkButton(
            toolbar,
            text="Clear",
            width=90,
            command=self._clear_filters,
        ).grid(row=0, column=2, padx=(0, 10), pady=10)

        ctk.CTkButton(
            toolbar,
            text="Edit Selected",
            width=120,
            command=self._open_edit_dialog,
        ).grid(row=0, column=3, padx=(0, 10), pady=10)

        ctk.CTkButton(
            toolbar,
            text="Delete Selected",
            width=130,
            command=self._delete_selected,
        ).grid(row=0, column=4, padx=(0, 10), pady=10)

    def _build_table(self) -> None:
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        columns = ("id", "name", "course", "phone", "email")

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        headings = {
            "id": "ID",
            "name": "Name",
            "course": "Course",
            "phone": "Phone",
            "email": "Email",
        }
        widths = {
            "id": 60,
            "name": 220,
            "course": 180,
            "phone": 150,
            "email": 260,
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", lambda _event: self._open_edit_dialog())

    def _on_select(self, _event=None) -> None:
        selection = self.tree.selection()
        if not selection:
            self.selected_member_id = None
            return

        values = self.tree.item(selection[0], "values")
        self.selected_member_id = int(values[0])

    def refresh_members(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = search_members(
            query=self.search_entry.get(),
            course=self.course_combo.get(),
        )

        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    row["member_id"],
                    row["name"],
                    row["course"],
                    row["phone"] or "",
                    row["email"] or "",
                ),
            )

        courses = ["All"] + get_courses()
        current = self.course_combo.get()
        self.course_combo.configure(values=courses)
        self.course_combo.set(current if current in courses else "All")

    def _clear_filters(self) -> None:
        self.search_entry.delete(0, "end")
        self.course_combo.set("All")
        self.refresh_members()

    def _open_add_dialog(self) -> None:
        MemberDialog(
            self,
            title="Add Member",
            on_save=self._save_new_member,
        ).grab_set()

    def _open_edit_dialog(self) -> None:
        if self.selected_member_id is None:
            messagebox.showwarning("Select Member", "Please select a member first.")
            return

        member = get_member(self.selected_member_id)
        if member is None:
            messagebox.showerror("Error", "Member not found.")
            self.refresh_members()
            return

        MemberDialog(
            self,
            title="Edit Member",
            member=member,
            on_save=self._save_existing_member,
        ).grab_set()

    def _save_new_member(self, data: dict) -> None:
        try:
            add_member(**data)
        except Exception as exc:
            messagebox.showerror("Unable to Add Member", str(exc))
            return

        self.refresh_members()
        messagebox.showinfo("Success", "Member added successfully.")

    def _save_existing_member(self, data: dict) -> None:
        try:
            update_member(self.selected_member_id, **data)
        except Exception as exc:
            messagebox.showerror("Unable to Update Member", str(exc))
            return

        self.refresh_members()
        messagebox.showinfo("Success", "Member updated successfully.")

    def _delete_selected(self) -> None:
        if self.selected_member_id is None:
            messagebox.showwarning("Select Member", "Please select a member first.")
            return

        member = get_member(self.selected_member_id)
        if member is None:
            messagebox.showerror("Error", "Member not found.")
            self.refresh_members()
            return

        confirmed = messagebox.askyesno(
            "Delete Member",
            f"Delete '{member['name']}'?",
        )
        if not confirmed:
            return

        try:
            delete_member(self.selected_member_id)
        except Exception as exc:
            messagebox.showerror("Unable to Delete Member", str(exc))
            return

        self.selected_member_id = None
        self.refresh_members()
        messagebox.showinfo("Success", "Member deleted successfully.")


class MemberDialog(ctk.CTkToplevel):
    def __init__(self, master, title: str, on_save, member=None):
        super().__init__(master)
        self.title(title)
        self.geometry("520x500")
        self.resizable(False, False)

        self.on_save = on_save
        self.member = member
        self.entries = {}

        self.grid_columnconfigure(1, weight=1)

        fields = [
            ("name", "Name"),
            ("course", "Course"),
            ("phone", "Phone"),
            ("email", "Email"),
        ]

        for index, (key, label) in enumerate(fields):
            ctk.CTkLabel(self, text=label).grid(
                row=index,
                column=0,
                padx=25,
                pady=(25 if index == 0 else 12, 5),
                sticky="w",
            )

            entry = ctk.CTkEntry(self)
            entry.grid(
                row=index,
                column=1,
                padx=(5, 25),
                pady=(25 if index == 0 else 12, 5),
                sticky="ew",
            )
            self.entries[key] = entry

        if member:
            self.entries["name"].insert(0, member["name"])
            self.entries["course"].insert(0, member["course"])
            self.entries["phone"].insert(0, member["phone"] or "")
            self.entries["email"].insert(0, member["email"] or "")

        ctk.CTkButton(
            self,
            text="Save",
            command=self._save,
        ).grid(row=4, column=0, columnspan=2, padx=25, pady=30, sticky="ew")

        self.bind("<Return>", lambda _event: self._save())
        self.transient(master)

    def _save(self) -> None:
        data = {
            "name": self.entries["name"].get(),
            "course": self.entries["course"].get(),
            "phone": self.entries["phone"].get(),
            "email": self.entries["email"].get(),
        }

        try:
            self.on_save(data)
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Invalid Input", str(exc))
