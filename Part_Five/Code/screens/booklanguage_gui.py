import tkinter as tk
from tkinter import messagebox, ttk
from db_manager import get_all_booklanguage, add_booklanguage, update_booklanguage, delete_booklanguage

class BookLanguageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BookLanguage Manager")
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
        labels = ["BookLanguageID", "BookID*", "LanguageID*"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1)
            self.entries[label] = entry

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.action_btn = tk.Button(btn_frame, text="Execute", command=self.execute_action)
        self.action_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh List", command=self.load_rows).pack(side=tk.LEFT, padx=5)

        # תווית לספירת שורות מעל הטבלה, בצד שמאל צמוד
        self.row_count_label = tk.Label(self.root, text="Rows: 0")
        self.row_count_label.pack(anchor="nw", padx=10, pady=(0, 0))

        self.tree = ttk.Treeview(self.root, columns=labels, show='headings')
        for col in labels:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(padx=10, pady=(10, 0), fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.on_mode_change()

    def on_mode_change(self):
        mode = self.selected_mode.get()
        self.clear_entries()
        if mode == "create":
            self.entries["BookLanguageID"].config(state="disabled")
            for key in self.entries:
                if key != "BookLanguageID":
                    self.entries[key].config(state="normal")
            self.action_btn.config(text="Add BookLanguage")
        elif mode == "read":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["BookLanguageID"].config(state="normal")
            self.action_btn.config(text="Search BookLanguage")
        elif mode == "update":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["BookLanguageID"].config(state="normal")
            self.action_btn.config(text="Load for Update")
        elif mode == "delete":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["BookLanguageID"].config(state="normal")
            self.action_btn.config(text="Delete BookLanguage")

    def load_rows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = get_all_booklanguage()
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
                    if key != "BookLanguageID":
                        self.entries[key].config(state="readonly")
            elif self.selected_mode.get() == "update":
                self.entries["BookLanguageID"].config(state="readonly")

    def execute_action(self):
        mode = self.selected_mode.get()
        data = {key: self.entries[key].get().strip() for key in self.entries}
        # מיפוי שמות שדות לטור DB
        db_map = {"BookLanguageID": "BookLanguageID", "BookID*": "BookID", "LanguageID*": "LanguageID"}
        try:
            if mode == "create":
                # BookID ו-LanguageID חייבים להיות מספרים
                if not data["BookID*"].isdigit():
                    messagebox.showerror("Error", "BookID must be a number.")
                    return
                if not data["LanguageID*"].isdigit():
                    messagebox.showerror("Error", "LanguageID must be a number.")
                    return
                try:
                    new_id = add_booklanguage(int(data["BookID*"]), int(data["LanguageID*"]))
                except Exception as e:
                    err_msg = str(e)
                    if "violates foreign key constraint" in err_msg:
                        messagebox.showerror("Error", "BookID or LanguageID does not exist in their tables.")
                    elif "duplicate key value violates unique constraint" in err_msg:
                        messagebox.showerror("Error", "This BookID-LanguageID pair already exists.")
                    else:
                        messagebox.showerror("Error", f"Exception occurred:\n{e}")
                    return
                if new_id:
                    messagebox.showinfo("Success", f"BookLanguage added successfully with ID {new_id}.")
                    self.load_rows()
                    self.clear_entries()
                else:
                    messagebox.showerror("Error", "Failed to add BookLanguage. DB error.")
            elif mode == "read":
                if data["BookLanguageID"]:
                    found = [r for r in self.current_rows if str(r[0]) == data["BookLanguageID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            if key != "BookLanguageID":
                                self.entries[key].config(state="readonly")
                    else:
                        messagebox.showinfo("Not found", f"No BookLanguage with ID {data['BookLanguageID']}")
                        self.clear_entries()
            elif mode == "update":
                if self.action_btn.cget("text") == "Load for Update":
                    found = [r for r in self.current_rows if str(r[0]) == data["BookLanguageID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            self.entries[key].config(state="normal")
                        self.entries["BookLanguageID"].config(state="readonly")
                        self.action_btn.config(text="Update BookLanguage")
                    else:
                        messagebox.showinfo("Not found", f"No BookLanguage with ID {data['BookLanguageID']}")
                        self.clear_entries()
                else:
                    # BookID ו-LanguageID חייבים להיות מספרים אם הוזנו
                    if data["BookID*"] and not data["BookID*"].isdigit():
                        messagebox.showerror("Error", "BookID must be a number.")
                        return
                    if data["LanguageID*"] and not data["LanguageID*"].isdigit():
                        messagebox.showerror("Error", "LanguageID must be a number.")
                        return
                    try:
                        result = update_booklanguage(
                            int(data["BookLanguageID"]),
                            int(data["BookID*"]) if data["BookID*"] else None,
                            int(data["LanguageID*"]) if data["LanguageID*"] else None
                        )
                    except Exception as e:
                        err_msg = str(e)
                        if "violates foreign key constraint" in err_msg:
                            messagebox.showerror("Error", "BookID or LanguageID does not exist in their tables.")
                        elif "duplicate key value violates unique constraint" in err_msg:
                            messagebox.showerror("Error", "This BookID-LanguageID pair already exists.")
                        else:
                            messagebox.showerror("Error", f"Exception occurred:\n{e}")
                        return
                    if result:
                        messagebox.showinfo("Success", "BookLanguage updated successfully.")
                        self.load_rows()
                        self.clear_entries()
                        self.action_btn.config(text="Load for Update")
                        self.entries["BookLanguageID"].config(state="normal")
                    else:
                        messagebox.showerror("Error", "Failed to update BookLanguage. DB error or not found.")
            elif mode == "delete":
                if not data["BookLanguageID"]:
                    messagebox.showerror("Error", "BookLanguageID is required for delete.")
                    return
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete BookLanguageID {data['BookLanguageID']}?")
                if confirm:
                    try:
                        result = delete_booklanguage(int(data["BookLanguageID"]))
                        if result:
                            messagebox.showinfo("Success", "BookLanguage deleted successfully.")
                            self.load_rows()
                            self.clear_entries()
                        else:
                            messagebox.showerror("Error", f"Delete failed. No BookLanguage exists with ID {data['BookLanguageID']}")
                    except Exception as e:
                        err_msg = str(e)
                        if "violates foreign key constraint" in err_msg:
                            messagebox.showerror("Error", "Cannot delete: This BookLanguageID is referenced in BookstoreInventory or LibraryCopy. Remove dependencies first.")
                        else:
                            messagebox.showerror("Error", f"Exception occurred:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

    def fill_entries_from_tuple(self, tpl):
        keys = list(self.entries.keys())
        for i, val in enumerate(tpl):
            self.entries[keys[i]].config(state="normal")
            self.entries[keys[i]].delete(0, tk.END)
            self.entries[keys[i]].insert(0, "null" if val is None else str(val))

    def clear_entries(self):
        for key, entry in self.entries.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)
        if self.selected_mode.get() == "create":
            self.entries["BookLanguageID"].config(state="disabled")
        if self.selected_mode.get() == "delete":
            for key in self.entries:
                if key == "BookLanguageID":
                    self.entries[key].config(state="normal")
                else:
                    self.entries[key].config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookLanguageGUI(root)
    root.geometry("500x400")
    root.mainloop() 