import tkinter as tk
from screens.reader_gui import ReaderGUI
from screens.bookstoreinventory_gui import BookstoreInventoryGUI
from screens.booklanguage_gui import BookLanguageGUI
from screens.language_gui import LanguageGUI
from screens.book_gui import BookGUI
from screens.librarycopy_gui import LibraryCopyGUI
from screens.borrow_gui import BorrowGUI
from screens.orderitem_gui import OrderItemGUI
from screens.borrowed_gui import BorrowedGUI
from db_manager import get_all_available_copies
from tkinter import ttk, messagebox
from db_manager import check_book_availability_db
from db_manager import get_book_borrowers_db
from db_manager import get_book_copy_count_db
from db_manager import get_top_selling_books_db
from db_manager import get_available_copies_db
from db_manager import get_current_borrowers_db
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from db_manager import get_bookstore_analytics_db, get_library_analytics_db
import numpy as np

def open_reader_manager():
    top = tk.Toplevel()
    app = ReaderGUI(top)
    top.geometry("1050x600")
    top.title("Reader Manager")

def open_bookstoreinventory_manager():
    top = tk.Toplevel()
    app = BookstoreInventoryGUI(top)
    top.geometry("600x400")
    top.title("Bookstore Inventory Manager")

def open_booklanguage_manager():
    top = tk.Toplevel()
    app = BookLanguageGUI(top)
    top.geometry("500x400")
    top.title("BookLanguage Manager")

def open_language_manager():
    top = tk.Toplevel()
    app = LanguageGUI(top)
    top.geometry("500x400")
    top.title("Language Manager")

def open_book_manager():
    top = tk.Toplevel()
    app = BookGUI(top)
    top.geometry("700x450")
    top.title("Book Manager")

def open_librarycopy_manager():
    top = tk.Toplevel()
    app = LibraryCopyGUI(top)
    top.geometry("800x450")
    top.title("LibraryCopy Manager")

def open_borrow_manager():
    top = tk.Toplevel()
    app = BorrowGUI(top)
    top.geometry("800x450")
    top.title("Borrow Manager")

def open_borrowed_manager():
    top = tk.Toplevel()
    app = BorrowedGUI(top)
    top.geometry("400x350")
    top.title("Borrowed Manager")

def open_orders_manager():
    top = tk.Toplevel()
    from screens.orders_gui import OrdersGUI
    app = OrdersGUI(top)
    top.geometry("400x350")
    top.title("Orders Manager")

def open_table_window(gui_class, title):
    top = tk.Toplevel()
    app = gui_class(top)
    top.geometry("400x350")
    top.title(title)

def open_available_copies_window():
    top = tk.Toplevel()
    top.geometry("950x500")
    top.title("עותקים זמינים בספריה")
    desc_frame = tk.LabelFrame(top, text="הסבר הפונקציה", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    desc = ("פונקציה זו מציגה את כל העותקים הפיזיים הזמינים בספריה (שאינם מושאלים כרגע), כולל פרטי ספר, שפה, מצב, ומיקום מדף.\n"
            "ניתן לסנן לפי מזהה ספר (BookID) באמצעות השדה למטה.")
    label = tk.Label(desc_frame, text=desc, wraplength=900, justify="right")
    label.pack()
    input_frame = tk.Frame(top)
    input_frame.pack(pady=5)
    tk.Label(input_frame, text="BookID (לא חובה):").pack(side=tk.LEFT)
    bookid_var = tk.StringVar()
    bookid_entry = tk.Entry(input_frame, textvariable=bookid_var, width=10)
    bookid_entry.pack(side=tk.LEFT, padx=5)
    check_btn = tk.Button(input_frame, text="בדוק", width=10)
    check_btn.pack(side=tk.LEFT, padx=10)
    row_count_label = tk.Label(top, text="מספר רשומות: 0", font=("Arial", 12))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    columns = ["Book ID", "Title", "Library Copy ID", "Language Name", "Copy Condition", "Shelf Number", "Floor", "Row Number"]
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110)
    tree.pack(fill="both", expand=True)
    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        bookid = bookid_var.get().strip()
        if bookid and not bookid.isdigit():
            row_count_label.config(text="BookID חייב להיות מספר שלם או ריק.", fg="red")
            return
        try:
            rows = get_available_copies_db(int(bookid) if bookid else None)
            for row in rows:
                tree.insert("", "end", values=row)
            row_count_label.config(text=f"מספר רשומות: {len(rows)}", fg="black")
        except Exception as e:
            row_count_label.config(text=f"שגיאה: {e}", fg="red")
    check_btn.config(command=load_data)
    load_data()

def open_book_borrowers_window():
    top = tk.Toplevel()
    top.geometry("900x400")
    top.title("משאילים נוכחיים לספר מסוים")
    desc_frame = tk.LabelFrame(top, text="הסבר הפונקציה", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    desc = ("פונקציה זו מציגה את כל המשאילים הנוכחיים של ספר מסוים בספריה (עותקים שמושאלים כרגע).\n"
            "יש להזין מזהה ספר (BookID) וללחוץ על 'בדוק'. התוצאה תכלול: פרטי עותק, פרטי קורא, תאריכי השאלה, מספר ימי איחור (אם יש).\n")
    label = tk.Label(desc_frame, text=desc, wraplength=850, justify="right")
    label.pack()
    input_frame = tk.Frame(top)
    input_frame.pack(pady=5)
    tk.Label(input_frame, text="BookID:").pack(side=tk.LEFT)
    bookid_var = tk.StringVar()
    bookid_entry = tk.Entry(input_frame, textvariable=bookid_var, width=10)
    bookid_entry.pack(side=tk.LEFT, padx=5)
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    columns = [
        "Borrow Number", "Library Copy ID", "Book Title", "Language Name", "Reader ID", "Reader Full Name",
        "Phone", "Email", "Borrow Date", "Expected Return Date", "Days Overdue"
    ]
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110)
    tree.pack(fill="both", expand=True)
    def check_borrowers():
        for row in tree.get_children():
            tree.delete(row)
        bookid = bookid_var.get().strip()
        if not bookid:
            messagebox.showerror("שגיאה", "יש להזין מזהה ספר (BookID)")
            return
        if not bookid.isdigit():
            messagebox.showerror("שגיאה", "BookID חייב להיות מספר שלם")
            return
        try:
            rows = get_book_borrowers_db(int(bookid))
            if not rows:
                messagebox.showinfo("אין משאילים", f"אין משאילים נוכחיים לספר {bookid}.")
                return
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            msg = str(e)
            if 'not found' in msg:
                messagebox.showerror("שגיאה", f"ספר עם מזהה {bookid} לא נמצא.")
            else:
                messagebox.showerror("שגיאה", f"שגיאה:\n{e}")
    check_btn = tk.Button(input_frame, text="בדוק", command=check_borrowers)
    check_btn.pack(side=tk.LEFT, padx=10)

def open_book_copy_count_window():
    top = tk.Toplevel()
    top.geometry("400x250")
    top.title("ספירת עותקים לספר מסוים")
    desc_frame = tk.LabelFrame(top, text="הסבר הפונקציה", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    desc = ("פונקציה זו מציגה את מספר העותקים הפיזיים של ספר מסוים בספריה (ללא תלות בשפה).\n"
            "יש להזין מזהה ספר (BookID) וללחוץ על 'בדוק'.")
    label = tk.Label(desc_frame, text=desc, wraplength=350, justify="right")
    label.pack()
    input_frame = tk.Frame(top)
    input_frame.pack(pady=10)
    tk.Label(input_frame, text="BookID:").pack(side=tk.LEFT)
    bookid_var = tk.StringVar()
    bookid_entry = tk.Entry(input_frame, textvariable=bookid_var, width=10)
    bookid_entry.pack(side=tk.LEFT, padx=5)
    result_frame = tk.LabelFrame(top, text="מספר עותקים בספריה", padx=10, pady=10)
    result_frame.pack(pady=15, padx=10, fill="x")
    result_label = tk.Label(result_frame, text="")
    result_label.pack()
    def check_count():
        bookid = bookid_var.get().strip()
        if not bookid or not bookid.isdigit():
            result_label.config(text="יש להזין BookID חוקי (מספר שלם)", fg="red")
            return
        try:
            rows = get_book_copy_count_db(int(bookid))
            if not rows or rows[0][1] == 0:
                result_label.config(text=f"לא נמצאו עותקים לספר {bookid}.", fg="red")
            else:
                result_label.config(text=f"לספר {bookid} יש {rows[0][1]} עותקים בספריה.", fg="black")
        except Exception as e:
            result_label.config(text=f"שגיאה: {e}", fg="red")
    check_btn = tk.Button(input_frame, text="בדוק", command=check_count)
    check_btn.pack(side=tk.LEFT, padx=10)

def open_top_selling_books_window():
    top = tk.Toplevel()
    top.geometry("900x400")
    top.title("הספרים הנמכרים ביותר")
    desc_frame = tk.LabelFrame(top, text="הסבר הפונקציה", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    desc = ("פונקציה זו מציגה את 10 הספרים הנמכרים ביותר במערכת, כולל כמות עותקים שנמכרו והכנסה כוללת.\n"
            "הנתונים מוצגים לפי מהדורה (BookLanguageID) וסופר.")
    label = tk.Label(desc_frame, text=desc, wraplength=850, justify="right")
    label.pack()
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    columns = [
        "Rank Position", "BookLanguage ID", "Book Title", "Author Name", "Total Copies Sold", "Total Revenue"
    ]
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)
    tree.pack(fill="both", expand=True)
    try:
        rows = get_top_selling_books_db()
        if not rows:
            tk.Label(result_frame, text="לא נמצאו נתוני מכירות.", fg="red").pack()
        else:
            for row in rows:
                tree.insert("", "end", values=row)
    except Exception as e:
        tk.Label(result_frame, text=f"שגיאה: {e}", fg="red").pack()

def open_current_borrowers_window():
    top = tk.Toplevel()
    top.geometry("1100x500")
    top.title("השאלות פעילות בספריה")
    desc_frame = tk.LabelFrame(top, text="הסבר הפונקציה", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    desc = ("פונקציה זו מציגה את כל ההשאלות הפעילות בספריה (כל המשאילים שטרם החזירו ספרים).\n"
            "ניתן לסנן לפי מזהה ספר (BookID) באמצעות השדה למטה.")
    label = tk.Label(desc_frame, text=desc, wraplength=1000, justify="right")
    label.pack()
    input_frame = tk.Frame(top)
    input_frame.pack(pady=5)
    tk.Label(input_frame, text="BookID (לא חובה):").pack(side=tk.LEFT)
    bookid_var = tk.StringVar()
    bookid_entry = tk.Entry(input_frame, textvariable=bookid_var, width=10)
    bookid_entry.pack(side=tk.LEFT, padx=5)
    check_btn = tk.Button(input_frame, text="בדוק", width=10)
    check_btn.pack(side=tk.LEFT, padx=10)
    row_count_label = tk.Label(top, text="מספר רשומות: 0", font=("Arial", 12))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    columns = [
        "Borrow Number", "Reader ID", "Reader Full Name", "Email", "Phone", "Borrow Date", "Expected Return Date", "Days Overdue"
    ]
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)
    tree.pack(fill="both", expand=True)
    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        bookid = bookid_var.get().strip()
        if bookid and not bookid.isdigit():
            row_count_label.config(text="BookID חייב להיות מספר שלם או ריק.", fg="red")
            return
        try:
            rows = get_current_borrowers_db(int(bookid) if bookid else None)
            for row in rows:
                # אם אין איחור, הצג ריק
                row_disp = list(row)
                if row_disp[-1] is None or row_disp[-1] == 0:
                    row_disp[-1] = ""
                tree.insert("", "end", values=row_disp)
            row_count_label.config(text=f"מספר רשומות: {len(rows)}", fg="black")
        except Exception as e:
            row_count_label.config(text=f"שגיאה: {e}", fg="red")
    check_btn.config(command=load_data)
    load_data()

def open_books_by_genre_age_window():
    genres = [
        "ALL", "Fiction", "Non-Fiction", "Fantasy", "Mystery", "Science Fiction", "Biography", "Romance", "Thriller", "Horror", "Historical Fiction", "Young Adult", "Children's", "Adventure", "Poetry", "Drama", "Satire", "Self-Help", "Memoir", "Travel", "Cookbook", "Art", "Philosophy", "Psychology", "History", "Science", "Technology", "Business", "Economics", "Politics", "Religion", "Sports", "Music", "Comics", "Graphic Novel", "Dystopian", "Paranormal", "Mythology", "Fairy Tale", "Western", "Crime", "Detective", "Suspense", "Action", "Comedy", "Short Story", "Essay", "Reference", "Academic", "Classic", "Literary Fiction"
    ]
    age_groups = ["ALL", "Adults", "Teens", "Children"]
    columns = [
        "bookid", "book_name", "author_name", "agegroup", "genre", "publicationyear", "publishing", "available_languages", "languages_list", "bookstore_price", "bookstore_stock", "library_copies", "excellent_copies"
    ]
    headers = [
        "BookID", "Book Name", "Author Name", "Age Group", "Genre", "Publication Year", "Publishing", "# Languages", "Languages", "Bookstore Price", "Bookstore Stock", "Library Copies", "Excellent Copies"
    ]
    win_width = 850
    win_height = 400
    top = tk.Toplevel()
    top.title("חיפוש ספרים לפי ז'אנר וקבוצת גיל")
    top.geometry(f"{win_width}x{win_height}")
    desc = (
        "מאפשר חיפוש ספרים לפי ז'אנר וקבוצת גיל, כולל זמינות בחנות ובספריה. "
        "ניתן לבחור ז'אנר וקבוצת גיל, או להציג את כל הספרים."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר השאילתא", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=900, justify="right").pack(fill="x", padx=4, pady=2)
    # --- Filters ---
    filter_frame = tk.Frame(top)
    filter_frame.pack(pady=2)
    tk.Label(filter_frame, text="ז'אנר:").pack(side=tk.RIGHT, padx=4)
    genre_var = tk.StringVar(value="ALL")
    genre_combo = ttk.Combobox(filter_frame, textvariable=genre_var, values=genres, width=18, state="readonly")
    genre_combo.pack(side=tk.RIGHT, padx=4)
    tk.Label(filter_frame, text="קבוצת גיל:").pack(side=tk.RIGHT, padx=4)
    age_var = tk.StringVar(value="ALL")
    age_combo = ttk.Combobox(filter_frame, textvariable=age_var, values=age_groups, width=10, state="readonly")
    age_combo.pack(side=tk.RIGHT, padx=4)
    def load_data():
        genre = genre_var.get() if genre_var.get() != "ALL" else None
        age = age_var.get() if age_var.get() != "ALL" else None
        from db_manager import get_books_by_genre_and_age_group
        rows = get_books_by_genre_and_age_group(genre, age)
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", "end", values=[row.get(c, "") for c in columns])
        row_count_label.config(text=f"Rows: {len(rows)}")
    search_btn = tk.Button(filter_frame, text="חפש", command=load_data)
    search_btn.pack(side=tk.RIGHT, padx=8)
    # --- Table ---
    row_count_label = tk.Label(top, text="Rows: 0", font=("Arial", 9))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=8)
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)
        tree.column(col, width=110)
    tree.pack(fill="both", expand=True)
    # Load all books by default
    load_data()

root = tk.Tk()
root.title("Main Window")
root.geometry("1200x700")  # הגדלת חלון ראשי
root.minsize(1200, 700)

# אזור CRUD
crud_frame = tk.LabelFrame(root, text="ניהול טבלאות CRUD", padx=10, pady=10)
crud_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

btn = tk.Button(crud_frame, text="Show Readers", command=open_reader_manager)
btn.pack(pady=10, fill=tk.X)
btn2 = tk.Button(crud_frame, text="Show BookstoreInventory", command=open_bookstoreinventory_manager)
btn2.pack(pady=10, fill=tk.X)
btn3 = tk.Button(crud_frame, text="Show BookLanguage", bg="yellow", command=open_booklanguage_manager)
btn3.pack(pady=10, fill=tk.X)
btn4 = tk.Button(crud_frame, text="Show Language", command=open_language_manager)
btn4.pack(pady=10, fill=tk.X)
btn5 = tk.Button(crud_frame, text="Show Book", command=open_book_manager)
btn5.pack(pady=10, fill=tk.X)
btn6 = tk.Button(crud_frame, text="Show LibraryCopy", command=open_librarycopy_manager)
btn6.pack(pady=10, fill=tk.X)
btn7 = tk.Button(crud_frame, text="Show Borrow", command=open_borrow_manager)
btn7.pack(pady=10, fill=tk.X)
btn8 = tk.Button(crud_frame, text="Show Borrowed", command=open_borrowed_manager, bg="yellow")
btn8.pack(pady=10, fill=tk.X)
btn9 = tk.Button(crud_frame, text="Show Orders", command=open_orders_manager)
btn9.pack(pady=10, fill=tk.X)
orderitem_btn = tk.Button(crud_frame, text="OrderItem", bg="yellow", command=lambda: open_table_window(OrderItemGUI, "OrderItem"))
orderitem_btn.pack(pady=10, fill=tk.X)

# אזור פונקציות מידע
functions_frame = tk.LabelFrame(root, text="פונקציות מידע", padx=10, pady=10)
functions_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

func1_btn = tk.Button(functions_frame, text="הצג עותקים זמינים בספריה", command=open_available_copies_window)
func1_btn.pack(pady=10, fill=tk.X)
func2_btn = tk.Button(functions_frame, text="הצג השאלות פעילות בספריה", command=open_current_borrowers_window)
func2_btn.pack(pady=10, fill=tk.X)
func3_btn = tk.Button(functions_frame, text="ספירת עותקים לכל ספר", command=open_book_copy_count_window)
func3_btn.pack(pady=10, fill=tk.X)
func4_btn = tk.Button(functions_frame, text="הצג את הספרים הנמכרים ביותר", command=open_top_selling_books_window)
func4_btn.pack(pady=10, fill=tk.X)

# --- סטטיסטיקות במסגרת נפרדת ---
stats_frame = tk.LabelFrame(functions_frame, text="סטטיסטיקות", padx=10, pady=10)
stats_frame.pack(pady=(20, 0), fill=tk.X)

stats_btn1 = tk.Button(stats_frame, text="סטטיסטיקות חנות הספרים", command=lambda: open_bookstore_analytics_window())
stats_btn1.pack(pady=5, fill=tk.X)

stats_btn2 = tk.Button(stats_frame, text="סטטיסטיקות הספריה", command=lambda: open_library_analytics_window())
stats_btn2.pack(pady=5, fill=tk.X)

# --- פונקציה לחלון תוצאות השאילתה ---
def open_low_stock_query_window():
    columns = [
        "bookid", "book_name", "author_name", "author_nationality", "language", "stock_quantity", "price", "genre", "total_sold"
    ]
    win_width = len(columns) * 120 + 60
    win_height = 350
    top = tk.Toplevel()
    top.title("מלאי נמוך בחנות הספרים")
    top.geometry(f"{win_width}x{win_height}")
    desc = (
        "מציג את כל הספרים בחנות שהמלאי שלהם נמוך מ-5, כולל פרטי ספר, מחבר, שפה, ז'אנר, מחיר וכמות שנמכרה. "
        "הטבלה כוללת את כל הפרטים הנדרשים לבקרה וניהול מלאי."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר השאילתא", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=900, justify="right").pack(fill="x", padx=4, pady=2)
    row_count_label = tk.Label(top, text="Rows: 0", font=("Arial", 9))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=8)
    for col in columns:
        tree.heading(col, text=col.replace('_', ' ').title())
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)
    try:
        from db_manager import get_low_stock_books_with_author
        rows = get_low_stock_books_with_author()
        for row in rows:
            tree.insert("", "end", values=[row[c] for c in columns])
        row_count_label.config(text=f"Rows: {len(rows)}")
    except Exception as e:
        row_count_label.config(text=f"Error: {e}", fg="red")

def open_last_orders_query_window():
    columns = [
        "orderid", "customer_name", "customer_type", "customer_discount", "seller_name", "seller_experience", "orderdate", "items_count", "total_price", "books_ordered"
    ]
    win_width = len(columns) * 120 + 60
    win_height = 350
    top = tk.Toplevel()
    top.title("10 ההזמנות האחרונות")
    top.geometry(f"{win_width}x{win_height}")
    desc = (
        "מציג את 10 ההזמנות האחרונות שבוצעו בחנות. "
        "הטבלה כוללת פרטי לקוח, סוג לקוח, הנחה, פרטי מוכר, תאריך, כמות פריטים, מחיר כולל ושמות הספרים."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר השאילתא", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=900, justify="right").pack(fill="x", padx=4, pady=2)
    row_count_label = tk.Label(top, text="Rows: 0", font=("Arial", 9))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    headers = [
        "OrderID", "Customer Name", "Customer Type", "Customer Discount", "Seller Name", "Seller Experience", "Order Date", "Items Count", "Total Price", "Books Ordered"
    ]
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=8)
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)
    try:
        from db_manager import get_last_10_orders_with_customer_seller
        rows = get_last_10_orders_with_customer_seller()
        for row in rows:
            tree.insert("", "end", values=[row[c] for c in columns])
        row_count_label.config(text=f"Rows: {len(rows)}")
    except Exception as e:
        row_count_label.config(text=f"Error: {e}", fg="red")

def open_last_fines_query_window():
    columns = [
        "fine_number", "borrow_id", "reader_name", "reader_phone", "reader_current_books", "librarian_name", "borrowdate", "returndate", "fine_date", "fine_amount", "fine_reason", "is_paid", "days_borrowed", "borrowed_books"
    ]
    headers = [
        "Fine Number", "Borrow ID", "Reader Name", "Reader Phone", "Reader Current Books", "Librarian Name", "Borrow Date", "Return Date", "Fine Date", "Fine Amount", "Fine Reason", "Is Paid", "Days Borrowed", "Borrowed Books"
    ]
    win_width = 900
    win_height = 420
    top = tk.Toplevel()
    top.title("10 הקנסות האחרונים")
    top.geometry(f"{win_width}x{win_height}")
    desc = (
        "מציג את 10 הקנסות האחרונים שהתקבלו במערכת. "
        "כולל פרטי קורא, ספרן, תאריכים, סיבה, סכום, סטטוס תשלום ופרטי הספרים."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר השאילתא", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=900, justify="right").pack(fill="x", padx=4, pady=2)
    row_count_label = tk.Label(top, text="Rows: 0", font=("Arial", 9))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=8)
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)
    try:
        from db_manager import get_last_10_fines_with_reader_librarian
        rows = get_last_10_fines_with_reader_librarian()
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", "end", values=[row.get(c, "") for c in columns])
        row_count_label.config(text=f"Rows: {len(rows)}")
    except Exception as e:
        row_count_label.config(text=f"Error: {e}", fg="red")
# --- אזור שאילתות (Queries) חדש ---
queries_frame = tk.LabelFrame(root, text="Queries", padx=10, pady=10)
queries_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Update query buttons to match info/statistics buttons
low_stock_btn = tk.Button(queries_frame, text="הצג מלאי נמוך בחנות הספרים", command=lambda: open_low_stock_query_window())
low_stock_btn.pack(pady=10, fill=tk.X)
last_orders_btn = tk.Button(queries_frame, text="הצג 10 הזמנות אחרונות", command=lambda: open_last_orders_query_window())
last_orders_btn.pack(pady=10, fill=tk.X)
books_by_genre_age_btn = tk.Button(queries_frame, text="חיפוש ספרים לפי ז'אנר וגיל", command=open_books_by_genre_age_window)
books_by_genre_age_btn.pack(pady=10, fill=tk.X)
last_fines_btn = tk.Button(queries_frame, text="הצג 10 קנסות אחרונים", command=open_last_fines_query_window)
last_fines_btn.pack(pady=10, fill=tk.X)

# --- כפתור: הצג מלאי בחנות הספרים (BookstoreInventory) ---
def open_bookstore_stock_query_window():
    columns = ["BookLanguageID", "Title", "StockQuantity"]
    win_width = 600
    win_height = 400
    top = tk.Toplevel()
    top.title("מלאי בחנות הספרים")
    top.geometry(f"{win_width}x{win_height}")
    desc = (
        "פונקציה זו מציגה את כל הספרים הקיימים במלאי חנות הספרים, כולל מזהה מהדורה, שם הספר וכמות במלאי.\n"
        "הנתונים ממוינים לפי כמות במלאי מהגבוה לנמוך."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר השאילתא", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=900, justify="right").pack(fill="x", padx=4, pady=2)
    row_count_label = tk.Label(top, text="Rows: 0", font=("Arial", 9))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(fill="both", expand=True)
    try:
        import psycopg2
        from config import DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            SELECT 
                bl.BookLanguageID, 
                b.Title, 
                bi.StockQuantity
            FROM BookstoreInventory bi
            JOIN BookLanguage bl ON bi.BookLanguageID = bl.BookLanguageID
            JOIN Book b ON bl.BookID = b.BookID
            ORDER BY bi.StockQuantity DESC;
        ''')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)
        row_count_label.config(text=f"Rows: {len(rows)}")
    except Exception as e:
        row_count_label.config(text=f"Error: {e}", fg="red")

# --- כפתור: הצג ספרים זמינים בספריה (עותקים שאינם מושאלים) ---
def open_library_available_books_window():
    columns = ["LibraryCopyID", "BookLanguageID", "BookID", "Title"]
    win_width = 700
    win_height = 400
    top = tk.Toplevel()
    top.title("ספרים זמינים בספריה")
    top.geometry(f"{win_width}x{win_height}")
    desc = (
        "פונקציה זו מציגה את כל העותקים הפיזיים הזמינים בספריה (שאינם מושאלים כרגע).\n"
        "הטבלה כוללת מזהה עותק, מזהה מהדורה, מזהה ספר ושם הספר."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר השאילתא", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=900, justify="right").pack(fill="x", padx=4, pady=2)
    row_count_label = tk.Label(top, text="Rows: 0", font=("Arial", 9))
    row_count_label.pack(anchor="nw", padx=20, pady=(0, 0))
    result_frame = tk.Frame(top)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True)
    try:
        import psycopg2
        from config import DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            SELECT lc.LibraryCopyID, bl.BookLanguageID, b.BookID, b.Title
            FROM LibraryCopy lc
            JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
            JOIN Book b ON bl.BookID = b.BookID
            WHERE lc.LibraryCopyID NOT IN (
                SELECT br.LibraryCopyID
                FROM Borrowed br
                JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
                WHERE bo.WasReturned = FALSE
            );
        ''')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)
        row_count_label.config(text=f"Rows: {len(rows)}")
    except Exception as e:
        row_count_label.config(text=f"Error: {e}", fg="red")

# --- הוספת הכפתורים למסגרת ה-QUERIES ---
library_stock_btn = tk.Button(queries_frame, text="הצג מלאי בחנות הספרים", command=open_bookstore_stock_query_window)
library_stock_btn.pack(pady=10, fill=tk.X)
library_available_btn = tk.Button(queries_frame, text="הצג ספרים זמינים בספריה", command=open_library_available_books_window)
library_available_btn.pack(pady=10, fill=tk.X)

# --- אזור פרוצידורות (Procedures) חדש ---
procedures_frame = tk.LabelFrame(root, text="פרוצדורות", padx=10, pady=10)
procedures_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

def open_borrow_procedure_window():
    top = tk.Toplevel()
    top.title("השאלת ספר בספריה (פרוצדורה)")
    top.geometry("750x420")
    desc = (
        "פרוצידורה זו מוסיפה השאלה חדשה למערכת.\n"
        "יש לבחור מזהה קורא, מזהה ספרן, ורשימת עותקים זמינים להשאלה."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר הפרוצידורה", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=900, justify="right").pack(fill="x", padx=4, pady=2)
    # --- בחירת מזהים ---
    form_frame = tk.Frame(top)
    form_frame.pack(pady=10)
    # --- מזהה קורא ---
    tk.Label(form_frame, text="מזהה קורא:").grid(row=0, column=0, sticky="e", padx=4, pady=2)
    reader_var = tk.StringVar()
    reader_entry = tk.Entry(form_frame, textvariable=reader_var, width=10)
    reader_entry.grid(row=0, column=1, padx=4)
    tk.Button(form_frame, text="הצג קוראים", command=lambda: show_readers_window(top)).grid(row=0, column=2, padx=4)
    # --- מזהה ספרן ---
    tk.Label(form_frame, text="מזהה ספרן:").grid(row=1, column=0, sticky="e", padx=4, pady=2)
    librarian_var = tk.StringVar()
    librarian_entry = tk.Entry(form_frame, textvariable=librarian_var, width=10)
    librarian_entry.grid(row=1, column=1, padx=4)
    tk.Button(form_frame, text="הצג ספרנים", command=lambda: show_librarians_window(top)).grid(row=1, column=2, padx=4)
    # --- עותקים זמינים (ריבוי בחירה) ---
    tk.Label(form_frame, text="עותקים זמינים להשאלה:").grid(row=2, column=0, sticky="ne", padx=4, pady=2)
    copies_listbox = tk.Listbox(form_frame, selectmode=tk.MULTIPLE, width=50, height=6)
    copies_listbox.grid(row=2, column=1, padx=4, pady=2)
    # --- מילוי רשימות ---
    def load_available_copies():
        copies_listbox.delete(0, tk.END)
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute('''
                SELECT lc.LibraryCopyID, b.Title, l.LanguageName
                FROM LibraryCopy lc
                JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
                JOIN Book b ON bl.BookID = b.BookID
                JOIN Language l ON bl.LanguageID = l.LanguageID
                WHERE lc.LibraryCopyID NOT IN (
                    SELECT br.LibraryCopyID
                    FROM Borrowed br
                    JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
                    WHERE bo.WasReturned = FALSE
                );
            ''')
            rows = cur.fetchall()
            cur.close()
            conn.close()
            for row in rows:
                copies_listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]})")
        except Exception as e:
            copies_listbox.insert(tk.END, f"שגיאה: {e}")
    load_available_copies()
    # --- כפתור להרצת הפרוצדורה ---
    def run_procedure():
        reader_id = reader_var.get().strip()
        librarian_id = librarian_var.get().strip()
        selected = copies_listbox.curselection()
        if not reader_id or not reader_id.isdigit():
            messagebox.showerror("שגיאה", "יש להזין מזהה קורא חוקי.")
            return
        if not librarian_id or not librarian_id.isdigit():
            messagebox.showerror("שגיאה", "יש להזין מזהה ספרן חוקי.")
            return
        # --- בדיקת קיום מזהה קורא/ספרן ---
        from db_manager import check_reader_exists, check_librarian_exists
        if not check_reader_exists(int(reader_id)):
            messagebox.showerror("Error", f"No reader with ID {reader_id} exists in the system. Please try again.")
            return
        if not check_librarian_exists(int(librarian_id)):
            messagebox.showerror("Error", f"No librarian with ID {librarian_id} exists in the system. Please try again.")
            return
        if not selected:
            messagebox.showerror("שגיאה", "יש לבחור לפחות עותק אחד.")
            return
        copy_ids = []
        for i in selected:
            val = copies_listbox.get(i)
            copy_id = val.split(" - ")[0]
            if copy_id.isdigit():
                copy_ids.append(int(copy_id))
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            conn.notices.clear()  # נקה הודעות ישנות
            cur.execute("CALL create_new_borrow(%s, %s, %s)", (int(reader_id), int(librarian_id), copy_ids))
            conn.commit()
            cur.close()
            notice_msg = None
            if conn.notices:
                notice_msg = conn.notices[-1].strip()
            conn.close()
            if notice_msg:
                messagebox.showinfo("הצלחה", notice_msg)
            else:
                messagebox.showinfo("הצלחה", "ההשאלה נוספה בהצלחה!")
            load_available_copies()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהרצת הפרוצדורה:\n{e}")
    run_btn = tk.Button(top, text="בצע השאלה", command=run_procedure)
    run_btn.pack(pady=20)

# --- פרוצדורה: ביצוע הזמנה בחנות הספרים ---
def open_order_procedure_window():
    top = tk.Toplevel()
    top.title("ביצוע הזמנה בחנות הספרים (פרוצדורה)")
    top.geometry("850x520")
    desc = (
        "פרוצדורה זו מוסיפה הזמנה חדשה לחנות הספרים.\n"
        "יש לבחור מזהה לקוח, מזהה מוכר, ולבחור ספרים זמינים להזמנה.\n"
        "עבור כל ספר שנבחר, יש להגדיר את הכמות (1 עד מלאי)."
    )
    desc_frame = tk.LabelFrame(top, text="הסבר הפרוצדורה", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=800, justify="right").pack(fill="x", padx=4, pady=2)
    form_frame = tk.Frame(top)
    form_frame.pack(pady=10, fill="x")
    # --- מזהה לקוח ---
    tk.Label(form_frame, text="מזהה לקוח:").grid(row=0, column=0, sticky="e", padx=4, pady=2)
    customer_var = tk.StringVar()
    customer_entry = tk.Entry(form_frame, textvariable=customer_var, width=10)
    customer_entry.grid(row=0, column=1, padx=4)
    tk.Button(form_frame, text="הצג לקוחות", command=lambda: show_customers_window(top)).grid(row=0, column=2, padx=4)
    # --- תצוגת סוג הזמנה בראש החלון, בצד ימין, פונט ברירת מחדל, גודל קטן ---
    order_type_frame = tk.Frame(top, bd=2, relief="groove", width=170, height=38)
    order_type_frame.pack(anchor="ne", pady=10, padx=30)
    order_type_frame.pack_propagate(False)
    order_type_label = tk.Label(order_type_frame, text="", font=("", 11, "bold"), width=13, anchor="center")
    order_type_label.pack(expand=True, fill="both")
    def update_order_type_label(*args):
        customer_id = customer_var.get().strip()
        from db_manager import get_customer_type
        if not customer_id or not customer_id.isdigit():
            order_type_label.config(text="", bg="#F0F0F0")
            return
        ctype = get_customer_type(int(customer_id))
        if ctype == "Library":
            order_type_label.config(text="הזמנת ספריה", bg="#B7E3F7", fg="#222")
        elif ctype == "Individual":
            order_type_label.config(text="הזמנה פרטית", bg="#D6EAF8", fg="#222")
        else:
            order_type_label.config(text="", bg="#F0F0F0")
    customer_var.trace_add('write', update_order_type_label)
    # --- מזהה מוכר ---
    tk.Label(form_frame, text="מזהה מוכר:").grid(row=1, column=0, sticky="e", padx=4, pady=2)
    seller_var = tk.StringVar()
    seller_entry = tk.Entry(form_frame, textvariable=seller_var, width=10)
    seller_entry.grid(row=1, column=1, padx=4)
    tk.Button(form_frame, text="הצג מוכרים", command=lambda: show_sellers_window(top)).grid(row=1, column=2, padx=4)
    # --- ספרים זמינים ---
    books_frame = tk.LabelFrame(top, text="בחר ספרים להזמנה (Ctrl+Click לריבוי)", padx=8, pady=8)
    books_frame.pack(pady=8, padx=10, fill="both", expand=True)
    books_listbox = tk.Listbox(books_frame, selectmode=tk.MULTIPLE, width=70, height=10)
    books_listbox.pack(side=tk.LEFT, fill="y", padx=4)
    # מילוי ספרים זמינים
    import psycopg2
    from config import DB_CONFIG
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            SELECT bi.BookLanguageID, b.Title, l.LanguageName, bi.StockQuantity
            FROM BookstoreInventory bi
            JOIN BookLanguage bl ON bi.BookLanguageID = bl.BookLanguageID
            JOIN Book b ON bl.BookID = b.BookID
            JOIN Language l ON bl.LanguageID = l.LanguageID
            WHERE bi.StockQuantity > 0
            ORDER BY b.Title;
        ''')
        books = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        books = []
        books_listbox.insert(tk.END, f"שגיאה: {e}")
    book_id_to_info = {}
    for row in books:
        book_id_to_info[row[0]] = row  # BookLanguageID: (BookLanguageID, Title, LanguageName, StockQuantity)
        books_listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]}) | Stock: {row[3]}")
    # --- מסגרת לכמויות ---
    qty_frame = tk.Frame(books_frame)
    qty_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=8)
    qty_labels = {}
    qty_spinboxes = {}
    def update_qty_fields(event=None):
        # הסר שדות קודמים
        for widget in qty_frame.winfo_children():
            widget.destroy()
        qty_labels.clear()
        qty_spinboxes.clear()
        selected = books_listbox.curselection()
        for idx, i in enumerate(selected):
            val = books_listbox.get(i)
            booklanguage_id = int(val.split(" - ")[0])
            info = book_id_to_info[booklanguage_id]
            max_qty = info[3]
            tk.Label(qty_frame, text=f"{info[1]} ({info[2]}) - כמות:").grid(row=idx, column=0, sticky="e", pady=2)
            qty_var = tk.StringVar(value="1")
            spin = tk.Spinbox(qty_frame, from_=1, to=max_qty, width=5, textvariable=qty_var)
            spin.grid(row=idx, column=1, padx=4, pady=2)
            qty_labels[booklanguage_id] = qty_var
            qty_spinboxes[booklanguage_id] = spin
    books_listbox.bind('<<ListboxSelect>>', update_qty_fields)
    # --- כפתור ביצוע הזמנה ---
    def run_order_procedure():
        customer_id = customer_var.get().strip()
        seller_id = seller_var.get().strip()
        selected = books_listbox.curselection()
        if not customer_id or not customer_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid customer ID.")
            return
        if not seller_id or not seller_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid seller ID.")
            return
        from db_manager import check_customer_exists, check_seller_exists
        if not check_customer_exists(int(customer_id)):
            messagebox.showerror("Error", f"No customer with ID {customer_id} exists in the system. Please try again.")
            return
        if not check_seller_exists(int(seller_id)):
            messagebox.showerror("Error", f"No seller with ID {seller_id} exists in the system. Please try again.")
            return
        if not selected:
            messagebox.showerror("Error", "Please select at least one book.")
            return
        booklanguage_ids = []
        quantities = []
        for i in selected:
            val = books_listbox.get(i)
            booklanguage_id = int(val.split(" - ")[0])
            qty_str = qty_labels[booklanguage_id].get()
            info = book_id_to_info[booklanguage_id]
            max_qty = info[3]
            try:
                qty = int(qty_str)
            except Exception:
                messagebox.showerror("Error", f"Invalid quantity for book {info[1]} ({info[2]}). Must be a number.")
                return
            if qty < 1 or qty > max_qty:
                messagebox.showerror("Error", f"Quantity for book {info[1]} ({info[2]}) must be between 1 and {max_qty}.")
                return
            booklanguage_ids.append(booklanguage_id)
            quantities.append(qty)
        # קריאה לפרוצדורה
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            conn.notices.clear()
            cur.execute("CALL create_new_order(%s, %s, %s, %s)", (int(customer_id), int(seller_id), booklanguage_ids, quantities))
            conn.commit()
            cur.close()
            notice_msg = None
            if conn.notices:
                notice_msg = conn.notices[-1].strip()
            conn.close()
            if notice_msg:
                messagebox.showinfo("Success", notice_msg)
            else:
                messagebox.showinfo("Success", "Order created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error running procedure:\n{e}")
    run_btn = tk.Button(top, text="בצע הזמנה", command=run_order_procedure)
    run_btn.pack(pady=20)

# --- הצגת לקוחות ---
def show_customers_window(parent):
    win = tk.Toplevel(parent)
    win.title("מזהי לקוחות")
    win.geometry("350x350")
    columns = ["CustomerID", "FullName"]
    tree = ttk.Treeview(win, columns=columns, show='headings', height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    try:
        import psycopg2
        from config import DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            SELECT c.CustomerID, p.FirstName || ' ' || p.LastName AS FullName
            FROM Customer c
            JOIN Person p ON c.CustomerID = p.ID;
        ''')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        tk.Label(win, text=f"שגיאה: {e}", fg="red").pack()

# --- הצגת מוכרים ---
def show_sellers_window(parent):
    win = tk.Toplevel(parent)
    win.title("מזהי מוכרים")
    win.geometry("350x350")
    columns = ["SellerID", "FullName"]
    tree = ttk.Treeview(win, columns=columns, show='headings', height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    try:
        import psycopg2
        from config import DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            SELECT s.SellerID, p.FirstName || ' ' || p.LastName AS FullName
            FROM Seller s
            JOIN Person p ON s.SellerID = p.ID;
        ''')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        tk.Label(win, text=f"שגיאה: {e}", fg="red").pack()

# --- כפתור לאזור הפרוצדות ---
borrow_proc_btn = tk.Button(procedures_frame, text="השאלת ספר בספריה", command=open_borrow_procedure_window)
borrow_proc_btn.pack(pady=10, fill=tk.X)
order_proc_btn = tk.Button(procedures_frame, text="בצע הזמנה בחנות הספרים", command=open_order_procedure_window)
order_proc_btn.pack(pady=10, fill=tk.X)

# (הוסר) כפתור גישה להרצת Main Borrow Interactive מתוך אזור הפרוצדורות

# --- ויזרד חדש: השאלה בספרייה (UX מודרך) ---
def open_library_borrow_wizard():
    top = tk.Toplevel()
    top.title("השאלה בספרייה - ויזרד")
    top.geometry("1000x560")

    # --- שלב 1: זיהוי קורא ---
    reader_frame = tk.LabelFrame(top, text="זיהוי קורא", padx=10, pady=10)
    reader_frame.pack(fill="x", padx=10, pady=(10, 6))
    tk.Label(reader_frame, text="ReaderID:").pack(side=tk.RIGHT, padx=6)
    reader_var = tk.StringVar()
    reader_entry = tk.Entry(reader_frame, textvariable=reader_var, width=10)
    reader_entry.pack(side=tk.RIGHT)
    reader_status = tk.Label(reader_frame, text="", fg="red")
    reader_status.pack(side=tk.RIGHT, padx=10)

    def validate_reader(event=None):
        rid = reader_var.get().strip()
        if not rid or not rid.isdigit():
            reader_status.config(text="יש להזין מספר קורא תקין")
            return False
        from db_manager import check_reader_exists
        if not check_reader_exists(int(rid)):
            reader_status.config(text="הקורא לא נמצא")
            return False
        reader_status.config(text="✓ נמצא", fg="green")
        return True

    reader_entry.bind('<FocusOut>', validate_reader)

    # --- שלב 2: רשימת ספרים זמינים ---
    books_frame = tk.LabelFrame(top, text="בחר/י ספר להשאלה (זמינים)", padx=10, pady=8)
    books_frame.pack(fill="both", expand=True, padx=10, pady=(6, 6))
    # חיפוש
    search_frame = tk.Frame(books_frame)
    search_frame.pack(fill="x", pady=(0, 6))
    tk.Label(search_frame, text="חיפוש לפי שם/BookID:").pack(side=tk.RIGHT)
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=24)
    search_entry.pack(side=tk.RIGHT, padx=6)
    # טבלה
    books_columns = ["BookID", "Title", "AvailableCopies"]
    books_tree = ttk.Treeview(books_frame, columns=books_columns, show='headings', height=8)
    for col in books_columns:
        books_tree.heading(col, text=col)
        books_tree.column(col, width=200 if col == "Title" else 120)
    books_tree.pack(fill="both", expand=True)
    books_row_count = tk.Label(books_frame, text="Rows: 0", font=("Arial", 9))
    books_row_count.pack(anchor="nw")

    # --- שלב 3: עותקים זמינים ---
    copies_frame = tk.LabelFrame(top, text="עותקים זמינים לספר שנבחר", padx=10, pady=8)
    copies_frame.pack(fill="both", expand=True, padx=10, pady=(6, 6))
    copies_columns = ["LibraryCopyID", "Language", "Condition", "Shelf", "Floor", "Row"]
    copies_tree = ttk.Treeview(copies_frame, columns=copies_columns, show='headings', height=8)
    for col in copies_columns:
        copies_tree.heading(col, text=col)
        copies_tree.column(col, width=130)
    copies_tree.pack(fill="both", expand=True)
    copies_row_count = tk.Label(copies_frame, text="Rows: 0", font=("Arial", 9))
    copies_row_count.pack(anchor="nw")

    # --- כפתורי פעולה ---
    actions = tk.Frame(top)
    actions.pack(fill="x", padx=10, pady=(6, 12))
    borrow_btn = tk.Button(actions, text="השאל", state=tk.DISABLED)
    borrow_btn.pack(side=tk.RIGHT, padx=6)
    refresh_btn = tk.Button(actions, text="רענן")
    refresh_btn.pack(side=tk.RIGHT, padx=6)

    # --- טעינת ספרים זמינים (שאילתה ישירה) ---
    all_books = []
    def load_available_books():
        nonlocal all_books
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute('''
                SELECT 
                    bl.BookID AS book_id,
                    MIN(b.Title) AS title,
                    COUNT(*) AS available_copies
                FROM LibraryCopy lc
                JOIN BookLanguage bl ON bl.BookLanguageID = lc.BookLanguageID
                JOIN Book b ON b.BookID = bl.BookID
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM Borrowed br
                    JOIN Borrow bo ON bo.BorrowNumber = br.BorrowNumber
                    WHERE br.LibraryCopyID = lc.LibraryCopyID
                      AND bo.WasReturned = FALSE
                )
                GROUP BY bl.BookID
                ORDER BY title;
            ''')
            rows = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            rows = []
            messagebox.showerror("שגיאה", f"שגיאה בטעינת ספרים זמינים:\n{e}")
        all_books = rows
        apply_book_filter()

    def apply_book_filter(event=None):
        query = search_var.get().strip().lower()
        for r in books_tree.get_children():
            books_tree.delete(r)
        filtered = []
        for row in all_books:
            bid, title, cnt = row
            if not query:
                filtered.append(row)
            else:
                if query.isdigit() and str(bid).startswith(query):
                    filtered.append(row)
                elif query in str(title).lower():
                    filtered.append(row)
        for row in filtered:
            books_tree.insert("", "end", values=row)
        books_row_count.config(text=f"Rows: {len(filtered)}")
        # ניקוי טבלת העותקים בבחירה חדשה
        for r in copies_tree.get_children():
            copies_tree.delete(r)
        copies_row_count.config(text="Rows: 0")
        borrow_btn.config(state=tk.DISABLED)

    search_entry.bind('<KeyRelease>', apply_book_filter)

    # --- טעינת עותקים עבור ספר ---
    selected_book_id = None
    def load_copies_for_selected_book(event=None):
        nonlocal selected_book_id
        sel = books_tree.selection()
        if not sel:
            return
        item = books_tree.item(sel[0])
        vals = item.get('values')
        if not vals:
            return
        selected_book_id = int(vals[0])
        # קריאה לפונקציה הקיימת: check_book_availability(book_id)
        try:
            rows = check_book_availability_db(selected_book_id)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בבדיקת זמינות:\n{e}")
            return
        for r in copies_tree.get_children():
            copies_tree.delete(r)
        if not rows:
            copies_row_count.config(text="Rows: 0")
            # אין זמינות: הצג לווים נוכחיים בחלון נפרד
            show_borrowers_when_no_availability(selected_book_id)
            borrow_btn.config(state=tk.DISABLED)
            return
        for row in rows:
            # מצופה: (library_copy_id, language_name, copy_condition, shelf_number, floor, row_num, ...)
            copies_tree.insert("", "end", values=row[:6])
        copies_row_count.config(text=f"Rows: {len(rows)}")
        borrow_btn.config(state=tk.DISABLED)

    books_tree.bind('<<TreeviewSelect>>', load_copies_for_selected_book)

    # --- חלון לווים נוכחיים ---
    def show_borrowers_when_no_availability(book_id):
        win = tk.Toplevel(top)
        win.title("אין זמינות - לווים נוכחיים")
        win.geometry("800x360")
        tk.Label(win, text="אין עותקים זמינים לספר זה כרגע. להלן הלווים הנוכחיים:").pack(pady=8)
        columns = ["LibraryCopyID", "ReaderID", "Name", "BorrowDate", "DaysOverdue"]
        tree = ttk.Treeview(win, columns=columns, show='headings', height=10)
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, width=140)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        row_count_label = tk.Label(win, text="Rows: 0", font=("Arial", 9))
        row_count_label.pack(anchor="nw", padx=10)
        try:
            rows = get_book_borrowers_db(book_id)
            for row in rows:
                tree.insert("", "end", values=row[:5])
            row_count_label.config(text=f"Rows: {len(rows)}")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת לווים:\n{e}")

    # --- פעולה: ביצוע השאלה ---
    def on_copy_selection(event=None):
        sel = copies_tree.selection()
        borrow_btn.config(state=(tk.NORMAL if sel else tk.DISABLED))

    copies_tree.bind('<<TreeviewSelect>>', on_copy_selection)

    def perform_borrow(event=None):
        if not validate_reader():
            messagebox.showerror("שגיאה", "יש לאשר ReaderID תקין לפני המשך.")
            return
        sel = copies_tree.selection()
        if not sel:
            messagebox.showerror("שגיאה", "יש לבחור עותק אחד להשאלה.")
            return
        copy_vals = copies_tree.item(sel[0]).get('values')
        if not copy_vals:
            messagebox.showerror("שגיאה", "בחירה לא חוקית.")
            return
        library_copy_id = int(copy_vals[0])
        reader_id = int(reader_var.get().strip())
        librarian_id = 801
        # מניעת לחיצות כפולות
        borrow_btn.config(state=tk.DISABLED)
        top.config(cursor="watch")
        top.update_idletasks()
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            try:
                conn.notices.clear()
            except Exception:
                pass
            cur.execute("CALL public.create_new_borrow(%s, %s, %s)", (reader_id, librarian_id, [library_copy_id]))
            conn.commit()
            cur.close()
            # קבלת מספר השאלה האחרון לקורא
            cur2 = None
            borrow_number = None
            try:
                cur2 = conn.cursor()
                cur2.execute("SELECT MAX(BorrowNumber) FROM public.Borrow WHERE ReaderID=%s", (reader_id,))
                row = cur2.fetchone()
                if row and row[0] is not None:
                    borrow_number = int(row[0])
            finally:
                if cur2:
                    cur2.close()
            conn.close()
            if borrow_number is not None:
                messagebox.showinfo("הצלחה", f"ההשאלה מספר #{borrow_number} שויכה בהצלחה למשתמש {reader_id}.")
            else:
                messagebox.showinfo("הצלחה", "ההשאלה בוצעה בהצלחה.")
            # רענון רשימות
            load_available_books()
            if selected_book_id is not None:
                load_copies_for_selected_book()
        except Exception as e:
            msg = str(e)
            if 'books already borrowed' in msg or 'already borrowed' in msg:
                messagebox.showerror("שגיאה", "העותק שנבחר הושאל כעת ע""י משתמש אחר. נא לבחור עותק אחר.")
            else:
                messagebox.showerror("שגיאה", f"שגיאה בביצוע השאלה:\n{e}")
        finally:
            top.config(cursor="")
            borrow_btn.config(state=tk.NORMAL)

    # הפעלת הפעולה מכפתור, לחיצה כפולה וקיצורי מקלדת
    borrow_btn.config(command=perform_borrow)
    copies_tree.bind('<Double-1>', perform_borrow)
    top.bind('<Control-Return>', perform_borrow)
    top.bind('<Control-b>', perform_borrow)
    refresh_btn.config(command=lambda: (load_available_books(), apply_book_filter()))

    # טעינה ראשונית
    load_available_books()

# (הועבר) כפתור פתיחת הוויזרד ייווצר באזור "תוכניות ראשיות"


# --- אזור תוכניות ראשיות (Main Programs) ---
main_programs_frame = tk.LabelFrame(root, text="תוכניות ראשיות", padx=10, pady=10, bd=3, relief="ridge")
main_programs_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

def open_main_borrow_program_window():
    top = tk.Toplevel()
    top.title("Main Program - Borrow Interactive")
    top.geometry("800x500")
    desc = (
        "תוכנית ראשית אינטראקטיבית להרצת תהליך השאלה מהמאגר כפי שמוגדר ב-DB.\n"
        "ההרצה קוראת ל- CALL public.main_borrow_interactive() ומציגה את הודעות ה-NOTICE."
    )
    desc_frame = tk.LabelFrame(top, text="תיאור", padx=10, pady=10)
    desc_frame.pack(pady=10, padx=10, fill="x")
    tk.Label(desc_frame, text=desc, wraplength=760, justify="right").pack(fill="x")

    controls = tk.Frame(top)
    controls.pack(pady=6, padx=10, fill="x")

    run_btn = tk.Button(controls, text="הרץ תוכנית", width=14)
    run_btn.pack(side=tk.RIGHT)

    output_frame = tk.LabelFrame(top, text="פלט (NOTICES)", padx=8, pady=8)
    output_frame.pack(padx=10, pady=10, fill="both", expand=True)

    text = tk.Text(output_frame, height=18)
    text.pack(fill="both", expand=True)

    def run_program():
        text.delete("1.0", tk.END)
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            # נקה הודעות קודמות במידה וקיימות
            try:
                conn.notices.clear()
            except Exception:
                pass
            cur.execute("CALL public.main_borrow_interactive();")
            conn.commit()
            cur.close()
            notices = []
            try:
                notices = [n.strip() for n in getattr(conn, 'notices', [])]
            except Exception:
                notices = []
            conn.close()
            if notices:
                for n in notices:
                    text.insert(tk.END, n + "\n")
            else:
                text.insert(tk.END, "ההרצה הושלמה. לא התקבלו NOTICE מהשרת.\n")
        except Exception as e:
            text.insert(tk.END, f"שגיאה בהרצת התוכנית:\n{e}\n")

    run_btn.config(command=run_program)

# כפתורים לאזור התוכניות הראשיות
# כפתור יחיד באזור התוכניות הראשיות: ביצוע השאלה בספריה
borrow_wizard_btn = tk.Button(main_programs_frame, text="ביצוע השאלה בספריה", command=open_library_borrow_wizard)
borrow_wizard_btn.pack(pady=10, fill=tk.X)

# --- תוכנית ראשית 2: הזמנת ספר בחנות (ויזרד) ---
def open_bookstore_order_main_program():
    top = tk.Toplevel()
    top.title("הזמנת ספר בחנות - ויזרד")
    top.geometry("1200x780")

    # --- Best Sellers (פונקציה) ---
    best_frame = tk.LabelFrame(top, text="Best Sellers (public.get_top_selling_books)", padx=8, pady=8)
    best_frame.pack(fill="x", padx=10, pady=(10, 6))
    best_cols = ["Rank Position", "BookLanguage ID", "Book Title", "Author Name", "Total Copies Sold", "Total Revenue"]
    best_tree = ttk.Treeview(best_frame, columns=best_cols, show='headings', height=6)
    for c in best_cols:
        best_tree.heading(c, text=c)
        best_tree.column(c, width=150)
    best_tree.pack(fill="x", expand=False)
    try:
        rows = get_top_selling_books_db()
        for r in rows:
            best_tree.insert("", "end", values=r)
    except Exception:
        pass

    # --- זיהוי לקוח ---
    id_frame = tk.LabelFrame(top, text="זיהוי לקוח והנחה", padx=8, pady=8)
    id_frame.pack(fill="x", padx=10, pady=(6, 6))
    tk.Label(id_frame, text="CustomerID:").pack(side=tk.RIGHT, padx=6)
    cust_var = tk.StringVar()
    cust_entry = tk.Entry(id_frame, textvariable=cust_var, width=10)
    cust_entry.pack(side=tk.RIGHT)
    cust_status = tk.Label(id_frame, text="", fg="red")
    cust_status.pack(side=tk.RIGHT, padx=10)

    discount_var = tk.DoubleVar(value=0.0)
    type_var = tk.StringVar(value="")
    discount_display_var = tk.StringVar(value="0")
    tk.Label(id_frame, textvariable=type_var).pack(side=tk.LEFT, padx=8)
    tk.Label(id_frame, text="הנחת לקוח (%):").pack(side=tk.LEFT)
    disc_label = tk.Label(id_frame, textvariable=discount_display_var)
    disc_label.pack(side=tk.LEFT, padx=4)
    check_btn = tk.Button(id_frame, text="בדוק", width=8)
    check_btn.pack(side=tk.LEFT, padx=6)

    def validate_customer(event=None):
        cid = cust_var.get().strip()
        if not cid or not cid.isdigit():
            cust_status.config(text="הזיני CustomerID תקין", fg="red")
            discount_var.set(0.0)
            type_var.set("")
            discount_display_var.set("0")
            return False
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT Discount, CustomerType FROM public.Customer WHERE CustomerID=%s", (int(cid),))
            row = cur.fetchone()
            cur.close(); conn.close()
            if not row:
                cust_status.config(text="לקוח לא נמצא", fg="red")
                discount_var.set(0.0)
                type_var.set("")
                discount_display_var.set("0")
                return False
            discount_var.set(float(row[0] or 0))
            type_var.set(f"סוג לקוח: {row[1] or ''}")
            discount_display_var.set(str(row[0] or 0))
            cust_status.config(text="✓ נמצא", fg="green")
            return True
        except Exception as e:
            cust_status.config(text=f"שגיאה: {e}", fg="red")
            return False

    cust_entry.bind('<FocusOut>', validate_customer)
    cust_entry.bind('<Return>', validate_customer)
    check_btn.config(command=validate_customer)

    # --- קטלוג זמין ---
    catalog_frame = tk.LabelFrame(top, text="קטלוג מלאי זמין (StockQuantity>0)", padx=8, pady=8)
    catalog_frame.pack(fill="both", expand=True, padx=10, pady=(6, 6))
    search_cat = tk.StringVar(value="")
    tk.Label(catalog_frame, text="חיפוש שם/שפה:").pack(side=tk.TOP, anchor='e')
    search_entry2 = tk.Entry(catalog_frame, textvariable=search_cat, width=24)
    search_entry2.pack(side=tk.TOP, anchor='e', pady=2)
    # כמות להוספה + כפתור הוספה לעגלה
    ctl_bar = tk.Frame(catalog_frame)
    ctl_bar.pack(fill="x", pady=4)
    tk.Label(ctl_bar, text="כמות להוספה:").pack(side=tk.RIGHT)
    qty_var = tk.StringVar(value="1")
    qty_spin = tk.Spinbox(ctl_bar, from_=1, to=999, width=6, textvariable=qty_var)
    qty_spin.pack(side=tk.RIGHT, padx=6)
    add_btn = tk.Button(ctl_bar, text="הוסף לעגלה")
    add_btn.pack(side=tk.RIGHT)
    stock_hint = tk.Label(ctl_bar, text="")
    stock_hint.pack(side=tk.LEFT)
    columns = ["BookLanguageID", "Title", "Language", "Price", "InStock"]
    cat_tree = ttk.Treeview(catalog_frame, columns=columns, show='headings', height=8)
    for c in columns:
        cat_tree.heading(c, text=c)
        cat_tree.column(c, width=160 if c=="Title" else 110)
    cat_tree.pack(fill="both", expand=True)
    # הוסר מידע תחתון לא נחוץ

    # טעינת מלאי
    catalog_rows = []
    def load_catalog():
        nonlocal catalog_rows
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute('''
                SELECT bl.BookLanguageID,
                       b.Title,
                       l.LanguageName,
                       bi.BookstorePrice AS price,
                       bi.StockQuantity  AS in_stock
                FROM public.BookstoreInventory bi
                JOIN public.BookLanguage bl ON bl.BookLanguageID = bi.BookLanguageID
                JOIN public.Book         b  ON b.BookID         = bl.BookID
                JOIN public.Language     l  ON l.LanguageID     = bl.LanguageID
                WHERE bi.StockQuantity > 0
                ORDER BY b.Title, l.LanguageName;''')
            catalog_rows = cur.fetchall()
            cur.close(); conn.close()
        except Exception as e:
            catalog_rows = []
            messagebox.showerror("שגיאה", f"שגיאה בטעינת קטלוג:\n{e}")
        apply_catalog_filter()

    def apply_catalog_filter(event=None):
        q = search_cat.get().strip().lower()
        for i in cat_tree.get_children():
            cat_tree.delete(i)
        shown = 0
        for row in catalog_rows:
            bid, title, lang, price, stock = row
            if not q or q in (title or '').lower() or q in (lang or '').lower():
                cat_tree.insert("", "end", values=row)
                shown += 1
        # עדכון רמז מלאי/כמות
        stock_hint.config(text="")
        # אין הצגת מונה בשורה תחתונה

    search_entry2.bind('<KeyRelease>', apply_catalog_filter)

    # --- עגלה: מועברת לחלון צף; שומרים מודל נתונים סמוי ---
    cart_cols = ["BookLanguageID", "Title", "Price", "Qty", "Subtotal"]
    cart_items = []  # list of dicts: {blid,title,price,qty}
    cart_window = {'win': None, 'tree': None, 'total_label': None, 'pay_btn': None}

    def recalc_totals():
        total = 0.0
        for itm in cart_items:
            total += float(itm['price']) * int(itm['qty'])
        disc = discount_var.get() or 0.0
        final = total * (1 - (disc/100.0))
        return total, disc, final

    def open_or_update_cart():
        # פתח אם סגור
        if cart_window['win'] is None or not cart_window['win'].winfo_exists():
            w = tk.Toplevel(top)
            w.title("עגלה")
            w.geometry("640x400")
            w.attributes('-topmost', True)
            t = ttk.Treeview(w, columns=cart_cols, show='headings', height=10)
            for c in cart_cols:
                t.heading(c, text=c)
                t.column(c, width=120 if c != 'Title' else 220)
            t.pack(fill="both", expand=True, padx=10, pady=10)
            footer = tk.Frame(w)
            footer.pack(fill="x", padx=10, pady=(0,10))
            lbl = tk.Label(footer, text="")
            lbl.pack(side=tk.LEFT)
            tk.Button(footer, text="+", width=4, command=lambda: adjust_qty(+1)).pack(side=tk.RIGHT, padx=4)
            tk.Button(footer, text="-", width=4, command=lambda: adjust_qty(-1)).pack(side=tk.RIGHT, padx=4)
            tk.Button(footer, text="Del", width=6, command=lambda: adjust_qty(-999)).pack(side=tk.RIGHT, padx=4)
            pay_btn = tk.Button(footer, text="לתשלום", width=10)
            pay_btn.pack(side=tk.RIGHT, padx=8)
            cart_window['win'] = w
            cart_window['tree'] = t
            cart_window['total_label'] = lbl
            cart_window['pay_btn'] = pay_btn
        # עדכון תוכן
        t = cart_window['tree']
        for i in t.get_children():
            t.delete(i)
        for itm in cart_items:
            t.insert("", "end", values=[itm['blid'], itm['title'], itm['price'], itm['qty'], float(itm['price'])*int(itm['qty'])])
        total, disc, final = recalc_totals()
        cart_window['total_label'].config(text=f"סה\"כ: ₪{total:.2f} | הנחה {disc:.2f}% | לתשלום: ₪{final:.2f}")
        # דאג שהחלון יישאר מעל הראשי ולא ייפתח כפול
        try:
            cart_window['win'].deiconify()
            cart_window['win'].lift()
            cart_window['win'].focus_force()
            cart_window['tree'].update_idletasks()
        except Exception:
            pass

    def on_catalog_select(event=None):
        sel = cat_tree.selection()
        if not sel:
            stock_hint.config(text="")
            return
        bid, title, lang, price, stock = cat_tree.item(sel[0])['values']
        stock_hint.config(text=f"מלאי זמין: {stock}")
        try:
            qty_spin.config(to=int(stock))
        except Exception:
            pass

    cat_tree.bind('<<TreeviewSelect>>', on_catalog_select)

    def add_to_cart_from_catalog(event=None):
        if not validate_customer():
            messagebox.showerror("שגיאה", "יש לאמת לקוח לפני הוספה לעגלה.")
            return
        sel = cat_tree.selection()
        if not sel:
            return
        bid, title, lang, price, stock = cat_tree.item(sel[0])['values']
        # כמות לבקשה
        try:
            add_qty = int(qty_var.get())
        except Exception:
            add_qty = 1
        if add_qty < 1:
            add_qty = 1
        # חפש פריט קיים בעגלה
        for itm in cart_items:
            if itm['blid'] == bid:
                new_qty = int(itm['qty']) + add_qty
                if new_qty > int(stock):
                    messagebox.showerror("שגיאה", f"אין מספיק מלאי לפריט {title}.")
                    return
                itm['qty'] = new_qty
                open_or_update_cart()
                return
        # פריט חדש
        if add_qty > int(stock):
            messagebox.showerror("שגיאה", f"אין מספיק מלאי לפריט {title}.")
            return
        cart_items.append({'blid': bid, 'title': title, 'price': float(price), 'qty': add_qty})
        open_or_update_cart()

    cat_tree.bind('<Double-1>', add_to_cart_from_catalog)
    add_btn.config(command=add_to_cart_from_catalog)
    # אין כפתור רענון; הטעינה אוטומטית בפתיחה ובסינון

    # טען אוטומטית אחרי יצירת החלון (למקרה שחסימה גרפית מנעה טעינה מיידית)
    top.after(50, load_catalog)

    def adjust_qty(delta):
        # התבסס על בחירה בחלון העגלה הצף
        if cart_window['tree'] is None or not cart_window['tree'].winfo_exists():
            return
        sel = cart_window['tree'].selection()
        if not sel:
            return
        blid, title, price, qty, _ = cart_window['tree'].item(sel[0])['values']
        # מצא את הרשומה התואמת בעגלה
        target = None
        for itm in cart_items:
            if itm['blid'] == blid:
                target = itm
                break
        if target is None:
            return
        # בדוק מלאי
        max_stock = None
        for row in catalog_rows:
            if row[0] == blid:
                max_stock = int(row[4]); break
        new_qty = 0 if delta == -999 else max(0, int(qty) + delta)
        if new_qty > 0 and max_stock is not None and new_qty > max_stock:
            messagebox.showerror("שגיאה", f"אין מספיק מלאי לפריט {title} (זמינים {max_stock}).")
            return
        if new_qty == 0:
            cart_items[:] = [i for i in cart_items if i['blid'] != blid]
        else:
            target['qty'] = new_qty
        open_or_update_cart()

    # --- Checkout ---
    checkout_bar = tk.Frame(top)
    checkout_bar.pack(fill="x", padx=10, pady=(0, 12))
    tk.Label(checkout_bar, text="SellerID (ברירת מחדל 1607):").pack(side=tk.RIGHT)
    seller_var = tk.StringVar(value="1607")
    tk.Entry(checkout_bar, textvariable=seller_var, width=8).pack(side=tk.RIGHT, padx=6)
    # כפתור תשלום יוגדר לאחר הגדרת place_order
    summary_btn = tk.Button(checkout_bar, text="סיום קניה / לתשלום", width=18)
    summary_btn.pack(side=tk.RIGHT)
    # פתיחת חלון עגלה כברירת מחדל בזמן הוספה

    def place_order():
        if not validate_customer():
            messagebox.showerror("שגיאה", "יש לאמת לקוח לפני ביצוע הזמנה.")
            return
        cid = int(cust_var.get().strip())
        sid = seller_var.get().strip()
        if not sid or not sid.isdigit():
            messagebox.showerror("שגיאה", "SellerID לא תקין.")
            return
        ids, qties = [], []
        for itm in cart_items:
            ids.append(int(itm['blid'])); qties.append(int(itm['qty']))
        if not ids:
            messagebox.showerror("שגיאה", "העגלה ריקה.")
            return
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            conn.notices.clear()
            cur.execute("CALL public.create_new_order(%s, %s, %s, %s)", (cid, int(sid), ids, qties))
            conn.commit()
            # שליפת OrderID אחרון ללקוח
            cur2 = conn.cursor()
            cur2.execute("SELECT MAX(OrderID) FROM public.Orders WHERE CustomerID=%s", (cid,))
            order_id = cur2.fetchone()[0]
            cur2.close(); cur.close(); conn.close()
            # סכום סופי לפי חישוב מקומי
            total = sum(float(itm['price']) * int(itm['qty']) for itm in cart_items)
            final = total * (1 - (discount_var.get()/100.0))
            messagebox.showinfo("הצלחה", f"ההזמנה מספר #{order_id} נוצרה בהצלחה. סכום סופי: ₪{final:.2f}")
            # רענון מלאי לאחר הטריגר
            load_catalog()
            top.destroy()
        except Exception as e:
            msg = str(e)
            if 'insufficient' in msg or 'stock' in msg:
                messagebox.showerror("שגיאה", "אין מספיק מלאי לאחד הפריטים. רענני את הקטלוג ועדכני כמויות.")
                load_catalog()
            else:
                messagebox.showerror("שגיאה", f"שגיאה בביצוע הזמנה:\n{e}")

    # לאחר שהוגדרה הפונקציה, חבר את הכפתורים
    summary_btn.config(command=place_order)
    def wire_cart_pay_button():
        if cart_window['pay_btn'] is not None:
            try:
                cart_window['pay_btn'].config(command=place_order)
            except Exception:
                pass
    wire_cart_pay_button()

    def open_checkout_summary():
        # סיכום הזמנה לפני ביצוע
        if not validate_customer():
            messagebox.showerror("שגיאה", "יש לאמת לקוח לפני סיום קניה.")
            return
        if not cart_items:
            messagebox.showerror("שגיאה", "העגלה ריקה.")
            return
        dlg = tk.Toplevel(top)
        dlg.title("סיכום הזמנה")
        dlg.geometry("760x420")
        # --- פרטי לקוח ---
        header = tk.Frame(dlg)
        header.pack(fill="x", padx=10, pady=(10, 4))
        cust_info_var = tk.StringVar(value="")
        tk.Label(header, textvariable=cust_info_var, anchor='w', justify='right').pack(side=tk.RIGHT, fill='x', expand=True)
        try:
            import psycopg2
            from config import DB_CONFIG
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute('''
                SELECT c.CustomerID, p.FirstName, p.LastName, c.CustomerType, COALESCE(c.Discount,0)
                FROM public.Customer c
                JOIN public.Person   p ON p.ID = c.CustomerID
                WHERE c.CustomerID=%s
            ''', (int(cust_var.get().strip()),))
            row = cur.fetchone()
            cur.close(); conn.close()
            if row:
                cid, first, last, ctype, disc_db = row
                cust_info_var.set(f"לקוח: {cid} | שם: {first} {last} | סוג: {ctype} | הנחה: {disc_db}%")
        except Exception:
            pass
        cols = ["BookLanguageID", "Title", "Price", "Qty", "Subtotal"]
        tree = ttk.Treeview(dlg, columns=cols, show='headings', height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=110)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        total = 0.0
        for itm in cart_items:
            vals = [itm['blid'], itm['title'], itm['price'], itm['qty'], float(itm['price'])*int(itm['qty'])]
            tree.insert("", "end", values=vals)
            total += float(itm['price']) * int(itm['qty'])
        disc = discount_var.get() or 0.0
        final = total * (1 - (disc/100.0))
        footer = tk.Frame(dlg)
        footer.pack(fill="x", padx=10, pady=(0,10))
        tk.Label(footer, text=f"סה\"כ: ₪{total:.2f} | הנחה {disc:.2f}% | לתשלום: ₪{final:.2f}").pack(side=tk.LEFT)
        tk.Button(footer, text="אישור רכישה", command=lambda: (dlg.destroy(), place_order())).pack(side=tk.RIGHT, padx=6)
        tk.Button(footer, text="חזרה", command=dlg.destroy).pack(side=tk.RIGHT)

    summary_btn.config(command=open_checkout_summary)

    # טעינה ראשונית
    load_catalog()

# כפתור לפתיחת התוכנית הראשית להזמנה
order_main_btn = tk.Button(main_programs_frame, text="ביצוע הזמנה בחנות הספרים", command=open_bookstore_order_main_program)
order_main_btn.pack(pady=10, fill=tk.X)

# קיצור מקלדת לפתיחת תוכנית ההשאלה הראשית (F9)
root.bind("<F9>", lambda e: open_main_borrow_program_window())

# --- Placeholder functions for analytics windows ---
def open_bookstore_analytics_window():
    top = tk.Toplevel()
    top.title("Bookstore Analytics")
    top.geometry("800x500")
    try:
        data = get_bookstore_analytics_db()
        if not data:
            tk.Label(top, text="No data found.", fg="red").pack(pady=30)
            return
        # --- Main grid for all analytics ---
        main_grid = tk.Frame(top)
        main_grid.pack(fill="both", expand=True, padx=10, pady=10)
        # --- Stats 2x2 grid at the top (row 0, colspan=2) ---
        stats_frame = tk.Frame(main_grid)
        stats_frame.grid(row=0, column=0, columnspan=2, pady=(0, 12))
        stat_labels = [
            f"Total Revenue: ₪{data['total_revenue']}",
            f"Total Orders: {data['total_orders']}",
            f"Avg. Order Value: ₪{data['avg_order_value']}",
            f"Low Stock Items (≤3): {data['low_stock_count']}"
        ]
        for i, text in enumerate(stat_labels):
            row, col = divmod(i, 2)
            tk.Label(stats_frame, text=text).grid(row=row, column=col, padx=16, pady=2, sticky="nsew")
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        # --- Table (row 1, col 0) and Pie Chart (row 1, col 1) ---
        genres = data.get('top_genres', [])
        cust_types = data.get('customer_types', [])
        table_frame = None
        if genres:
            genre_names = [g['genre'] for g in genres]
            sales = [g['sales'] for g in genres]
            table_frame = tk.Frame(main_grid)
            table_frame.grid(row=1, column=0, padx=(0, 10), pady=2, sticky="nsew")
            tk.Label(table_frame, text="Top Genres Table").pack()
            genre_table = ttk.Treeview(table_frame, columns=("Genre", "Sales"), show='headings', height=len(genre_names))
            genre_table.heading("Genre", text="Genre")
            genre_table.heading("Sales", text="Sales")
            for g in genres:
                genre_table.insert("", "end", values=(g['genre'], g['sales']))
            genre_table.pack()
        if cust_types:
            labels = [c['type'] if c['type'] else 'Unknown' for c in cust_types]
            counts = [c['count'] for c in cust_types]
            # Custom colors: Library = light blue, Individual = blue
            pie_colors = ['#A9CCE3', '#4F81BD'] if set(labels) == {'Library', 'Individual'} else ["#A9CCE3", "#4F81BD"][:len(labels)]
            fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
            pie_result = ax2.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=pie_colors, textprops={'fontsize': 12})
            ax2.set_title('Customer Types Distribution', fontsize=12)
            fig2.tight_layout()
            canvas2 = FigureCanvasTkAgg(fig2, master=main_grid)  # restore to main_grid
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=1, column=1, padx=(10, 0), pady=2, sticky="nsew")  # restore to grid
        # --- Bar Chart (row 2, colspan=2) ---
        if genres:
            cmap = plt.get_cmap('tab10') if len(genre_names) <= 10 else plt.get_cmap('rainbow')
            colors = [cmap(i / len(genre_names)) for i in range(len(genre_names))]
            fig1, ax1 = plt.subplots(figsize=(6.5, 2))
            bars = ax1.bar(genre_names, sales, color=colors)
            ax1.set_title('Top 5 Selling Genres', fontsize=11)
            ax1.set_ylabel('Sales', fontsize=11)
            ax1.set_xlabel('Genre', fontsize=11)
            for i, v in enumerate(sales):
                ax1.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=9)
            fig1.tight_layout(rect=(0, 0.13, 1, 1))
            canvas1 = FigureCanvasTkAgg(fig1, master=main_grid)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=2, column=0, columnspan=2, padx=0, pady=(10, 0), sticky="nsew")
        # --- Configure grid weights for symmetry ---
        main_grid.grid_rowconfigure(0, weight=0)
        main_grid.grid_rowconfigure(1, weight=1)
        main_grid.grid_rowconfigure(2, weight=1)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=1)
    except Exception as e:
        tk.Label(top, text=f"Error loading data:\n{e}", fg="red").pack(pady=30)

def open_library_analytics_window():
    top = tk.Toplevel()
    top.title("Library Analytics")
    top.geometry("800x500")
    try:
        data = get_library_analytics_db()
        if not data:
            tk.Label(top, text="No data found.", fg="red").pack(pady=30)
            return
        # --- Main grid for all analytics ---
        main_grid = tk.Frame(top)
        main_grid.pack(fill="both", expand=True, padx=10, pady=10)
        # --- Stats 2x2 grid at the top (row 0, colspan=2) ---
        stats_frame = tk.Frame(main_grid)
        stats_frame.grid(row=0, column=0, columnspan=2, pady=(0, 12))
        stat_labels = [
            f"Total Borrows: {data['total_borrows']}",
            f"Active Readers: {data['active_readers']}",
            f"Return Rate: {data['return_rate']}%",
            f"Unpaid Fines: ₪{data['unpaid_fines']}"
        ]
        for i, text in enumerate(stat_labels):
            row, col = divmod(i, 2)
            tk.Label(stats_frame, text=text).grid(row=row, column=col, padx=16, pady=2, sticky="nsew")
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        # --- Top Borrowed Genres Bar Chart (row 1, col 0) ---
        genres = data.get('top_genres', [])
        chart1_frame = None
        bar_colors = []
        if genres:
            genre_names = [g['genre'] for g in genres]
            borrows = [g['borrows'] for g in genres]
            cmap = plt.get_cmap('tab10') if len(genre_names) <= 10 else plt.get_cmap('rainbow')
            bar_colors = [cmap(i / len(genre_names)) for i in range(len(genre_names))]
            fig1, ax1 = plt.subplots(figsize=(3.2, 1.7))
            bars = ax1.bar(range(len(genre_names)), borrows, color=bar_colors)
            ax1.set_title('Top 5 Borrowed Genres', fontsize=11)
            ax1.set_ylabel('Borrows', fontsize=11)
            ax1.set_xlabel('')
            ax1.set_xticks([])  # Remove x labels
            for i, v in enumerate(borrows):
                ax1.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=9)
            fig1.tight_layout(rect=(0, 0.13, 1, 1))
            chart1_frame = FigureCanvasTkAgg(fig1, master=main_grid)
            chart1_frame.draw()
            chart1_frame.get_tk_widget().grid(row=1, column=0, padx=(0, 10), pady=2, sticky="nsew")
            # --- Legend for bar chart ---
            legend_frame = tk.Frame(main_grid)
            legend_frame.grid(row=2, column=0, pady=(0, 10))
            for i, (color, genre) in enumerate(zip(bar_colors, genre_names)):
                c = '#%02x%02x%02x' % tuple(int(255*x) for x in color[:3])
                swatch = tk.Label(legend_frame, bg=c, width=2, height=1)
                swatch.grid(row=0, column=i, padx=2)
                tk.Label(legend_frame, text=genre).grid(row=1, column=i, padx=2)
        # --- Second Chart: Pie of Overdue vs. On Time (row 1, col 1) ---
        overdue = data.get('overdue_books', 0)
        returned = data.get('total_borrows', 0) - overdue if data.get('total_borrows') else 0
        pie_labels = ['Overdue (30+ days)', 'Returned/On Time']
        pie_counts = [overdue, max(returned, 0)]
        cmap2 = plt.get_cmap('Set3')
        pie_colors = [cmap2(i / 2) for i in range(2)]
        fig2, ax2 = plt.subplots(figsize=(2, 2))
        pie_result = ax2.pie(pie_counts, labels=None, autopct='%1.1f%%', startangle=140, colors=pie_colors, textprops={'fontsize': 11})
        ax2.set_title('Borrow Status Distribution', fontsize=11)
        fig2.tight_layout(rect=(0, 0.13, 1, 1))
        chart2_frame = FigureCanvasTkAgg(fig2, master=main_grid)
        chart2_frame.draw()
        chart2_frame.get_tk_widget().grid(row=1, column=1, padx=(10, 0), pady=2, sticky="nsew")
        # --- Legend for pie chart ---
        pie_legend_frame = tk.Frame(main_grid)
        pie_legend_frame.grid(row=2, column=1, pady=(0, 10))
        for i, (color, label) in enumerate(zip(pie_colors, pie_labels)):
            c = '#%02x%02x%02x' % tuple(int(255*x) for x in color[:3])
            swatch = tk.Label(pie_legend_frame, bg=c, width=2, height=1)
            swatch.grid(row=0, column=i, padx=2)
            tk.Label(pie_legend_frame, text=label).grid(row=1, column=i, padx=2)
        # --- Configure grid weights for symmetry ---
        main_grid.grid_rowconfigure(0, weight=0)
        main_grid.grid_rowconfigure(1, weight=1)
        main_grid.grid_rowconfigure(2, weight=0)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=1)
    except Exception as e:
        tk.Label(top, text=f"Error loading data:\n{e}", fg="red").pack(pady=30)

def show_readers_window(parent):
    win = tk.Toplevel(parent)
    win.title("מזהי קוראים")
    win.geometry("350x350")
    columns = ["ReaderID", "FullName"]
    tree = ttk.Treeview(win, columns=columns, show='headings', height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    try:
        import psycopg2
        from config import DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            SELECT r.ReaderID, p.FirstName || ' ' || p.LastName AS FullName
            FROM Reader r
            JOIN Person p ON r.ReaderID = p.ID;
        ''')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        tk.Label(win, text=f"שגיאה: {e}", fg="red").pack()

def show_librarians_window(parent):
    win = tk.Toplevel(parent)
    win.title("מזהי ספרנים")
    win.geometry("350x350")
    columns = ["LibrarianID", "FullName"]
    tree = ttk.Treeview(win, columns=columns, show='headings', height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    try:
        import psycopg2
        from config import DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('''
            SELECT l.LibrarianID, p.FirstName || ' ' || p.LastName AS FullName
            FROM Librarian l
            JOIN Person p ON l.LibrarianID = p.ID;
        ''')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        tk.Label(win, text=f"שגיאה: {e}", fg="red").pack()

root.mainloop()
