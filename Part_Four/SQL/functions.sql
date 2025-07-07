CREATE OR REPLACE FUNCTION get_all_available_copies()
RETURNS TABLE (
    BookID INTEGER,                      -- ID of the book
    Title VARCHAR,                       -- Title of the book
    LibraryCopyID INTEGER,              -- ID of the specific physical library copy
    LanguageName VARCHAR,               -- Language of the copy
    CopyCondition copy_condition_enum,  -- Condition of the copy (e.g., new, good, worn)
    ShelfNumber INTEGER,                -- Shelf number in the library
    Floor INTEGER,                      -- Floor number where the shelf is located
    RowNum INTEGER                      -- Row number within the shelf
) 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Returns all available (not currently borrowed) library copies, including their location and metadata
    RETURN QUERY
    SELECT 
        b.BookID,                       -- Book identifier
        b.Title,                        -- Book title
        lc.LibraryCopyID,              -- Physical copy ID in the library
        l.LanguageName,                -- Language of the copy
        lc.CopyCondition,              -- Condition status of the copy
        sl.ShelfNumber,                -- Shelf location details
        sl.Floor,
        sl.RowNum
    FROM LibraryCopy lc
    JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID     -- Join to get book and language info
    JOIN Book b ON bl.BookID = b.BookID                                -- Book details
    JOIN Language l ON bl.LanguageID = l.LanguageID                    -- Language name
    LEFT JOIN ShelfLocation sl ON lc.ShelfLocationID = sl.ShelfLocationID -- Optional location info
    WHERE lc.LibraryCopyID NOT IN (                                   -- Filter out borrowed books
        SELECT br.LibraryCopyID
        FROM Borrowed br
        JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
        WHERE bo.WasReturned = FALSE                                   -- Still on loan
    );
END;
$$;


-- Function: Returns available copies of a specific book in the library
CREATE OR REPLACE FUNCTION check_book_availability(book_id INTEGER)
RETURNS TABLE (
    library_copy_id INTEGER,        -- ID of the available library copy
    language_name VARCHAR(100),    -- Language of the copy
    copy_condition VARCHAR(20),    -- Physical condition of the copy
    shelf_number INTEGER,          -- Shelf number where the copy is located
    floor INTEGER,                 -- Floor in the library
    row_num INTEGER                -- Row number on the shelf
) 
LANGUAGE plpgsql
AS $$
DECLARE
    copy_rec RECORD;               -- Temporary record for looping over available copies
    available_count INTEGER := 0;  -- Number of available copies
    total_copies INTEGER := 0;     -- Total number of copies in the library
    cur_available CURSOR FOR       -- Cursor for fetching available copies
        SELECT DISTINCT
            lc.LibraryCopyID,
            l.LanguageName,
            lc.CopyCondition,
            sl.ShelfNumber,
            sl.Floor,
            sl.RowNum
        FROM LibraryCopy lc
        JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
        JOIN Language l ON bl.LanguageID = l.LanguageID
        LEFT JOIN ShelfLocation sl ON lc.ShelfLocationID = sl.ShelfLocationID
        WHERE bl.BookID = book_id
        AND lc.LibraryCopyID NOT IN (
            SELECT br.LibraryCopyID
            FROM Borrowed br
            JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
            WHERE bo.WasReturned = FALSE
        );
BEGIN
    -- Check if the book exists in the library
    SELECT COUNT(*) INTO total_copies
    FROM Book b
    JOIN BookLanguage bl ON b.BookID = bl.BookID
    JOIN LibraryCopy lc ON bl.BookLanguageID = lc.BookLanguageID
    WHERE b.BookID = book_id;
    
    IF total_copies = 0 THEN
        RAISE EXCEPTION 'Book with ID % not found in library', book_id;
    END IF;

    -- Count how many available (not currently borrowed) copies exist
    SELECT COUNT(*) INTO available_count
    FROM LibraryCopy lc
    JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
    WHERE bl.BookID = book_id
    AND lc.LibraryCopyID NOT IN (
        SELECT br.LibraryCopyID
        FROM Borrowed br
        JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
        WHERE bo.WasReturned = FALSE
    );
    
    -- Return each available copy
    IF available_count > 0 THEN
        FOR copy_rec IN cur_available LOOP
            library_copy_id := copy_rec.LibraryCopyID;
            language_name := copy_rec.LanguageName;
            copy_condition := copy_rec.CopyCondition::VARCHAR;
            shelf_number := copy_rec.ShelfNumber;
            floor := copy_rec.Floor;
            row_num := copy_rec.RowNum;
            RETURN NEXT;
        END LOOP;
    ELSE
        -- If all copies are borrowed
        RAISE NOTICE 'No copies available for book ID % - all copies are currently borrowed', book_id;
        RETURN;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in check_book_availability: %', SQLERRM;
        RAISE;
END;
$$;
-- Function: Returns a list of current borrowers for a specific book
CREATE OR REPLACE FUNCTION get_book_borrowers(book_id INTEGER)
RETURNS TABLE (
    library_copy_id INTEGER,         -- Copy ID being borrowed
    book_title VARCHAR(255),         -- Title of the book
    language_name VARCHAR(100),      -- Language of the book
    reader_id INTEGER,               -- ID of the reader
    reader_full_name VARCHAR(200),   -- Reader's full name
    borrow_date DATE,                -- Date the book was borrowed
    expected_return_date DATE,       -- Due date for returning
    days_overdue INTEGER             -- Number of days the book is overdue (if any)
) 
LANGUAGE plpgsql
AS $$
DECLARE
    borrow_rec RECORD;              -- Temporary record to hold current borrow info
    borrowers_count INTEGER := 0;   -- Count of active borrowers
    cur_borrowed CURSOR FOR         -- Cursor to fetch current borrowers
        SELECT DISTINCT
            lc.LibraryCopyID,
            b.Title,
            l.LanguageName,
            r.ReaderID,
            CONCAT(p.FirstName, ' ', p.LastName) as full_name,
            bo.BorrowDate,
            bo.BorrowDate + INTERVAL '30 days' as expected_return,
            CASE 
                WHEN bo.BorrowDate + INTERVAL '30 days' < CURRENT_DATE 
                THEN EXTRACT(DAY FROM CURRENT_DATE - (bo.BorrowDate + INTERVAL '30 days'))::INTEGER
                ELSE 0
            END as overdue_days
        FROM LibraryCopy lc
        JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
        JOIN Book b ON bl.BookID = b.BookID
        JOIN Language l ON bl.LanguageID = l.LanguageID
        JOIN Borrowed br ON lc.LibraryCopyID = br.LibraryCopyID
        JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
        JOIN Reader r ON bo.ReaderID = r.ReaderID
        JOIN Person p ON r.ReaderID = p.ID
        WHERE b.BookID = book_id
        AND bo.WasReturned = FALSE;
BEGIN
    -- Check if the book exists
    IF NOT EXISTS (
        SELECT 1 FROM Book WHERE BookID = book_id
    ) THEN
        RAISE EXCEPTION 'Book with ID % not found', book_id;
    END IF;
    
    -- Count the number of current borrowers
    SELECT COUNT(*) INTO borrowers_count
    FROM LibraryCopy lc
    JOIN BookLanguage bl ON lc.BookLanguageID = bl.BookLanguageID
    JOIN Borrowed br ON lc.LibraryCopyID = br.LibraryCopyID
    JOIN Borrow bo ON br.BorrowNumber = bo.BorrowNumber
    WHERE bl.BookID = book_id
    AND bo.WasReturned = FALSE;
    
    IF borrowers_count = 0 THEN
        RAISE NOTICE 'No current borrowers found for book ID: %', book_id;
        RETURN;
    END IF;
    
    -- Return all active borrow records
    FOR borrow_rec IN cur_borrowed LOOP
        library_copy_id := borrow_rec.LibraryCopyID;
        book_title := borrow_rec.Title;
        language_name := borrow_rec.LanguageName;
        reader_id := borrow_rec.ReaderID;
        reader_full_name := borrow_rec.full_name;
        borrow_date := borrow_rec.BorrowDate;
        expected_return_date := borrow_rec.expected_return::DATE;
        days_overdue := borrow_rec.overdue_days;
        RETURN NEXT;
    END LOOP;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in get_book_borrowers: %', SQLERRM;
        RAISE;
END;
$$;
CREATE OR REPLACE FUNCTION get_top_selling_books()
RETURNS TABLE (
    rank_position INTEGER,           -- Ranking position based on sales
    booklanguage_id INTEGER,         -- BookLanguageID (specific language edition)
    book_title VARCHAR(255),         -- Title of the book
    author_name VARCHAR(200),        -- Author's first name only
    total_copies_sold BIGINT,        -- Total number of copies sold
    total_revenue DECIMAL(12,2)      -- Total revenue generated
) 
LANGUAGE plpgsql
AS $$
DECLARE
    book_rec RECORD;                 -- Temporary variable to hold current row from cursor
    current_rank INTEGER := 1;       -- Rank counter
    cur_top_books CURSOR FOR         -- Cursor to retrieve top 10 best-selling books
        SELECT 
            bl.BookLanguageID,
            b.Title,
            p.FirstName AS author_first_name,
            SUM(oi.Quantity) AS copies_sold,
            SUM(oi.Quantity * bi.BookstorePrice) AS revenue
        FROM Book b
        JOIN Author a ON b.AuthorID = a.AuthorID
        JOIN Person p ON a.AuthorID = p.ID
        JOIN BookLanguage bl ON b.BookID = bl.BookID
        JOIN BookstoreInventory bi ON bl.BookLanguageID = bi.BookLanguageID
        JOIN OrderItem oi ON bl.BookLanguageID = oi.BookLanguageID
        JOIN Orders o ON oi.OrderID = o.OrderID
        GROUP BY bl.BookLanguageID, b.Title, p.FirstName
        ORDER BY copies_sold DESC, revenue DESC
        LIMIT 10;
BEGIN
    -- Step 1: Ensure there is sales data available
    IF NOT EXISTS (SELECT 1 FROM OrderItem LIMIT 1) THEN
        RAISE NOTICE 'No sales data found in the system';
        RETURN;
    END IF;

    -- Step 2: Loop through cursor and return each book with its ranking and stats
    FOR book_rec IN cur_top_books LOOP
        rank_position := current_rank;
        booklanguage_id := book_rec.BookLanguageID;
        book_title := book_rec.Title;
        author_name := book_rec.author_first_name;
        total_copies_sold := book_rec.copies_sold;
        total_revenue := book_rec.revenue;

        current_rank := current_rank + 1;
        RETURN NEXT;
    END LOOP;

    -- If no books were returned at all
    IF current_rank = 1 THEN
        RAISE NOTICE 'No books found with sales data';
    END IF;

EXCEPTION
    -- Generic exception handling
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in get_top_selling_books: %', SQLERRM;
        RAISE;
END;
$$;
