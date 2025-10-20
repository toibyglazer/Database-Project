CREATE OR REPLACE PROCEDURE proc_borrow_specific_copy(
    IN p_reader_id INTEGER,
    IN p_library_copy_id INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_borrow_number INTEGER;
BEGIN
    -- Check if the copy is already borrowed and not returned
    IF EXISTS (
        SELECT 1 FROM Borrowed br
        JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
        WHERE br.LibraryCopyID = p_library_copy_id AND bo.WasReturned = FALSE
    ) THEN
        RAISE EXCEPTION 'This copy is already borrowed.';
    END IF;

    -- Create a new borrow record
    INSERT INTO Borrow (ReaderID, LibrarianID, BorrowDate)
    VALUES (p_reader_id, 801, CURRENT_DATE)
    RETURNING BorrowNumber INTO v_borrow_number;

    -- Link the selected copy to the borrow record
    INSERT INTO Borrowed (BorrowNumber, LibraryCopyID)
    VALUES (v_borrow_number, p_library_copy_id);
END;
$$;

CREATE OR REPLACE PROCEDURE proc_place_multi_book_order(
    IN p_customer_id INTEGER,
    IN p_booklanguage_ids INTEGER[],
    IN p_quantities INTEGER[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    v_order_id INTEGER;
    v_price_per_copy DECIMAL(10,2);
    v_temp_price DECIMAL(10,2);
    v_total_price DECIMAL(10,2) := 0;
    v_stock INTEGER;
BEGIN
    -- Step 0: Validate input arrays are of the same length
    IF array_length(p_booklanguage_ids, 1) IS DISTINCT FROM array_length(p_quantities, 1) THEN
        RAISE EXCEPTION 'BookLanguageID array and quantity array must be of the same length';
    END IF;

    -- Step 1: Create a new order header with initial price 0
    INSERT INTO Orders (OrderDate, OrderType, FinalPrice, SellerID, CustomerID)
    VALUES (CURRENT_DATE, 'Individual', 0, 1201, p_customer_id)
    RETURNING OrderID INTO v_order_id;

    -- Step 2: Iterate through each book to be added to the order
    FOR i IN 1 .. array_length(p_booklanguage_ids, 1) LOOP
        -- 2.1: Check stock availability
        SELECT StockQuantity INTO v_stock
        FROM BookstoreInventory
        WHERE BookLanguageID = p_booklanguage_ids[i];

        IF NOT FOUND THEN
            RAISE EXCEPTION 'BookLanguageID % not found in inventory', p_booklanguage_ids[i];
        ELSIF v_stock < p_quantities[i] THEN
            RAISE EXCEPTION 'Not enough stock for BookLanguageID %: Available %, Requested %',
                p_booklanguage_ids[i], v_stock, p_quantities[i];
        END IF;

        -- 2.2: Get the price per copy for the current book
        SELECT BookstorePrice INTO v_price_per_copy
        FROM BookstoreInventory
        WHERE BookLanguageID = p_booklanguage_ids[i];

        -- 2.3: Insert item into OrderItem table
        INSERT INTO OrderItem (OrderID, BookLanguageID, Quantity)
        VALUES (v_order_id, p_booklanguage_ids[i], p_quantities[i]);

        -- 2.4: Update running total price for the order
        v_temp_price := v_price_per_copy * p_quantities[i];
        v_total_price := v_total_price + v_temp_price;
    END LOOP;

    -- Step 3: Update the final price in the Orders table
    UPDATE Orders
    SET FinalPrice = v_total_price
    WHERE OrderID = v_order_id;

    -- Step 4: Display success message
    RAISE NOTICE 'Order % placed successfully with total price ₪%', v_order_id, v_total_price;
END;
$$;
CREATE OR REPLACE PROCEDURE create_new_borrow(
    IN p_reader_id INTEGER,
    IN p_librarian_id INTEGER,
    IN p_library_copy_ids INTEGER[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    copy_id INTEGER;
    unavailable_books TEXT := '';
    v_borrow_number INTEGER;
BEGIN
    -- בדיקת זמינות כל הספרים
    FOREACH copy_id IN ARRAY p_library_copy_ids
    LOOP
        IF EXISTS (
            SELECT 1 FROM Borrowed br
            JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
            WHERE br.LibraryCopyID = copy_id AND bo.WasReturned = FALSE
        ) THEN
            unavailable_books := unavailable_books || copy_id || ', ';
        END IF;
    END LOOP;

    -- אם יש ספרים לא זמינים - כשל
    IF unavailable_books != '' THEN
        RAISE EXCEPTION 'Cannot create borrow - books already borrowed: %', 
            TRIM(TRAILING ', ' FROM unavailable_books);
    END IF;

    -- יצירת השאלה חדשה
    INSERT INTO Borrow (ReaderID, LibrarianID, BorrowDate)
    VALUES (p_reader_id, p_librarian_id, CURRENT_DATE)
    RETURNING BorrowNumber INTO v_borrow_number;

    -- הוספת כל הספרים
    FOREACH copy_id IN ARRAY p_library_copy_ids
    LOOP
        INSERT INTO Borrowed (BorrowNumber, LibraryCopyID)
        VALUES (v_borrow_number, copy_id);
    END LOOP;

    RAISE NOTICE 'Borrow created successfully with ID: %', v_borrow_number;
END;
$$;

CREATE OR REPLACE PROCEDURE create_new_order(
    IN p_customer_id INTEGER,
    IN p_seller_id INTEGER,
    IN p_booklanguage_ids INTEGER[],
    IN p_quantities INTEGER[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    v_order_id INTEGER;
    v_price_per_copy DECIMAL(10,2);
    v_total_price DECIMAL(10,2) := 0;
    v_stock INTEGER;
    v_customer_discount DECIMAL(5,2);
    v_order_type order_type_enum;
    v_discounted_price DECIMAL(10,2);
    unavailable_items TEXT := '';
BEGIN
    -- ולידציה: אורך מערכים זהה
    IF array_length(p_booklanguage_ids, 1) IS DISTINCT FROM array_length(p_quantities, 1) THEN
        RAISE EXCEPTION 'BookLanguageID array and quantity array must be of the same length';
    END IF;

    -- פרטי לקוח (סוג הזמנה + הנחה)
    SELECT Discount, CustomerType INTO v_customer_discount, v_order_type
    FROM Customer
    WHERE CustomerID = p_customer_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Customer ID % not found', p_customer_id;
    END IF;

    -- בדיקת זמינות לכל הפריטים מראש
    FOR i IN 1 .. array_length(p_booklanguage_ids, 1) LOOP
        SELECT StockQuantity INTO v_stock
        FROM BookstoreInventory
        WHERE BookLanguageID = p_booklanguage_ids[i];

        IF NOT FOUND THEN
            unavailable_items := unavailable_items || 'BookLanguageID ' || p_booklanguage_ids[i] || ' not found, ';
        ELSIF v_stock < p_quantities[i] THEN
            unavailable_items := unavailable_items || 'BookLanguageID ' || p_booklanguage_ids[i] ||
                ' insufficient stock (Available: ' || v_stock || ', Requested: ' || p_quantities[i] || '), ';
        END IF;
    END LOOP;

    IF unavailable_items <> '' THEN
        RAISE EXCEPTION 'Cannot create order - issues found: %',
            TRIM(TRAILING ', ' FROM unavailable_items);
    END IF;

    -- יצירת הזמנה
    INSERT INTO Orders (OrderDate, OrderType, FinalPrice, SellerID, CustomerID)
    VALUES (CURRENT_DATE, v_order_type, 0, p_seller_id, p_customer_id)
    RETURNING OrderID INTO v_order_id;

    -- הוספת פריטים + חישוב מחיר (הפחתת המלאי תתבצע ע"י הטריגר על OrderItem!)
    FOR i IN 1 .. array_length(p_booklanguage_ids, 1) LOOP
        SELECT BookstorePrice INTO v_price_per_copy
        FROM BookstoreInventory
        WHERE BookLanguageID = p_booklanguage_ids[i];

        INSERT INTO OrderItem (OrderID, BookLanguageID, Quantity)
        VALUES (v_order_id, p_booklanguage_ids[i], p_quantities[i]);

        v_discounted_price := v_price_per_copy * (1 - v_customer_discount / 100);
        v_total_price := v_total_price + (v_discounted_price * p_quantities[i]);
        -- >>> הוסר: UPDATE BookstoreInventory ... (מטופל ע"י הטריגר) <<<
    END LOOP;

    -- עדכון מחיר סופי
    UPDATE Orders
    SET FinalPrice = v_total_price
    WHERE OrderID = v_order_id;

    RAISE NOTICE 'Order % created successfully. Total price: %', v_order_id, v_total_price;
END;
$$;
