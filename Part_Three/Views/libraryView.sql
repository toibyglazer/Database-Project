-- View 2: From the received department's perspective - detailed borrowing and fines information
CREATE VIEW BorrowingAndFinesDetails AS
SELECT 
    b.borrow_number,
    p.pname AS ReaderName,
    r.phone_number AS ReaderPhone,
    r.birth_day,
    r.join_date,
    b.borrow_date,
    b.return_date,
    b.was_returned,
    CASE 
        WHEN b.return_date < CURRENT_DATE AND b.was_returned = FALSE THEN 'Overdue'
        WHEN b.was_returned = TRUE THEN 'Returned'
        ELSE 'Active'
    END AS BorrowStatus,
    f.fine_number,
    f.reason AS FineReason,
    f.fine_sum,
    f.receive_date AS FineDate,
    f.was_paid AS FinePaid,
    lib.pname AS LibrarianName,
    lib_details.email AS LibrarianEmail
FROM Borrow b
JOIN Take t ON b.borrow_number = t.borrow_number
JOIN Reader r ON t.pid = r.pid
JOIN Person p ON r.pid = p.pid
JOIN Librarian lib_l ON b.pid = lib_l.pid
JOIN Person lib ON lib_l.pid = lib.pid
JOIN Librarian lib_details ON lib_l.pid = lib_details.pid
LEFT JOIN Fine f ON b.borrow_number = f.borrow_number;

-- Comments:
-- This view shows borrowing transactions and related fines from the receiving department’s perspective.
-- It includes reader info, borrowing and return dates, fine details, and payment status.
-- The CASE statement categorizes borrowing status as 'Overdue', 'Returned', or 'Active' for easy tracking.
-- JOINs gather all necessary personal and transaction data.
-- LEFT JOIN ensures borrowings without fines are also shown.
-- Librarian contact info is included to support communication and oversight.
-- Designed to simplify management of lending and fines clearly and efficiently.
