import tkinter as tk
from tkinter import messagebox, ttk
from db_manager import get_all_borrowed, add_borrowed, delete_borrowed

class BorrowedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Borrowed Manager")
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
            ("Delete", "delete")
        ]
        for text, mode in modes:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.selected_mode, value=mode, command=self.on_mode_change)
            rb.pack(side=tk.LEFT, padx=5)

        form_frame = tk.Frame(self.root)
        form_frame.pack(padx=10, pady=10)
        labels = [
            ("BorrowNumber*", "BorrowNumber"),
            ("LibraryCopyID*", "LibraryCopyID")
        ]
        self.entries = {}
        for i, (label, key) in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e")
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
        for key in self.entries:
            self.entries[key].config(state="normal")
        if mode == "create":
            for widget in self.entries.values():
                widget.grid()
            self.action_btn.config(text="Add Borrowed", command=self.execute_action)
        elif mode == "read":
            for widget in self.entries.values():
                widget.grid()
            self.action_btn.config(text="Search Borrowed", command=self.execute_action)
        elif mode == "delete":
            for widget in self.entries.values():
                widget.grid()
            self.action_btn.config(text="Delete Borrowed", command=self.execute_action)

    def load_rows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = get_all_borrowed()
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
        for i, key in enumerate(self.entries):
            self.entries[key].config(state="normal")
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, "" if values[i] is None else str(values[i]))

    def execute_action(self):
        mode = self.selected_mode.get()
        data = {key: self.entries[key].get().strip() for key in self.entries}
        # בדיקת חובה ואינטגריים
        for key in self.entries:
            if not data[key]:
                messagebox.showerror("Error", f"{key} is required.")
                return
            if not data[key].isdigit():
                messagebox.showerror("Error", f"{key} must be an integer.")
                return
        try:
            if mode == "create":
                try:
                    add_borrowed(int(data["BorrowNumber"]), int(data["LibraryCopyID"]))
                except Exception as e:
                    err_msg = str(e)
                    if (
                        'violates foreign key constraint' in err_msg and
                        'borrowed_borrownumber_fkey' in err_msg
                    ):
                        messagebox.showerror("Error", "No such BorrowNumber exists in Borrow table.")
                    elif (
                        'violates foreign key constraint' in err_msg and
                        'borrowed_librarycopyid_fkey' in err_msg
                    ):
                        messagebox.showerror("Error", "No such LibraryCopyID exists in LibraryCopy table.")
                    else:
                        messagebox.showerror("Error", f"Exception occurred:\n{e}")
                    return
                messagebox.showinfo("Success", "Borrowed entry added successfully.")
                self.load_rows()
                self.clear_entries()
            elif mode == "read":
                found = [r for r in self.current_rows if str(r[0]) == data["BorrowNumber"] and str(r[1]) == data["LibraryCopyID"]]
                if found:
                    for i, key in enumerate(self.entries):
                        self.entries[key].config(state="normal")
                        self.entries[key].delete(0, tk.END)
                        self.entries[key].insert(0, str(found[0][i]))
                else:
                    messagebox.showinfo("Not found", f"No Borrowed entry with BorrowNumber {data['BorrowNumber']} and LibraryCopyID {data['LibraryCopyID']}")
                    self.clear_entries()
            elif mode == "delete":
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Borrowed entry with BorrowNumber {data['BorrowNumber']} and LibraryCopyID {data['LibraryCopyID']}?")
                if confirm:
                    try:
                        result = delete_borrowed(int(data["BorrowNumber"]), int(data["LibraryCopyID"]))
                        if result:
                            messagebox.showinfo("Success", "Borrowed entry deleted successfully.")
                            self.load_rows()
                            self.clear_entries()
                        else:
                            messagebox.showerror("Error", f"Delete failed. No such entry exists.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Exception occurred:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

    def clear_entries(self):
        for key, entry in self.entries.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BorrowedGUI(root)
    root.geometry("400x350")
    root.mainloop() 