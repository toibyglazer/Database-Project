import tkinter as tk
from tkinter import messagebox, ttk
from db_manager import get_all_librarycopies, add_librarycopy, update_librarycopy, delete_librarycopy

class LibraryCopyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LibraryCopy Manager")
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
            ("LibraryCopyID", "LibraryCopyID"),
            ("BookLanguageID*", "BookLanguageID"),
            ("CopySource*", "CopySource"),
            ("ShelfLocationID", "ShelfLocationID"),
            ("DonorID", "DonorID"),
            ("CopyCondition", "CopyCondition")
        ]
        self.entries = {}
        for i, (label, key) in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e")
            if key == "CopySource":
                entry = ttk.Combobox(form_frame, values=["Donated", "Purchased"], state="readonly", width=23)
                entry.grid(row=i, column=1)
            elif key == "CopyCondition":
                entry = ttk.Combobox(form_frame, values=["Excellent", "Good", "Fair"], state="readonly", width=23)
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
            self.entries["LibraryCopyID"].config(state="disabled")
            for key in ["BookLanguageID", "CopySource"]:
                self.entries[key].config(state="normal")
            self.entries["CopySource"].set("")
            self.entries["CopyCondition"].config(state="normal")
            self.entries["CopyCondition"].set("")
            self.entries["ShelfLocationID"].config(state="normal")
            self.entries["DonorID"].config(state="normal")
            self.action_btn.config(text="Add LibraryCopy")
        elif mode == "read":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["LibraryCopyID"].config(state="normal")
            self.action_btn.config(text="Search LibraryCopy")
        elif mode == "update":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["LibraryCopyID"].config(state="normal")
            self.action_btn.config(text="Load for Update")
        elif mode == "delete":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["LibraryCopyID"].config(state="normal")
            self.action_btn.config(text="Delete LibraryCopy")

    def load_rows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = get_all_librarycopies()
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
                if key in ["CopySource", "CopyCondition"]:
                    self.entries[key].set("" if values[i] is None else str(values[i]))
                else:
                    self.entries[key].delete(0, tk.END)
                    self.entries[key].insert(0, "" if values[i] is None else str(values[i]))
            if self.selected_mode.get() == "read":
                for key in self.entries:
                    if key != "LibraryCopyID":
                        self.entries[key].config(state="readonly")
            elif self.selected_mode.get() == "update":
                self.entries["LibraryCopyID"].config(state="readonly")

    def execute_action(self):
        mode = self.selected_mode.get()
        data = {key: self.entries[key].get().strip() for key in self.entries}
        # המרה לערכי None במקום מחרוזת ריקה
        for k in ["ShelfLocationID", "DonorID", "CopyCondition"]:
            if data[k] == "":
                data[k] = None
        # בדיקת תקינות אינטגריים
        for k in ["BookLanguageID", "ShelfLocationID", "DonorID"]:
            if data[k] is not None and data[k] != "":
                if not str(data[k]).isdigit():
                    messagebox.showerror("Error", f"{k} must be an integer.")
                    return
        try:
            if mode == "create":
                for key in ["BookLanguageID", "CopySource"]:
                    if not data[key]:
                        messagebox.showerror("Error", f"{key} is required.")
                        return
                if data["CopySource"] not in ["Donated", "Purchased"]:
                    messagebox.showerror("Error", "CopySource must be one of: Donated, Purchased.")
                    return
                try:
                    new_id = add_librarycopy(
                        int(data["BookLanguageID"]),
                        data["CopySource"],
                        int(data["ShelfLocationID"]) if data["ShelfLocationID"] is not None else None,
                        int(data["DonorID"]) if data["DonorID"] is not None else None,
                        data["CopyCondition"] if data["CopyCondition"] else None
                    )
                except Exception as e:
                    err_msg = str(e)
                    if (
                        'violates foreign key constraint' in err_msg and
                        'librarycopy_booklanguageid_fkey' in err_msg
                    ):
                        messagebox.showerror("Error", "No book with this language exists in BookLanguage table.")
                    else:
                        messagebox.showerror("Error", f"Exception occurred:\n{e}")
                    return
                if new_id:
                    messagebox.showinfo("Success", f"LibraryCopy added successfully with ID {new_id}.")
                    self.load_rows()
                    self.clear_entries()
                else:
                    messagebox.showerror("Error", "Failed to add LibraryCopy. DB error.")
            elif mode == "read":
                if data["LibraryCopyID"]:
                    found = [r for r in self.current_rows if str(r[0]) == data["LibraryCopyID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            if key != "LibraryCopyID":
                                self.entries[key].config(state="readonly")
                    else:
                        messagebox.showinfo("Not found", f"No LibraryCopy with ID {data['LibraryCopyID']}")
                        self.clear_entries()
            elif mode == "update":
                if self.action_btn.cget("text") == "Load for Update":
                    found = [r for r in self.current_rows if str(r[0]) == data["LibraryCopyID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            self.entries[key].config(state="normal")
                        self.entries["LibraryCopyID"].config(state="readonly")
                        self.action_btn.config(text="Update LibraryCopy")
                    else:
                        messagebox.showinfo("Not found", f"No LibraryCopy with ID {data['LibraryCopyID']}")
                        self.clear_entries()
                else:
                    for key in ["BookLanguageID", "CopySource"]:
                        if not data[key]:
                            messagebox.showerror("Error", f"{key} is required.")
                            return
                    if data["CopySource"] not in ["Donated", "Purchased"]:
                        messagebox.showerror("Error", "CopySource must be one of: Donated, Purchased.")
                        return
                    try:
                        result = update_librarycopy(
                            int(data["LibraryCopyID"]),
                            int(data["BookLanguageID"]) if data["BookLanguageID"] else None,
                            data["CopySource"] if data["CopySource"] else None,
                            int(data["ShelfLocationID"]) if data["ShelfLocationID"] else None,
                            int(data["DonorID"]) if data["DonorID"] else None,
                            data["CopyCondition"] if data["CopyCondition"] else None
                        )
                    except Exception as e:
                        err_msg = str(e)
                        if (
                            'violates foreign key constraint' in err_msg and
                            'librarycopy_booklanguageid_fkey' in err_msg
                        ):
                            messagebox.showerror("Error", "No book with this language exists in BookLanguage table.")
                        else:
                            messagebox.showerror("Error", f"Exception occurred:\n{e}")
                        return
                    if result:
                        messagebox.showinfo("Success", "LibraryCopy updated successfully.")
                        self.load_rows()
                        self.clear_entries()
                        self.action_btn.config(text="Load for Update")
                        self.entries["LibraryCopyID"].config(state="normal")
                    else:
                        messagebox.showerror("Error", "Failed to update LibraryCopy. DB error or not found.")
            elif mode == "delete":
                if not data["LibraryCopyID"]:
                    messagebox.showerror("Error", "LibraryCopyID is required for delete.")
                    return
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete LibraryCopyID {data['LibraryCopyID']}?")
                if confirm:
                    try:
                        result = delete_librarycopy(int(data["LibraryCopyID"]))
                        if result:
                            messagebox.showinfo("Success", "LibraryCopy deleted successfully.")
                            self.load_rows()
                            self.clear_entries()
                        else:
                            messagebox.showerror("Error", f"Delete failed. No LibraryCopy exists with ID {data['LibraryCopyID']}")
                    except Exception as e:
                        err_msg = str(e)
                        if (
                            'violates foreign key constraint' in err_msg and
                            (
                                'borrow_librarycopyid_fkey' in err_msg or
                                'borrowed_librarycopyid_fkey' in err_msg
                            )
                        ):
                            messagebox.showerror("Error", "Cannot delete this copy because it is currently borrowed.")
                        else:
                            messagebox.showerror("Error", f"Exception occurred:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

    def fill_entries_from_tuple(self, tpl):
        keys = list(self.entries.keys())
        for i, val in enumerate(tpl):
            self.entries[keys[i]].config(state="normal")
            if keys[i] in ["CopySource", "CopyCondition"]:
                self.entries[keys[i]].set("" if val is None else str(val))
            else:
                self.entries[keys[i]].delete(0, tk.END)
                self.entries[keys[i]].insert(0, "" if val is None else str(val))

    def clear_entries(self):
        for key, entry in self.entries.items():
            if key in ["CopySource", "CopyCondition"]:
                entry.set("")
            else:
                entry.config(state="normal")
                entry.delete(0, tk.END)
        if self.selected_mode.get() == "create":
            self.entries["LibraryCopyID"].config(state="disabled")
        if self.selected_mode.get() == "delete":
            for key in self.entries:
                if key == "LibraryCopyID":
                    self.entries[key].config(state="normal")
                else:
                    self.entries[key].config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryCopyGUI(root)
    root.geometry("800x450")
    root.mainloop() 