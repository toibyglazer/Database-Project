-- View 1: From the original department's perspective - detailed customer orders information
CREATE VIEW CustomerOrderDetails AS
SELECT 
    o.OrderID,
    o.OrderDate,
    o.FinalPrice,
    p.FirstName || ' ' || p.LastName AS CustomerName,
    p.Email,
    c.Discount,
    c.StartYearMember,
    bl.TitleBookName,
    a.FirstName || ' ' || a.LastName AS AuthorName,
    gt.GenreName,
    bto.BookQuantity,
    bl.price AS BookPrice,
    (bl.price * bto.BookQuantity) AS TotalBookPrice,
    lib.FirstName || ' ' || lib.LastName AS LibrarianName
FROM Orders o
JOIN Customer c ON o.CustomerID = c.CustomerID
JOIN Person p ON c.CustomerID = p.ID
JOIN BookToOrder bto ON o.OrderID = bto.OrderID
JOIN BookList bl ON bto.BookID = bl.BookID
JOIN Author a ON bl.AuthorID = a.AuthorID
JOIN GenreTypes gt ON bl.GenreID = gt.GenreID
LEFT JOIN Librarian l ON o.LibrarianID = l.LibrarianID
LEFT JOIN Person lib ON l.LibrarianID = lib.ID;


-- Comments:
-- This view consolidates detailed order information from the customer department's perspective.
-- It combines order details, customer identity and contact, book information, and associated librarian data.
-- The use of JOINs ensures relevant data is gathered from multiple tables to provide a comprehensive picture of each order.
-- LEFT JOIN is used on Librarian and Person tables to accommodate orders that may not have an assigned librarian without excluding those records.
-- This structure supports rich queries on sales performance, customer behavior, and order fulfillment.
-- By calculating TotalBookPrice, the view facilitates revenue analysis at the book-item level within each order.

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
