import tkinter as tk
from tkinter import messagebox, ttk
from db_manager import get_all_readers, add_reader, update_reader, delete_reader
import re

class ReaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reader Manager")
        self.current_readers = []
        self.previous_values = {}
        self.selected_mode = tk.StringVar(value="read")
        self.create_widgets()
        self.load_readers()

    def create_widgets(self):
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(padx=10, pady=5, anchor="w")

        # CRUD modes
        modes = [("Create", "create"), ("Read", "read"), ("Update", "update"), ("Delete", "delete")]
        for text, mode in modes:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.selected_mode, value=mode, command=self.on_mode_change)
            rb.pack(side=tk.LEFT, padx=5)

        form_frame = tk.Frame(self.root)
        form_frame.pack(padx=10, pady=10)

        labels = [
            "ID", "First Name*", "Last Name*", "Phone Number", "Email",
            "Birth Date (YYYY-MM-DD)", "Book Limit", "Num Taken Books", "Join Date"
        ]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1)
            self.entries[label] = entry
            entry.bind("<KeyRelease>", self.on_entry_change)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.action_btn = tk.Button(btn_frame, text="Execute", command=self.execute_action)
        self.action_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Refresh List", command=self.load_readers).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=labels, show='headings')
        for col in labels:
            self.tree.heading(col, text=col)
            # התאמת רוחב עמודות
            if col == "Email":
                self.tree.column(col, width=160)
            elif col == "Birth Date (YYYY-MM-DD)" or col == "Join Date":
                self.tree.column(col, width=120)
            else:
                self.tree.column(col, width=110)
        # תווית לספירת שורות מעל הטבלה, בצד שמאל צמוד
        self.row_count_label = tk.Label(self.root, text="Rows: 0")
        self.row_count_label.pack(anchor="nw", padx=10, pady=(0, 0))
        self.tree.pack(padx=10, pady=(10, 0), fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.on_mode_change()

    def on_mode_change(self):
        mode = self.selected_mode.get()
        self.clear_entries()

        if mode == "create":
            self.entries["ID"].config(state="disabled")
            for key in self.entries:
                if key != "ID":
                    self.entries[key].config(state="normal")
            self.action_btn.config(text="Add Reader")

        elif mode == "read":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["ID"].config(state="normal")
            self.action_btn.config(text="Search Reader")

        elif mode == "update":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["ID"].config(state="normal")
            self.action_btn.config(text="Load for Update")

        elif mode == "delete":
            for key in self.entries:
                self.entries[key].config(state="disabled")
            self.entries["ID"].config(state="normal")
            self.action_btn.config(text="Delete Reader")

    def on_entry_change(self, event):
        if self.selected_mode.get() == "read":
            for key in self.entries:
                if key != "ID":
                    self.entries[key].delete(0, tk.END)

    def load_readers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        readers = get_all_readers()
        self.current_readers = readers
        for r in readers:
            self.tree.insert("", "end", values=r)
        # עדכון תווית מספר שורות
        self.row_count_label.config(text=f"Rows: {len(readers)}")

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
                    if key != "ID":
                        self.entries[key].config(state="readonly")
            elif self.selected_mode.get() == "update":
                self.entries["ID"].config(state="readonly")

    def is_valid_phone(self, phone):
        if phone == "null" or phone == "":
            return True  # לא חובה למלא
        # תבניות תקינות: מספרים בלבד, 054-XXXXXXX, מספרים עם רווחים, +972...
        pattern = r"^(\+972 ?|0)([2-9]|5[0-9])[- ]?\d{3}[- ]?\d{4}$"
        return re.fullmatch(pattern, phone) is not None

    def is_valid_date(self, date_str):
        if date_str == "null" or date_str == "":
            return True  # לא חובה למלא
        try:
            import datetime
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def execute_action(self):
        mode = self.selected_mode.get()
        data = {key: self.entries[key].get().strip() for key in self.entries}

        try:
            if mode == "create":
                if not data["First Name*"] or not data["Last Name*"]:
                    messagebox.showerror("Error", "First Name and Last Name are required.")
                    return
                # בדיקת תקינות טלפון
                if not self.is_valid_phone(data["Phone Number"]):
                    messagebox.showerror("Error", "Phone number is invalid. Only digits, dashes, spaces, or +972 prefix are allowed.")
                    return
                # בדיקת תקינות תאריך
                if not self.is_valid_date(data["Birth Date (YYYY-MM-DD)"]):
                    messagebox.showerror("Error", "Birth date must be in format YYYY-MM-DD.")
                    return
                booklimit = int(data["Book Limit"]) if data["Book Limit"] else 5
                numtaken = int(data["Num Taken Books"]) if data["Num Taken Books"] else 0
                new_id = add_reader(
                    data["First Name*"], data["Last Name*"], data["Phone Number"] or None,
                    data["Email"] or None, data["Birth Date (YYYY-MM-DD)"] or None,
                    booklimit, numtaken
                )
                if new_id:
                    messagebox.showinfo("Success", f"Reader added with ID {new_id}")
                    self.load_readers()
                    self.clear_entries()
                else:
                    messagebox.showerror("Error", "Failed to add reader.")

            elif mode == "read":
                if data["ID"]:
                    found = [r for r in self.current_readers if str(r[0]) == data["ID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            if key != "ID":
                                self.entries[key].config(state="readonly")
                    else:
                        messagebox.showinfo("Not found", f"No reader with ID {data['ID']}")
                        self.clear_entries()

            elif mode == "update":
                if self.action_btn.cget("text") == "Load for Update":
                    found = [r for r in self.current_readers if str(r[0]) == data["ID"]]
                    if found:
                        self.fill_entries_from_tuple(found[0])
                        for key in self.entries:
                            self.entries[key].config(state="normal")
                        self.entries["ID"].config(state="readonly")
                        self.action_btn.config(text="Update Reader")
                    else:
                        messagebox.showinfo("Not found", f"No reader with ID {data['ID']}")
                        self.clear_entries()
                else:
                    label_to_param = {
                        "First Name*": "firstname",
                        "Last Name*": "lastname",
                        "Phone Number": "phonenumber",
                        "Email": "email",
                        "Book Limit": "booklimit",
                        "Num Taken Books": "numtakenbooks"
                    }
                    kwargs = {}
                    for key in label_to_param:
                        val = data[key]
                        param = label_to_param[key]
                        if val == "" or val == "null":
                            kwargs[param] = None
                        elif key in ["Book Limit", "Num Taken Books"]:
                            kwargs[param] = int(val)
                        else:
                            kwargs[param] = val
                    success = update_reader(int(data["ID"]), **kwargs)
                    if success:
                        messagebox.showinfo("Success", "Reader updated successfully.")
                        self.load_readers()
                        self.clear_entries()
                        self.action_btn.config(text="Load for Update")
                        self.entries["ID"].config(state="normal")
                    else:
                        messagebox.showerror("Error", "Failed to update reader.")

            elif mode == "delete":
                if not data["ID"]:
                    messagebox.showerror("Error", "Reader ID is required for delete.")
                    return
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Reader ID {data['ID']}?")
                if confirm:
                    success = delete_reader(int(data["ID"]))
                    if success:
                        messagebox.showinfo("Success", "Reader deleted successfully.")
                        self.load_readers()
                        self.clear_entries()
                    else:
                        messagebox.showerror("Error", f"Delete failed. No reader exists with ID: {data['ID']}")
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
        # אם במצב יצירה, ודא ש-ID נשאר חסום
        if self.selected_mode.get() == "create":
            self.entries["ID"].config(state="disabled")
        # אם במצב מחיקה, ודא שרק ID פתוח וכל השאר חסומים
        if self.selected_mode.get() == "delete":
            for key in self.entries:
                if key == "ID":
                    self.entries[key].config(state="normal")
                else:
                    self.entries[key].config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReaderGUI(root)
    root.geometry("1200x600")  # התאמת רוחב החלון לכל העמודות
    root.mainloop()
