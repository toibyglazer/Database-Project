import tkinter as tk
from tkinter import messagebox, ttk
from db_manager import get_all_orderitems, add_orderitem, update_orderitem, delete_orderitem

class OrderItemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OrderItem Manager")
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
            ("OrderID*", "OrderID"),
            ("BookLanguageID*", "BookLanguageID"),
            ("Quantity*", "Quantity")
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
            self.action_btn.config(text="Add OrderItem")
        elif mode == "read":
            self.action_btn.config(text="Search OrderItem")
        elif mode == "update":
            self.action_btn.config(text="Load for Update")
        elif mode == "delete":
            self.action_btn.config(text="Delete OrderItem")
            self.entries["Quantity"].config(state="readonly")

    def load_rows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = get_all_orderitems()
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
        mode = self.selected_mode.get()
        if mode == "update":
            self.entries["OrderID"].config(state="readonly")
            self.entries["BookLanguageID"].config(state="readonly")
        elif mode == "delete":
            self.entries["Quantity"].config(state="readonly")

    def execute_action(self):
        mode = self.selected_mode.get()
        data = {key: self.entries[key].get().strip() for key in self.entries}
        # בדיקת חובה ואינטגריים
        if mode == "create":
            for key in ["OrderID", "BookLanguageID", "Quantity"]:
                if not data[key]:
                    messagebox.showerror("Error", f"{key} is required.")
                    return
                if not data[key].isdigit():
                    messagebox.showerror("Error", f"{key} must be an integer.")
                    return
        elif mode == "update":
            if self.action_btn.cget("text") == "Load for Update":
                # בטעינה לא בודקים Quantity
                for key in ["OrderID", "BookLanguageID"]:
                    if not data[key]:
                        messagebox.showerror("Error", f"{key} is required.")
                        return
                    if not data[key].isdigit():
                        messagebox.showerror("Error", f"{key} must be an integer.")
                        return
            else:
                # כאן זה עדכון בפועל - בודקים גם Quantity
                for key in ["OrderID", "BookLanguageID"]:
                    if not data[key]:
                        messagebox.showerror("Error", f"{key} is required.")
                        return
                    if not data[key].isdigit():
                        messagebox.showerror("Error", f"{key} must be an integer.")
                        return
                if not data["Quantity"] or not data["Quantity"].isdigit():
                    messagebox.showerror("Error", "Quantity is required and must be an integer for update.")
                    return
        elif mode in ("read", "delete"):
            for key in ["OrderID", "BookLanguageID"]:
                if not data[key]:
                    messagebox.showerror("Error", f"{key} is required.")
                    return
                if not data[key].isdigit():
                    messagebox.showerror("Error", f"{key} must be an integer.")
                    return
        try:
            if mode == "create":
                try:
                    add_orderitem(int(data["OrderID"]), int(data["BookLanguageID"]), int(data["Quantity"]))
                except Exception as e:
                    err_msg = str(e)
                    if (
                        'violates foreign key constraint' in err_msg and
                        'orderitem_orderid_fkey' in err_msg
                    ):
                        messagebox.showerror("Error", "No such OrderID exists in Orders table.")
                    elif (
                        'violates foreign key constraint' in err_msg and
                        'orderitem_booklanguageid_fkey' in err_msg
                    ):
                        messagebox.showerror("Error", "No such BookLanguageID exists in BookstoreInventory table.")
                    else:
                        messagebox.showerror("Error", f"Exception occurred:\n{e}")
                    return
                messagebox.showinfo("Success", "OrderItem added successfully.")
                self.load_rows()
                self.clear_entries()
            elif mode == "read":
                found = [r for r in self.current_rows if str(r[0]) == data["OrderID"] and str(r[1]) == data["BookLanguageID"]]
                if found:
                    for i, key in enumerate(self.entries):
                        self.entries[key].config(state="normal")
                        self.entries[key].delete(0, tk.END)
                        self.entries[key].insert(0, str(found[0][i]))
                else:
                    messagebox.showinfo("Not found", f"No OrderItem with OrderID {data['OrderID']} and BookLanguageID {data['BookLanguageID']}")
                    self.clear_entries()
            elif mode == "update":
                if self.action_btn.cget("text") == "Load for Update":
                    found = [r for r in self.current_rows if str(r[0]) == data["OrderID"] and str(r[1]) == data["BookLanguageID"]]
                    if found:
                        # תמיד טוען את כל השדות כולל Quantity מהמסד
                        for i, key in enumerate(self.entries):
                            self.entries[key].config(state="normal")
                            self.entries[key].delete(0, tk.END)
                            self.entries[key].insert(0, str(found[0][i]))
                        self.entries["OrderID"].config(state="readonly")
                        self.entries["BookLanguageID"].config(state="readonly")
                        self.action_btn.config(text="Update OrderItem")
                    else:
                        messagebox.showinfo("Not found", f"No OrderItem with OrderID {data['OrderID']} and BookLanguageID {data['BookLanguageID']}")
                        self.clear_entries()
                else:
                    try:
                        result = update_orderitem(
                            int(data["OrderID"]),
                            int(data["BookLanguageID"]),
                            int(data["Quantity"])
                        )
                    except Exception as e:
                        err_msg = str(e)
                        if (
                            'violates foreign key constraint' in err_msg and
                            'orderitem_orderid_fkey' in err_msg
                        ):
                            messagebox.showerror("Error", "No such OrderID exists in Orders table.")
                        elif (
                            'violates foreign key constraint' in err_msg and
                            'orderitem_booklanguageid_fkey' in err_msg
                        ):
                            messagebox.showerror("Error", "No such BookLanguageID exists in BookstoreInventory table.")
                        else:
                            messagebox.showerror("Error", f"Exception occurred:\n{e}")
                        return
                    if result:
                        messagebox.showinfo("Success", "OrderItem updated successfully.")
                        self.load_rows()
                        self.clear_entries()
                        self.action_btn.config(text="Load for Update")
                        self.entries["OrderID"].config(state="normal")
                        self.entries["BookLanguageID"].config(state="normal")
                    else:
                        messagebox.showerror("Error", "Failed to update OrderItem. DB error or not found.")
            elif mode == "delete":
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete OrderItem with OrderID {data['OrderID']} and BookLanguageID {data['BookLanguageID']}?")
                if confirm:
                    try:
                        result = delete_orderitem(int(data["OrderID"]), int(data["BookLanguageID"]))
                        if result:
                            messagebox.showinfo("Success", "OrderItem deleted successfully.")
                            self.load_rows()
                            self.clear_entries()
                        else:
                            messagebox.showerror("Error", f"Delete failed. No such entry exists.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Exception occurred:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

    def fill_entries_from_tuple(self, tpl):
        keys = list(self.entries.keys())
        for i, val in enumerate(tpl):
            self.entries[keys[i]].config(state="normal")
            self.entries[keys[i]].delete(0, tk.END)
            self.entries[keys[i]].insert(0, "" if val is None else str(val))

    def clear_entries(self):
        for key, entry in self.entries.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderItemGUI(root)
    root.geometry("400x350")
    root.mainloop() 