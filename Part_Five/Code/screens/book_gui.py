import tkinter as tk
from tkinter import messagebox, ttk
from db_manager import get_all_books, add_book, update_book, delete_book

class BookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Manager")
        self.current_rows = []
        self.selected_mode = tk.StringVar(value="read")
        self.create_widgets()
        self.load_rows()

    def create_widgets(self):
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(padx=10, pady=5, anchor="w")
        modes = [
            ("Create", "create"),
            ("Read", "read"),
            ("Update", "update"),
            ("Delete", "delete")
        ]
        for text, mode in modes:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.selected_mode, value=mode, command=self.on_mode_change)
            rb.pack(side=tk.LEFT, padx=5)

        form_frame = tk.Frame(self.root)
        form_frame.pack(padx=10, pady=10)
        labels = [
            ("BookID", "BookID"),
            ("Title*", "Title"),
            ("AuthorID*", "AuthorID"),
            ("AgeGroup*", "AgeGroup"),
            ("PublicationYear", "PublicationYear"),
            ("Publishing", "Publishing")
        ]
        self.entries = {}
        for i, (label, key) in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e")
            if key == "AgeGroup":
                entry = ttk.Combobox(form_frame, values=["Adults", "Teens", "Children"], state="readonly", width=23)
                entry.grid(row=i, column=1)
            else:
                entry = tk.Entry(form_frame, width=26)
                entry.grid(row=i, column=1)
            self.entries[key] = entry

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.action_btn = tk.Button(btn_frame, text="Execute", command=self.execute_action)
        self.action_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh List", command=self.load_rows).pack(side=tk.LEFT, padx=5)

        self.row_count_label = tk.Label(self.root, text="Rows: 0")
        self.row_count_label.pack(anchor="nw", padx=10, pady=(0, 0))

        self.tree = ttk.Treeview(self.root, columns=[k for _, k in labels], show='headings')
        for (label, key) in labels:
            self.tree.heading(key, text=label)
            self.tree.column(key, width=120)
        self.tree.pack(padx=10, pady=(10, 0), fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.on_mode_change()

    def on_mode_change(self):
        mode = self.selected_mode.get()
        self.clear_entries()
        if mode == "create":
            self.entries["BookID"].config(state="disabled")
            for key in ["Title", "AuthorID", "AgeGroup"]:
                self.entries[key].config(state="normal")
            self.entries["PublicationYear"].config(state="normal")
            self.entries["Publishing"].config(state="normal")
            self.action_btn.config(text="Add Book")
        elif mode == "read":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["BookID"].config(state="normal")
            self.action_btn.config(text="Search Book")
        elif mode == "update":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["BookID"].config(state="normal")
            self.action_btn.config(text="Load for Update")
        elif mode == "delete":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["BookID"].config(state="normal")
            self.action_btn.config(text="Delete Book")

    def load_rows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = get_all_books()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            return
        self.current_rows = rows
        for r in rows:
            self.tree.insert("", "end", values=r)
        self.row_count_label.config(text=f"Rows: {len(rows)}")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        if self.selected_mode.get() in ["read", "update"]:
            for i, key in enumerate(self.entries):
                self.entries[key].config(state="normal")
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, values[i])
            if self.selected_mode.get() == "read":
                for key in self.entries:
                    if key != "BookID":
                        self.entries[key].config(state="readonly")
            elif self.selected_mode.get() == "update":
                self.entries["BookID"].config(state="readonly")

    def execute_action(self):
        mode = self.selected_mode.get()
        data = {key: self.entries[key].get().strip() for key in self.entries}
        # המרה לערכי None במקום מחרוזת ריקה
        for k in ["PublicationYear", "Publishing"]:
            if data[k] == "":
                data[k] = None
        try:
            if mode == "create":
                self.entries["BookID"].config(state="disabled")
                for key in ["Title", "AuthorID", "AgeGroup"]:
                    self.entries[key].config(state="normal")
                self.entries["PublicationYear"].config(state="normal")
                self.entries["Publishing"].config(state="normal")
                self.entries["AgeGroup"].set("")
                self.action_btn.config(text="Add Book")
                for key in ["Title", "AuthorID", "AgeGroup"]:
                    if not data[key]:
                        messagebox.showerror("Error", f"{key} is required.")
                        return
                if data["AgeGroup"] not in ["Adults", "Teens", "Children"]:
                    messagebox.showerror("Error", "AgeGroup must be one of: Adults, Teens, Children.")
                    return
                # בדיקת תקינות PublicationYear
                if data["PublicationYear"] is not None and data["PublicationYear"] != "":
                    if not data["PublicationYear"].isdigit():
                        messagebox.showerror("Error", "PublicationYear must be an integer.")
                        return
                try:
                    new_id = add_book(
                        data["Title"],
                        int(data["AuthorID"]),
                        data["AgeGroup"],
                        int(data["PublicationYear"]) if data["PublicationYear"] is not None and data["PublicationYear"] != "" else None,
                        data["Publishing"] if data["Publishing"] is not None else None
                    )
                except Exception as e:
                    err_msg = str(e)
                    if (
                        'violates foreign key constraint' in err_msg and
                        'book_authorid_fkey' in err_msg
                    ):
                        messagebox.showerror("Error", "No author with this ID exists in the system.")
                    else:
                        messagebox.showerror("Error", f"Exception occurred:\n{e}")
                    return
                if new_id:
                    messagebox.showinfo("Success", f"Book added successfully with ID {new_id}.")
                    self.load_rows()
                    self.clear_entries()
                else:
                    messagebox.showerror("Error", "Failed to add Book. DB error.")
            elif mode == "read":
                if data["BookID"]:
                    found = [r for r in self.current_rows if str(r[0]) == data["BookID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            if key != "BookID":
                                self.entries[key].config(state="readonly")
                    else:
                        messagebox.showinfo("Not found", f"No Book with ID {data['BookID']}")
                        self.clear_entries()
            elif mode == "update":
                if self.action_btn.cget("text") == "Load for Update":
                    found = [r for r in self.current_rows if str(r[0]) == data["BookID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            self.entries[key].config(state="normal")
                        self.entries["BookID"].config(state="readonly")
                        self.action_btn.config(text="Update Book")
                    else:
                        messagebox.showinfo("Not found", f"No Book with ID {data['BookID']}")
                        self.clear_entries()
                else:
                    for key in ["Title", "AuthorID", "AgeGroup"]:
                        if not data[key]:
                            messagebox.showerror("Error", f"{key} is required.")
                            return
                    if data["AgeGroup"] not in ["Adults", "Teens", "Children"]:
                        messagebox.showerror("Error", "AgeGroup must be one of: Adults, Teens, Children.")
                        return
                    # בדיקת תקינות PublicationYear
                    if data["PublicationYear"] is not None and data["PublicationYear"] != "":
                        if not data["PublicationYear"].isdigit():
                            messagebox.showerror("Error", "PublicationYear must be an integer.")
                            return
                    try:
                        result = update_book(
                            int(data["BookID"]),
                            data["Title"] if data["Title"] else None,
                            int(data["AuthorID"]) if data["AuthorID"] else None,
                            data["AgeGroup"] if data["AgeGroup"] else None,
                            int(data["PublicationYear"]) if data["PublicationYear"] is not None and data["PublicationYear"] != "" else None,
                            data["Publishing"] if data["Publishing"] is not None else None
                        )
                    except Exception as e:
                        err_msg = str(e)
                        if (
                            'violates foreign key constraint' in err_msg and
                            'book_authorid_fkey' in err_msg
                        ):
                            messagebox.showerror("Error", "No author with this ID exists in the system.")
                        else:
                            messagebox.showerror("Error", f"Exception occurred:\n{e}")
                        return
                    if result:
                        messagebox.showinfo("Success", "Book updated successfully.")
                        self.load_rows()
                        self.clear_entries()
                        self.action_btn.config(text="Load for Update")
                        self.entries["BookID"].config(state="normal")
                    else:
                        messagebox.showerror("Error", "Failed to update Book. DB error or not found.")
            elif mode == "delete":
                for key in self.entries:
                    self.entries[key].config(state="disabled")
                self.entries["BookID"].config(state="normal")
                self.entries["AgeGroup"].config(state="readonly")
                self.entries["AgeGroup"].set("")
                self.action_btn.config(text="Delete Book")
                if not data["BookID"]:
                    messagebox.showerror("Error", "BookID is required for delete.")
                    return
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete BookID {data['BookID']}?")
                if confirm:
                    try:
                        result = delete_book(int(data["BookID"]))
                        if result:
                            messagebox.showinfo("Success", "Book deleted successfully.")
                            self.load_rows()
                            self.clear_entries()
                        else:
                            messagebox.showerror("Error", f"Delete failed. No Book exists with ID {data['BookID']}")
                    except Exception as e:
                        err_msg = str(e)
                        if (
                            'violates foreign key constraint' in err_msg and
                            'booklanguage_bookid_fkey' in err_msg
                        ):
                            messagebox.showerror("Error", "Cannot delete this book because there are entries in the BookLanguage table that depend on it.")
                        else:
                            messagebox.showerror("Error", f"Exception occurred:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

    def fill_entries_from_tuple(self, tpl):
        keys = list(self.entries.keys())
        for i, val in enumerate(tpl):
            self.entries[keys[i]].config(state="normal")
            if keys[i] == "AgeGroup":
                self.entries[keys[i]].set("" if val is None else str(val))
            else:
                self.entries[keys[i]].delete(0, tk.END)
                self.entries[keys[i]].insert(0, "" if val is None else str(val))

    def clear_entries(self):
        for key, entry in self.entries.items():
            if key == "AgeGroup":
                entry.set("")
            else:
                entry.config(state="normal")
                entry.delete(0, tk.END)
        if self.selected_mode.get() == "create":
            self.entries["BookID"].config(state="disabled")
        if self.selected_mode.get() == "delete":
            for key in self.entries:
                if key == "BookID":
                    self.entries[key].config(state="normal")
                elif key == "AgeGroup":
                    self.entries[key].config(state="readonly")
                    self.entries[key].set("")
                else:
                    self.entries[key].config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookGUI(root)
    root.geometry("700x450")
    root.mainloop() 