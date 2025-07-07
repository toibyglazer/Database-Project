-- ============================================
-- TEST SCRIPT FOR FUNCTIONALITY VALIDATION
-- ============================================
-- This file includes tests for the following components:
-- 1. check_book_availability (Function)
-- 2. get_book_borrowers (Function)
-- 3. get_top_selling_books (Function)
-- 4. proc_borrow_book_by_lang_id (Procedure)
-- 5. proc_place_order (Procedure)
-- 6. Triggers: trg_update_reader_books & trg_update_inventory_after_order

-- ============================================
-- PART 1: Initial Test on Book ID 343 - Availability & Borrowers
-- ============================================
-- Test: Check available copies for book ID 343 before any borrow
SELECT 'Testing available copies for book ID 343:' as test_description;
SELECT * FROM check_book_availability(343);

-- Test: Check that no current borrowers exist for book ID 343
SELECT 'Testing borrowers for book ID 343 (should be empty):' as test_description;
SELECT * FROM get_book_borrowers(343);

-- ============================================
-- PART 2: Insert Borrow Records & Re-run Tests
-- ============================================
-- Insert test borrow: Reader 1 borrows a copy of Book ID 343
INSERT INTO Borrow (ReaderID, LibrarianID, BorrowDate, WasReturned) 
VALUES (1, 801, CURRENT_DATE - INTERVAL '10 days', FALSE);

-- Link an available copy of Book ID 343 to the borrow above
INSERT INTO Borrowed (BorrowNumber, LibraryCopyID) 
SELECT currval('borrow_borrownumber_seq'), lc.LibraryCopyID
FROM LibraryCopy lc
JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
WHERE bl.BookID = 343
LIMIT 1;

-- Insert second borrow: Reader 2 borrows another available copy
INSERT INTO Borrow (ReaderID, LibrarianID, BorrowDate, WasReturned) 
VALUES (2, 802, CURRENT_DATE - INTERVAL '40 days', FALSE);

-- Link another available copy of Book ID 343 (not the one already borrowed)
INSERT INTO Borrowed (BorrowNumber, LibraryCopyID) 
SELECT currval('borrow_borrownumber_seq'), lc.LibraryCopyID
FROM LibraryCopy lc
JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
WHERE bl.BookID = 343
AND lc.LibraryCopyID NOT IN (
    SELECT LibraryCopyID FROM Borrowed
)
LIMIT 1;

-- Re-test: Check remaining available copies (should be less)
SELECT 'Testing with some copies borrowed - Available copies:' as test_description;
SELECT * FROM check_book_availability(343);

-- Re-test: Check current borrowers for book ID 343 (should return 2)
SELECT 'Testing with some copies borrowed - Current borrowers:' as test_description;
SELECT * FROM get_book_borrowers(343);

-- Additional: Test top selling books (output depends on data)
SELECT 'Testing top selling books:' as test_description;
SELECT * FROM get_top_selling_books();

-- ============================================
-- PART 3: Test Procedures & Triggers
-- ============================================
-- Test: Call borrow procedure for Reader 1 and BookLanguageID 686
CALL proc_borrow_book_by_lang_id(1, 686);

-- Verify the borrow was created
SELECT * FROM Borrow WHERE ReaderID = 1 ORDER BY BorrowDate DESC;

-- Verify the borrowed copy was linked properly
SELECT * FROM Borrowed WHERE BorrowNumber IN (SELECT BorrowNumber FROM Borrow WHERE ReaderID = 1);

-- Verify the reader's numTakenBooks was incremented (trigger test)
SELECT numTakenBooks FROM Reader WHERE ReaderID = 1;

-- Reset sequence for order ID to avoid conflict (if necessary)
SELECT setval('orders_orderid_seq', (SELECT MAX(orderid) FROM orders));

-- Check inventory before placing order
SELECT * FROM BookstoreInventory WHERE BookLanguageID = 5;

-- Test: Call place order procedure for Customer 1201, BookLanguageID 5, quantity 5
CALL proc_place_order(1201, 5, 5);

-- Check inventory after placing the order (should decrease)
SELECT * FROM BookstoreInventory WHERE BookLanguageID = 5;

-- Verify that a new order was inserted
SELECT * FROM Orders WHERE CustomerID = 1201 ORDER BY OrderID DESC LIMIT 1;

-- Verify that the order item was linked properly
SELECT * FROM OrderItem WHERE BookLanguageID = 5 ORDER BY OrderID DESC LIMIT 1;
