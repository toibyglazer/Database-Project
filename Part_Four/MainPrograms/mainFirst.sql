CREATE OR REPLACE PROCEDURE public.main_borrow_program(
    IN p_reader_id INTEGER,
    IN p_book_id INTEGER,
    IN p_library_copy_id INTEGER,
    IN p_librarian_id INTEGER DEFAULT 801,
    OUT p_borrow_number INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_exists BOOLEAN;
    v_available_count INTEGER;
    v_copy_ok BOOLEAN;
BEGIN
    -- 1) ולידציית קורא
    SELECT EXISTS (SELECT 1 FROM public.Reader WHERE ReaderID = p_reader_id)
    INTO v_exists;
    IF NOT v_exists THEN
        RAISE EXCEPTION 'READER_NOT_FOUND: ReaderID % does not exist', p_reader_id
            USING ERRCODE = 'P0001';
    END IF;

    -- 2) ולידציית ספרן (ברירת מחדל 801, אך נבדוק קיום)
    SELECT EXISTS (SELECT 1 FROM public.Librarian WHERE LibrarianID = p_librarian_id)
    INTO v_exists;
    IF NOT v_exists THEN
        RAISE EXCEPTION 'LIBRARIAN_NOT_FOUND: LibrarianID % does not exist', p_librarian_id
            USING ERRCODE = 'P0001';
    END IF;

    -- 3) בדיקת זמינות כלשהי לספר
    SELECT COUNT(*) FROM public.check_book_availability(p_book_id) INTO v_available_count;
    IF COALESCE(v_available_count, 0) = 0 THEN
        -- ה-GUI יציג get_book_borrowers(p_book_id)
        RAISE EXCEPTION 'BOOK_NOT_AVAILABLE: No available copies for BookID %', p_book_id
            USING ERRCODE = 'P0001';
    END IF;

    -- 4) האם העותק המסוים זמין לספר הזה
    SELECT EXISTS (
        SELECT 1
        FROM public.check_book_availability(p_book_id) a
        WHERE a.library_copy_id = p_library_copy_id
    ) INTO v_copy_ok;

    IF NOT v_copy_ok THEN
        RAISE EXCEPTION 'COPY_NOT_AVAILABLE: LibraryCopyID % is not available for BookID %',
            p_library_copy_id, p_book_id
            USING ERRCODE = 'P0001';
    END IF;

    -- 5) ביצוע השאלה בפועל (מגן גם על מרוץ זמינות)
    BEGIN
        CALL public.create_new_borrow(p_reader_id, p_librarian_id, ARRAY[p_library_copy_id]);

        -- שליפת מספר ההשאלה האחרון לקורא זה
        SELECT MAX(BorrowNumber)
        INTO p_borrow_number
        FROM public.Borrow
        WHERE ReaderID = p_reader_id;

        IF p_borrow_number IS NULL THEN
            RAISE EXCEPTION 'BORROW_CREATE_FAILED: BorrowNumber not found after creation'
                USING ERRCODE = 'P0001';
        END IF;

        RAISE NOTICE 'Borrow created successfully. BorrowNumber: %', p_borrow_number;
    EXCEPTION
        WHEN OTHERS THEN
            IF POSITION('books already borrowed' IN SQLERRM) > 0
               OR POSITION('already borrowed' IN SQLERRM) > 0 THEN
                RAISE EXCEPTION 'COPY_TAKEN: The selected copy was just borrowed by someone else. Choose another copy.'
                    USING ERRCODE = 'P0001';
            ELSE
                RAISE;
            END IF;
    END;
END;
$$;