-- Trigger function to update the number of books currently borrowed by a reader
CREATE OR REPLACE FUNCTION trg_update_reader_books()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment the numTakenBooks field in the Reader table by 1
    -- for the reader associated with the inserted borrow entry
    UPDATE Reader
    SET numTakenBooks = numTakenBooks + 1
    WHERE ReaderID = (
        SELECT ReaderID
        FROM Borrow
        WHERE BorrowNumber = NEW.BorrowNumber
    );

    -- Return the newly inserted row (mandatory for AFTER INSERT triggers)
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger definition: fires after inserting a row into the Borrowed table
-- Purpose: Automatically updates the reader's numTakenBooks count
CREATE TRIGGER trg_after_borrow_insert
AFTER INSERT ON Borrowed
FOR EACH ROW
EXECUTE FUNCTION trg_update_reader_books();

-- Trigger function to update inventory after a new order item is inserted
CREATE OR REPLACE FUNCTION trg_update_inventory_after_order()
RETURNS TRIGGER AS $$
BEGIN
    -- Subtract the ordered quantity from the stock of the corresponding book
    UPDATE BookstoreInventory
    SET StockQuantity = StockQuantity - NEW.Quantity
    WHERE BookLanguageID = NEW.BookLanguageID;

    -- Optional: You can add validation here to prevent negative stock levels

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger definition: fires after inserting a row into the OrderItem table
-- Purpose: Automatically updates inventory to reflect items sold
CREATE TRIGGER trg_after_orderitem_insert
AFTER INSERT ON OrderItem
FOR EACH ROW
EXECUTE FUNCTION trg_update_inventory_after_order();
