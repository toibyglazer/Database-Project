CREATE OR REPLACE PROCEDURE main_borrow_interactive()
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    v_book_id INTEGER;              -- The ID of the book the reader wants to borrow
    v_reader_id INTEGER;            -- The ID of the reader
    v_row_count INTEGER;            -- Used to detect if any available copies exist
    v_available BOOLEAN := FALSE;   -- Will be set to true if book has available copies
    v_booklanguage_id INTEGER;      -- The BookLanguageID of the selected copy
    v_library_copy_id INTEGER;      -- The specific LibraryCopyID chosen to borrow
BEGIN
    -- Simulated input for book ID (could be replaced with actual user input)
    RAISE NOTICE 'Please enter the BookID you want to borrow:';
    v_book_id := 343;  -- Replace with dynamic input in production

    -- Simulated input for reader ID
    RAISE NOTICE 'Please enter your ReaderID:';
    v_reader_id := 5;  -- Replace with dynamic input in production

    -- Check if any available copies exist for the selected book
    PERFORM 1 FROM check_book_availability(v_book_id) LIMIT 1;
    GET DIAGNOSTICS v_row_count = ROW_COUNT;
    v_available := (v_row_count > 0);

    IF v_available THEN
        RAISE NOTICE 'Available copies of BookID %:', v_book_id;

        -- Display all available copies with detailed information
        FOR rec IN SELECT * FROM check_book_availability(v_book_id) LOOP
            RAISE NOTICE 'CopyID: %, Language: %, Condition: %, Shelf: %, Floor: %, Row: %',
                rec.library_copy_id, rec.language_name, rec.copy_condition,
                rec.shelf_number, rec.floor, rec.row_num;
        END LOOP;

        -- Simulated selection of a specific copy to borrow
        RAISE NOTICE 'Please enter the LibraryCopyID you want to borrow:';
        v_library_copy_id := 8809;  -- Replace with dynamic input if needed

        -- Get the BookLanguageID for the selected copy
        SELECT BookLanguageID INTO v_booklanguage_id
        FROM LibraryCopy
        WHERE LibraryCopyID = v_library_copy_id;

        -- Borrow the book by calling the borrowing procedure
        CALL proc_borrow_book_by_lang_id(v_reader_id, v_booklanguage_id);

        RAISE NOTICE 'Borrow process completed successfully.';

    ELSE
        -- No available copies found, so show current borrowers of the book
        RAISE NOTICE 'No available copies. Showing current borrowers of BookID %:', v_book_id;

        FOR rec IN SELECT * FROM get_book_borrowers(v_book_id) LOOP
            RAISE NOTICE 'CopyID: %, ReaderID: %, Name: %, Borrowed: %, Overdue Days: %',
                rec.library_copy_id, rec.reader_id, rec.reader_full_name,
                rec.borrow_date, rec.days_overdue;
        END LOOP;

        RAISE NOTICE 'We will notify you when a copy becomes available.';
    END IF;
END;
$$;
