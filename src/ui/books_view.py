from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from services.book_service import (
    add_book,
    delete_book,
    get_book,
    get_categories,
    search_books,
    update_book,
)


class BooksView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.selected_book_id: int | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_toolbar()
        self._build_table()

        self.refresh_books()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 8))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Books Management",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text="+ Add Book",
            width=130,
            command=self._open_add_dialog,
        ).grid(row=0, column=1, padx=(10, 0))

    def _build_toolbar(self) -> None:
        toolbar = ctk.CTkFrame(self)
        toolbar.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 12))
        toolbar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search by title, author or ISBN",
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda _event: self.refresh_books())

        self.category_combo = ctk.CTkComboBox(
            toolbar,
            width=160,
            values=["All"],
            command=lambda _value: self.refresh_books(),
        )
        self.category_combo.set("All")
        self.category_combo.grid(row=0, column=1, padx=(0, 10), pady=10)

        self.availability_combo = ctk.CTkComboBox(
            toolbar,
            width=150,
            values=["All", "Available", "Unavailable"],
            command=lambda _value: self.refresh_books(),
        )
        self.availability_combo.set("All")
        self.availability_combo.grid(row=0, column=2, padx=(0, 10), pady=10)

        ctk.CTkButton(
            toolbar,
            text="Clear",
            width=90,
            command=self._clear_filters,
        ).grid(row=0, column=3, padx=(0, 10), pady=10)

        ctk.CTkButton(
            toolbar,
            text="Edit Selected",
            width=120,
            command=self._open_edit_dialog,
        ).grid(row=0, column=4, padx=(0, 10), pady=10)

        ctk.CTkButton(
            toolbar,
            text="Delete Selected",
            width=130,
            command=self._delete_selected,
        ).grid(row=0, column=5, padx=(0, 10), pady=10)

    def _build_table(self) -> None:
        frame = ctk.CTkFrame(self)
        frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        columns = (
            "id",
            "title",
            "author",
            "category",
            "isbn",
            "quantity",
            "available",
        )

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        headings = {
            "id": "ID",
            "title": "Title",
            "author": "Author",
            "category": "Category",
            "isbn": "ISBN",
            "quantity": "Qty",
            "available": "Available",
        }
        widths = {
            "id": 55,
            "title": 220,
            "author": 170,
            "category": 120,
            "isbn": 140,
            "quantity": 70,
            "available": 80,
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
            self.selected_book_id = None
            return

        values = self.tree.item(selection[0], "values")
        self.selected_book_id = int(values[0])

    def refresh_books(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = search_books(
            query=self.search_entry.get(),
            category=self.category_combo.get(),
            availability=self.availability_combo.get(),
        )

        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    row["book_id"],
                    row["title"],
                    row["author"],
                    row["category"],
                    row["isbn"] or "",
                    row["quantity"],
                    row["available_quantity"],
                ),
            )

        categories = ["All"] + get_categories()
        current = self.category_combo.get()
        self.category_combo.configure(values=categories)
        self.category_combo.set(current if current in categories else "All")

    def _clear_filters(self) -> None:
        self.search_entry.delete(0, "end")
        self.category_combo.set("All")
        self.availability_combo.set("All")
        self.refresh_books()

    def _open_add_dialog(self) -> None:
        BookDialog(self, title="Add Book", on_save=self._save_new_book).grab_set()

    def _open_edit_dialog(self) -> None:
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Please select a book first.")
            return

        book = get_book(self.selected_book_id)
        if book is None:
            messagebox.showerror("Error", "Book not found.")
            self.refresh_books()
            return

        BookDialog(
            self,
            title="Edit Book",
            book=book,
            on_save=self._save_existing_book,
        ).grab_set()

    def _save_new_book(self, data: dict) -> None:
        try:
            add_book(**data)
        except Exception as exc:
            messagebox.showerror("Unable to Add Book", str(exc))
            return

        self.refresh_books()
        messagebox.showinfo("Success", "Book added successfully.")

    def _save_existing_book(self, data: dict) -> None:
        try:
            update_book(
                self.selected_book_id,
                **data,
            )
        except Exception as exc:
            messagebox.showerror("Unable to Update Book", str(exc))
            return

        self.refresh_books()
        messagebox.showinfo("Success", "Book updated successfully.")

    def _delete_selected(self) -> None:
        if self.selected_book_id is None:
            messagebox.showwarning("Select Book", "Please select a book first.")
            return

        book = get_book(self.selected_book_id)
        if book is None:
            messagebox.showerror("Error", "Book not found.")
            self.refresh_books()
            return

        confirmed = messagebox.askyesno(
            "Delete Book",
            f"Delete '{book['title']}'?",
        )
        if not confirmed:
            return

        try:
            delete_book(self.selected_book_id)
        except Exception as exc:
            messagebox.showerror("Unable to Delete Book", str(exc))
            return

        self.selected_book_id = None
        self.refresh_books()
        messagebox.showinfo("Success", "Book deleted successfully.")


class BookDialog(ctk.CTkToplevel):
    def __init__(self, master, title: str, on_save, book=None):
        super().__init__(master)
        self.title(title)
        self.geometry("520x540")
        self.resizable(False, False)
        self.on_save = on_save
        self.book = book

        self.entries = {}

        self.grid_columnconfigure(1, weight=1)

        fields = [
            ("title", "Title"),
            ("author", "Author"),
            ("category", "Category"),
            ("isbn", "ISBN"),
            ("quantity", "Quantity"),
        ]

        for index, (key, label) in enumerate(fields):
            ctk.CTkLabel(self, text=label).grid(
                row=index,
                column=0,
                padx=25,
                pady=(20 if index == 0 else 10, 5),
                sticky="w",
            )

            entry = ctk.CTkEntry(self)
            entry.grid(
                row=index,
                column=1,
                padx=(5, 25),
                pady=(20 if index == 0 else 10, 5),
                sticky="ew",
            )
            self.entries[key] = entry

        if book:
            self.entries["title"].insert(0, book["title"])
            self.entries["author"].insert(0, book["author"])
            self.entries["category"].insert(0, book["category"])
            self.entries["isbn"].insert(0, book["isbn"] or "")
            self.entries["quantity"].insert(0, str(book["quantity"]))
        else:
            self.entries["quantity"].insert(0, "0")

        ctk.CTkButton(
            self,
            text="Save",
            command=self._save,
        ).grid(row=6, column=0, columnspan=2, padx=25, pady=25, sticky="ew")

        self.bind("<Return>", lambda _event: self._save())
        self.transient(master)

    def _save(self) -> None:
        try:
            quantity_text = self.entries["quantity"].get().strip()
            quantity = int(quantity_text)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")

            data = {
                "title": self.entries["title"].get(),
                "author": self.entries["author"].get(),
                "category": self.entries["category"].get(),
                "isbn": self.entries["isbn"].get(),
                "quantity": quantity,
            }

            self.on_save(data)
            self.destroy()
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
