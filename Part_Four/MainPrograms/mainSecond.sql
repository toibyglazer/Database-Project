CREATE OR REPLACE PROCEDURE main_place_order_interactive()
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    v_customer_id INTEGER;
    v_order_id INTEGER;
    v_continue BOOLEAN := TRUE;
    v_booklanguage_id INTEGER;
    v_quantity INTEGER;
    v_stock INTEGER;
    v_error_occurred BOOLEAN := FALSE;  -- To track if an error occurred
BEGIN
    -- Step 1: Display top 10 best-selling books
    RAISE NOTICE '--- Top 10 Best-Selling Books ---';
    FOR rec IN SELECT * FROM get_top_selling_books() LOOP
        RAISE NOTICE 'Rank: %, BookLangID: %, Title: %, Author: %, Sold: %, Revenue: ₪%',
            rec.rank_position,
            rec.booklanguage_id,
            rec.book_title,
            rec.author_name,
            rec.total_copies_sold,
            rec.total_revenue;
    END LOOP;

    -- Step 2: Request customer ID
    RAISE NOTICE 'Please enter your Customer ID:';
    v_customer_id := 1201;  -- Example (can be replaced with user input)

    -- Step 3: Create a new order with initial total 0
    INSERT INTO Orders (OrderDate, OrderType, FinalPrice, SellerID, CustomerID)
    VALUES (CURRENT_DATE, 'Individual', 0, 1607, v_customer_id)
    RETURNING OrderID INTO v_order_id;

    -- Step 4: Loop to allow ordering multiple books with exception handling
    WHILE v_continue LOOP
        BEGIN
            -- Ask for BookLanguageID
            RAISE NOTICE 'Enter the BookLanguageID to order:';
            v_booklanguage_id := 302;  -- Example value, change as needed

            -- Check stock availability
            SELECT StockQuantity INTO v_stock
            FROM BookstoreInventory
            WHERE BookLanguageID = v_booklanguage_id;

            IF NOT FOUND THEN
                RAISE EXCEPTION 'No inventory found for BookLanguageID %', v_booklanguage_id;
            END IF;

            RAISE NOTICE 'Available stock for BookLanguageID %: % copies', v_booklanguage_id, v_stock;

            -- Ask for quantity
            RAISE NOTICE 'Enter quantity to order:';
            v_quantity := 12;  -- Intentionally large to trigger exception

            -- Validate stock
            IF v_quantity > v_stock THEN
                RAISE EXCEPTION 'Insufficient stock for BookLanguageID %: requested %, available %',
                    v_booklanguage_id, v_quantity, v_stock;
            END IF;

            -- Add item to order
            INSERT INTO OrderItem (OrderID, BookLanguageID, Quantity)
            VALUES (v_order_id, v_booklanguage_id, v_quantity);

            RAISE NOTICE 'Item added to order: BookLanguageID %, Quantity %', v_booklanguage_id, v_quantity;

            -- Ask whether to continue
            RAISE NOTICE 'Would you like to order another book? (true/false)';
            v_continue := FALSE;  -- For demo stop after one iteration

        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Error: %', SQLERRM;
                RAISE NOTICE 'Order cancelled due to error.';
                v_continue := FALSE;  -- stop the loop on error
                v_error_occurred := TRUE;  -- mark that an error occurred
        END;
    END LOOP;

    -- Step 5: Update the final price of the order only if no error occurred
    IF NOT v_error_occurred THEN
        UPDATE Orders
        SET FinalPrice = (
            SELECT COALESCE(SUM(oi.Quantity * bi.BookstorePrice), 0)
            FROM OrderItem oi
            JOIN BookstoreInventory bi ON oi.BookLanguageID = bi.BookLanguageID
            WHERE oi.OrderID = v_order_id
        )
        WHERE OrderID = v_order_id;

        RAISE NOTICE 'Order #% completed successfully.', v_order_id;
    ELSE
        RAISE NOTICE 'Order #% was not completed due to errors.', v_order_id;
    END IF;
END;
$$;

CALL main_place_order_interactive();
