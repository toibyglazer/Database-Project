# db_manager.py
import psycopg2
from config import DB_CONFIG

def get_all_readers():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.firstname, p.lastname, p.phonenumber, p.email, p.birthdate,
                   r.booklimit, r.numtakenbooks, r.joindate
            FROM person p
            JOIN reader r ON p.id = r.readerid
            ORDER BY p.id;
        """)
        readers = cur.fetchall()
        print(f"Found {len(readers)} readers")
        cur.close()
        conn.close()
        return readers
    except Exception as e:
        print("Error fetching readers:", e)
        return []

def add_reader(firstname, lastname, phonenumber=None, email=None, birthdate=None,
               booklimit=5, numtakenbooks=0):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO person (firstname, lastname, phonenumber, email, birthdate)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (firstname, lastname, phonenumber, email, birthdate))
        new_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO reader (readerid, booklimit, numtakenbooks)
            VALUES (%s, %s, %s);
        """, (new_id, booklimit, numtakenbooks))
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Error adding reader:", e)
        try:
            conn.rollback()
        except:
            pass
        return None

def update_reader(reader_id, firstname=None, lastname=None, phonenumber=None, email=None,
                  booklimit=None, numtakenbooks=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if firstname is not None:
            cur.execute("UPDATE person SET firstname=%s WHERE id=%s;", (firstname, reader_id))
        if lastname is not None:
            cur.execute("UPDATE person SET lastname=%s WHERE id=%s;", (lastname, reader_id))
        if phonenumber is not None:
            cur.execute("UPDATE person SET phonenumber=%s WHERE id=%s;", (phonenumber, reader_id))
        if email is not None:
            cur.execute("UPDATE person SET email=%s WHERE id=%s;", (email, reader_id))
        if booklimit is not None:
            cur.execute("UPDATE reader SET booklimit=%s WHERE readerid=%s;", (booklimit, reader_id))
        if numtakenbooks is not None:
            cur.execute("UPDATE reader SET numtakenbooks=%s WHERE readerid=%s;", (numtakenbooks, reader_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating reader:", e)
        try:
            conn.rollback()
        except:
            pass
        return False

def delete_reader(reader_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # המחיקה היא מטבלת person על פי id
        cur.execute("DELETE FROM person WHERE id=%s;", (reader_id,))
        deleted = cur.rowcount  # כמה שורות נמחקו בפועל
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0  # רק אם נמחקה שורה אחת לפחות
    except Exception as e:
        print("Error deleting reader:", e)
        try:
            conn.rollback()
        except:
            pass
        return False

def get_all_bookstoreinventory():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT booklanguageid, bookstoreprice, stockquantity FROM BookstoreInventory ORDER BY booklanguageid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching BookstoreInventory:", e)
        return []

def add_bookstoreinventory(booklanguageid, bookstoreprice, stockquantity=0):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO BookstoreInventory (booklanguageid, bookstoreprice, stockquantity)
            VALUES (%s, %s, %s);
        """, (booklanguageid, bookstoreprice, stockquantity))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error adding BookstoreInventory:", e)
        try:
            conn.rollback()
        except:
            pass
        return False

def update_bookstoreinventory(booklanguageid, bookstoreprice=None, stockquantity=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if bookstoreprice is not None:
            cur.execute("UPDATE BookstoreInventory SET bookstoreprice=%s WHERE booklanguageid=%s;", (bookstoreprice, booklanguageid))
        if stockquantity is not None:
            cur.execute("UPDATE BookstoreInventory SET stockquantity=%s WHERE booklanguageid=%s;", (stockquantity, booklanguageid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating BookstoreInventory:", e)
        try:
            conn.rollback()
        except:
            pass
        return False

def delete_bookstoreinventory(booklanguageid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM BookstoreInventory WHERE booklanguageid=%s;", (booklanguageid,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting BookstoreInventory:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def get_all_booklanguage():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT booklanguageid, bookid, languageid FROM BookLanguage ORDER BY booklanguageid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching BookLanguage:", e)
        return []

def add_booklanguage(bookid, languageid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO BookLanguage (bookid, languageid)
            VALUES (%s, %s)
            RETURNING booklanguageid;
        """, (bookid, languageid))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Error adding BookLanguage:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def update_booklanguage(booklanguageid, bookid=None, languageid=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if bookid is not None:
            cur.execute("UPDATE BookLanguage SET bookid=%s WHERE booklanguageid=%s;", (bookid, booklanguageid))
        if languageid is not None:
            cur.execute("UPDATE BookLanguage SET languageid=%s WHERE booklanguageid=%s;", (languageid, booklanguageid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating BookLanguage:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_booklanguage(booklanguageid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM BookLanguage WHERE booklanguageid=%s;", (booklanguageid,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting BookLanguage:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def get_all_language():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT languageid, languagename, maincountry FROM Language ORDER BY languageid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching Language:", e)
        return []

def add_language(languagename, maincountry=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Language (languagename, maincountry)
            VALUES (%s, %s)
            RETURNING languageid;
        """, (languagename, maincountry))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Error adding Language:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def update_language(languageid, languagename=None, maincountry=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if languagename is not None:
            cur.execute("UPDATE Language SET languagename=%s WHERE languageid=%s;", (languagename, languageid))
        if maincountry is not None:
            cur.execute("UPDATE Language SET maincountry=%s WHERE languageid=%s;", (maincountry, languageid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating Language:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_language(languageid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM Language WHERE languageid=%s;", (languageid,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting Language:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def get_all_books():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT bookid, title, authorid, agegroup, publicationyear, publishing FROM Book ORDER BY bookid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching Books:", e)
        return []

def add_book(title, authorid, agegroup, publicationyear=None, publishing=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Book (title, authorid, agegroup, publicationyear, publishing)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING bookid;
        """, (title, authorid, agegroup, publicationyear, publishing))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Error adding Book:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def update_book(bookid, title=None, authorid=None, agegroup=None, publicationyear=None, publishing=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if title is not None:
            cur.execute("UPDATE Book SET title=%s WHERE bookid=%s;", (title, bookid))
        if authorid is not None:
            cur.execute("UPDATE Book SET authorid=%s WHERE bookid=%s;", (authorid, bookid))
        if agegroup is not None:
            cur.execute("UPDATE Book SET agegroup=%s WHERE bookid=%s;", (agegroup, bookid))
        if publicationyear is not None:
            cur.execute("UPDATE Book SET publicationyear=%s WHERE bookid=%s;", (publicationyear, bookid))
        if publishing is not None:
            cur.execute("UPDATE Book SET publishing=%s WHERE bookid=%s;", (publishing, bookid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating Book:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_book(bookid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM Book WHERE bookid=%s;", (bookid,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting Book:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def get_all_librarycopies():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT librarycopyid, booklanguageid, copysource, shelflocationid, donorid, copycondition FROM LibraryCopy ORDER BY librarycopyid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching LibraryCopy:", e)
        return []

def add_librarycopy(booklanguageid, copysource, shelflocationid=None, donorid=None, copycondition=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO LibraryCopy (booklanguageid, copysource, shelflocationid, donorid, copycondition)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING librarycopyid;
        """, (booklanguageid, copysource, shelflocationid, donorid, copycondition))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Error adding LibraryCopy:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def update_librarycopy(librarycopyid, booklanguageid=None, copysource=None, shelflocationid=None, donorid=None, copycondition=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if booklanguageid is not None:
            cur.execute("UPDATE LibraryCopy SET booklanguageid=%s WHERE librarycopyid=%s;", (booklanguageid, librarycopyid))
        if copysource is not None:
            cur.execute("UPDATE LibraryCopy SET copysource=%s WHERE librarycopyid=%s;", (copysource, librarycopyid))
        if shelflocationid is not None:
            cur.execute("UPDATE LibraryCopy SET shelflocationid=%s WHERE librarycopyid=%s;", (shelflocationid, librarycopyid))
        if donorid is not None:
            cur.execute("UPDATE LibraryCopy SET donorid=%s WHERE librarycopyid=%s;", (donorid, librarycopyid))
        if copycondition is not None:
            cur.execute("UPDATE LibraryCopy SET copycondition=%s WHERE librarycopyid=%s;", (copycondition, librarycopyid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating LibraryCopy:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_librarycopy(librarycopyid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM LibraryCopy WHERE librarycopyid=%s;", (librarycopyid,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting LibraryCopy:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def get_all_borrows():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT borrownumber, readerid, librarianid, borrowdate, returndate, wasreturned FROM Borrow ORDER BY borrownumber;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching Borrow:", e)
        return []

def add_borrow(readerid, librarianid, returndate=None, wasreturned=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Borrow (readerid, librarianid, returndate, wasreturned)
            VALUES (%s, %s, %s, %s)
            RETURNING borrownumber;
        """, (readerid, librarianid, returndate, wasreturned))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Error adding Borrow:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def update_borrow(borrownumber, readerid=None, librarianid=None, returndate=None, wasreturned=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if readerid is not None:
            cur.execute("UPDATE Borrow SET readerid=%s WHERE borrownumber=%s;", (readerid, borrownumber))
        if librarianid is not None:
            cur.execute("UPDATE Borrow SET librarianid=%s WHERE borrownumber=%s;", (librarianid, borrownumber))
        if returndate is not None:
            cur.execute("UPDATE Borrow SET returndate=%s WHERE borrownumber=%s;", (returndate, borrownumber))
        if wasreturned is not None:
            cur.execute("UPDATE Borrow SET wasreturned=%s WHERE borrownumber=%s;", (wasreturned, borrownumber))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating Borrow:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_borrow(borrownumber):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM Borrow WHERE borrownumber=%s;", (borrownumber,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting Borrow:", e)
        try:
            conn.rollback()
        except:
            pass
        raise





def get_all_borrowed():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT borrownumber, librarycopyid FROM Borrowed ORDER BY borrownumber, librarycopyid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching Borrowed:", e)
        return []

def add_borrowed(borrownumber, librarycopyid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Borrowed (borrownumber, librarycopyid)
            VALUES (%s, %s)
        """, (borrownumber, librarycopyid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error adding Borrowed:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_borrowed(borrownumber, librarycopyid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM Borrowed WHERE borrownumber=%s AND librarycopyid=%s;", (borrownumber, librarycopyid))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting Borrowed:", e)
        try:
            conn.rollback()
        except:
            pass
        raise





def get_all_orders():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT orderid, orderdate, ordertype, finalprice, sellerid, customerid FROM Orders ORDER BY orderid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching Orders:", e)
        return []

def add_order(ordertype, finalprice=None, sellerid=None, customerid=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Orders (ordertype, finalprice, sellerid, customerid)
            VALUES (%s, %s, %s, %s)
            RETURNING orderid;
        """, (ordertype, finalprice, sellerid, customerid))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id
    except Exception as e:
        print("Error adding Order:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def update_order(orderid, ordertype=None, finalprice=None, sellerid=None, customerid=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if ordertype is not None:
            cur.execute("UPDATE Orders SET ordertype=%s WHERE orderid=%s;", (ordertype, orderid))
        if finalprice is not None:
            cur.execute("UPDATE Orders SET finalprice=%s WHERE orderid=%s;", (finalprice, orderid))
        if sellerid is not None:
            cur.execute("UPDATE Orders SET sellerid=%s WHERE orderid=%s;", (sellerid, orderid))
        if customerid is not None:
            cur.execute("UPDATE Orders SET customerid=%s WHERE orderid=%s;", (customerid, orderid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating Order:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_order(orderid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM Orders WHERE orderid=%s;", (orderid,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting Order:", e)
        try:
            conn.rollback()
        except:
            pass
        raise





def get_all_orderitems():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT orderid, booklanguageid, quantity FROM OrderItem ORDER BY orderid, booklanguageid;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching OrderItem:", e)
        return []

def add_orderitem(orderid, booklanguageid, quantity):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO OrderItem (orderid, booklanguageid, quantity)
            VALUES (%s, %s, %s)
        """, (orderid, booklanguageid, quantity))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error adding OrderItem:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def update_orderitem(orderid, booklanguageid, quantity):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE OrderItem SET quantity=%s WHERE orderid=%s AND booklanguageid=%s;", (quantity, orderid, booklanguageid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error updating OrderItem:", e)
        try:
            conn.rollback()
        except:
            pass
        raise

def delete_orderitem(orderid, booklanguageid):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM OrderItem WHERE orderid=%s AND booklanguageid=%s;", (orderid, booklanguageid))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return deleted > 0
    except Exception as e:
        print("Error deleting OrderItem:", e)
        try:
            conn.rollback()
        except:
            pass
        raise





def get_all_available_copies():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_all_available_copies();")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error fetching available copies:", e)
        return []





def check_book_availability_db(book_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM check_book_availability(%s);", (book_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error in check_book_availability_db:", e)
        raise





def get_book_borrowers_db(book_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_book_borrowers(%s);", (book_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error in get_book_borrowers_db:", e)
        raise





def get_book_copy_count_db(book_id=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if book_id is not None:
            cur.execute("SELECT * FROM get_book_copy_count(%s);", (book_id,))
        else:
            cur.execute("SELECT * FROM get_book_copy_count();")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error in get_book_copy_count_db:", e)
        raise





def get_top_selling_books_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_top_selling_books();")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error in get_top_selling_books_db:", e)
        raise





def get_available_copies_db(book_id=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if book_id is not None:
            cur.execute("SELECT * FROM get_available_copies(%s);", (book_id,))
        else:
            cur.execute("SELECT * FROM get_available_copies();")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error in get_available_copies_db:", e)
        raise





def get_current_borrowers_db(book_id=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if book_id is not None:
            cur.execute("SELECT * FROM get_current_borrowers(%s);", (book_id,))
        else:
            cur.execute("SELECT * FROM get_current_borrowers();")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error in get_current_borrowers_db:", e)
        raise





# --- Analytics/statistics functions ---
def get_bookstore_analytics_db():
    """
    Calls the get_bookstore_analytics() SQL function and returns the result as a Python dict.
    """
    import json
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT get_bookstore_analytics();")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        # תיקון: אם כבר dict, לא לעשות json.loads
        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            return json.loads(result)
        else:
            return None
    except Exception as e:
        print("Error in get_bookstore_analytics_db:", e)
        raise

def get_library_analytics_db():
    """
    Calls the get_library_analytics() SQL function and returns the result as a Python dict.
    """
    import json
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT get_library_analytics();")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        # תיקון: אם כבר dict, לא לעשות json.loads
        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            return json.loads(result)
        else:
            return None
    except Exception as e:
        print("Error in get_library_analytics_db:", e)
        raise

def get_low_stock_books_with_author():
    import psycopg2
    import psycopg2.extras
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('''
                SELECT 
                    b.BookID,
                    b.Title as book_name,
                    p.FirstName || ' ' || p.LastName as author_name,
                    a.Nationality as author_nationality,
                    l.LanguageName as language,
                    bi.StockQuantity as stock_quantity,
                    bi.BookstorePrice as price,
                    g.GenreName as genre,
                    COALESCE(SUM(oi.Quantity), 0) as total_sold
                FROM BookstoreInventory bi
                JOIN BookLanguage bl ON bi.BookLanguageID = bl.BookLanguageID
                JOIN Book b ON bl.BookID = b.BookID
                JOIN Author a ON b.AuthorID = a.AuthorID
                JOIN Person p ON a.AuthorID = p.ID
                JOIN Language l ON bl.LanguageID = l.LanguageID
                JOIN GenreType gt ON b.BookID = gt.BookID
                JOIN Genre g ON gt.GenreID = g.GenreID
                LEFT JOIN OrderItem oi ON bi.BookLanguageID = oi.BookLanguageID
                WHERE bi.StockQuantity < 5
                GROUP BY b.BookID, b.Title, p.FirstName, p.LastName, a.Nationality, 
                         l.LanguageName, bi.StockQuantity, bi.BookstorePrice, g.GenreName
                ORDER BY bi.StockQuantity ASC, total_sold DESC;
            ''')
            return cur.fetchall()
    finally:
        conn.close()

def get_last_10_orders_with_customer_seller():
    import psycopg2
    import psycopg2.extras
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('''
                SELECT 
                    o.OrderID,
                    p_customer.FirstName || ' ' || p_customer.LastName as customer_name,
                    c.CustomerType as customer_type,
                    c.Discount as customer_discount,
                    p_seller.FirstName || ' ' || p_seller.LastName as seller_name,
                    s.ExperienceYears as seller_experience,
                    o.OrderDate,
                    COUNT(oi.BookLanguageID) as items_count,
                    o.FinalPrice as total_price,
                    STRING_AGG(b.Title, ', ') as books_ordered
                FROM Orders o
                JOIN Customer c ON o.CustomerID = c.CustomerID
                JOIN Person p_customer ON c.CustomerID = p_customer.ID
                LEFT JOIN Seller s ON o.SellerID = s.SellerID
                LEFT JOIN Person p_seller ON s.SellerID = p_seller.ID
                LEFT JOIN OrderItem oi ON o.OrderID = oi.OrderID
                LEFT JOIN BookLanguage bl ON oi.BookLanguageID = bl.BookLanguageID
                LEFT JOIN Book b ON bl.BookID = b.BookID
                GROUP BY o.OrderID, p_customer.FirstName, p_customer.LastName, c.CustomerType, 
                         c.Discount, p_seller.FirstName, p_seller.LastName, s.ExperienceYears, 
                         o.OrderDate, o.FinalPrice
                ORDER BY o.OrderDate DESC
                LIMIT 10;
            ''')
            return cur.fetchall()
    finally:
        conn.close()

def get_last_10_fines_with_reader_librarian():
    import psycopg2
    import psycopg2.extras
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('''
                SELECT 
                    f.FineID as fine_number,
                    f.BorrowNumber as borrow_id,
                    p_reader.FirstName || ' ' || p_reader.LastName as reader_name,
                    p_reader.PhoneNumber as reader_phone,
                    r.numTakenBooks as reader_current_books,
                    p_librarian.FirstName || ' ' || p_librarian.LastName as librarian_name,
                    b.BorrowDate,
                    b.ReturnDate,
                    f.ReceiveDate as fine_date,
                    f.Sum as fine_amount,
                    f.Reason as fine_reason,
                    f.WasPaid as is_paid,
                    CASE 
                        WHEN b.ReturnDate IS NULL THEN CURRENT_DATE - b.BorrowDate
                        ELSE b.ReturnDate - b.BorrowDate
                    END as days_borrowed,
                    STRING_AGG(bk.Title, ', ') as borrowed_books
                FROM Fine f
                JOIN Borrow b ON f.BorrowNumber = b.BorrowNumber
                JOIN Reader r ON b.ReaderID = r.ReaderID
                JOIN Person p_reader ON r.ReaderID = p_reader.ID
                JOIN Librarian lib ON b.LibrarianID = lib.LibrarianID
                JOIN Person p_librarian ON lib.LibrarianID = p_librarian.ID
                LEFT JOIN Borrowed br ON b.BorrowNumber = br.BorrowNumber
                LEFT JOIN LibraryCopy lc ON br.LibraryCopyID = lc.LibraryCopyID
                LEFT JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
                LEFT JOIN Book bk ON bl.BookID = bk.BookID
                GROUP BY f.FineID, f.BorrowNumber, p_reader.FirstName, p_reader.LastName, 
                         p_reader.PhoneNumber, r.numTakenBooks, p_librarian.FirstName, 
                         p_librarian.LastName, b.BorrowDate, b.ReturnDate, f.ReceiveDate, 
                         f.Sum, f.Reason, f.WasPaid
                ORDER BY f.ReceiveDate DESC
                LIMIT 10;
            ''')
            return cur.fetchall()
    finally:
        conn.close()

def get_books_by_genre_and_age_group(genre=None, age_group=None):
    import psycopg2
    import psycopg2.extras
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            base_query = '''
                SELECT 
                    b.BookID,
                    b.Title as book_name,
                    p.FirstName || ' ' || p.LastName as author_name,
                    b.AgeGroup,
                    g.GenreName as genre,
                    b.PublicationYear,
                    b.Publishing,
                    COUNT(DISTINCT bl.LanguageID) as available_languages,
                    STRING_AGG(DISTINCT l.LanguageName, ', ') as languages_list,
                    COALESCE(bi.BookstorePrice, 0) as bookstore_price,
                    COALESCE(bi.StockQuantity, 0) as bookstore_stock,
                    COUNT(DISTINCT lc.LibraryCopyID) as library_copies,
                    COUNT(DISTINCT CASE WHEN lc.CopyCondition = 'Excellent' THEN lc.LibraryCopyID END) as excellent_copies
                FROM Book b
                JOIN Author a ON b.AuthorID = a.AuthorID
                JOIN Person p ON a.AuthorID = p.ID
                JOIN GenreType gt ON b.BookID = gt.BookID
                JOIN Genre g ON gt.GenreID = g.GenreID
                JOIN BookLanguage bl ON b.BookID = bl.BookID
                JOIN Language l ON bl.LanguageID = l.LanguageID
                LEFT JOIN BookstoreInventory bi ON bl.BookLanguageID = bi.BookLanguageID
                LEFT JOIN LibraryCopy lc ON bl.BookLanguageID = lc.BookLanguageID
            '''
            where_clauses = []
            params = []
            if genre:
                where_clauses.append('g.GenreName = %s')
                params.append(genre)
            if age_group:
                where_clauses.append('b.AgeGroup = %s')
                params.append(age_group)
            if where_clauses:
                base_query += ' WHERE ' + ' AND '.join(where_clauses)
            base_query += '''
                GROUP BY b.BookID, b.Title, p.FirstName, p.LastName, b.AgeGroup, 
                         g.GenreName, b.PublicationYear, b.Publishing, bi.BookstorePrice, bi.StockQuantity
                ORDER BY b.Title;
            '''
            cur.execute(base_query, params)
            return cur.fetchall()
    finally:
        conn.close()

def check_reader_exists(reader_id):
    """Returns True if a reader with the given ID exists, else False."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM reader WHERE readerid=%s;", (reader_id,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking reader existence: {e}")
        return False

def check_librarian_exists(librarian_id):
    """Returns True if a librarian with the given ID exists, else False."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM librarian WHERE librarianid=%s;", (librarian_id,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking librarian existence: {e}")
        return False

def check_customer_exists(customer_id):
    """Returns True if a customer with the given ID exists, else False."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM customer WHERE customerid=%s;", (customer_id,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking customer existence: {e}")
        return False

def check_seller_exists(seller_id):
    """Returns True if a seller with the given ID exists, else False."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM seller WHERE sellerid=%s;", (seller_id,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking seller existence: {e}")
        return False

def get_customer_type(customer_id):
    """Returns the CustomerType ('Library' or 'Individual') for the given customer_id, or None if not found."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT CustomerType FROM Customer WHERE CustomerID=%s;", (customer_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return row[0]
        return None
    except Exception as e:
        print(f"Error getting customer type: {e}")
        return None




