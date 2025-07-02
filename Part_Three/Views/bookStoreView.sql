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


