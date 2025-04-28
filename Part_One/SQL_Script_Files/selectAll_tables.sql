-- Select all data from all tables
SELECT * FROM Person;
SELECT * FROM Customer;
SELECT * FROM Librarian;
SELECT * FROM ShelfLocation;
SELECT * FROM Author;
SELECT * FROM GenreTypes;
SELECT * FROM BookLanguage;
SELECT * FROM BookList;
SELECT * FROM Language;
SELECT * FROM Order_Table;
SELECT * FROM BookToOrder;

-- Count the number of records in each table
SELECT 'Person' AS table_name, COUNT(*) FROM Person;
SELECT 'Customer' AS table_name, COUNT(*) FROM Customer;
SELECT 'Librarian' AS table_name, COUNT(*) FROM Librarian;
SELECT 'ShelfLocation' AS table_name, COUNT(*) FROM ShelfLocation;
SELECT 'Author' AS table_name, COUNT(*) FROM Author;
SELECT 'GenreTypes' AS table_name, COUNT(*) FROM GenreTypes;
SELECT 'BookLanguage' AS table_name, COUNT(*) FROM BookLanguage;
SELECT 'BookList' AS table_name, COUNT(*) FROM BookList;
SELECT 'Language' AS table_name, COUNT(*) FROM Language;
SELECT 'Order_Table' AS table_name, COUNT(*) FROM Order_Table;
SELECT 'BookToOrder' AS table_name, COUNT(*) FROM BookToOrder;

-- Select data from related tables (with JOINs)

-- Display customers with their personal details
SELECT p.ID, p.FirstName, p.LastName, p.Email, p.PhoneNumber, 
       c.IDmember, c.Discount, c.StartYearMember
FROM Person p
JOIN Customer c ON p.ID = c.CustomerID;

-- Display books with their author and genre information
SELECT b.BookID, b.TitleBookName, b.PublicationYear, b.price, 
       a.FirstName AS AuthorFirstName, a.LastName AS AuthorLastName,
       g.GenreName
FROM BookList b
JOIN Author a ON b.AuthorID = a.AuthorID
JOIN GenreTypes g ON b.GenreID = g.GenreID;

-- Display books with their available languages
SELECT b.BookID, b.TitleBookName, 
       STRING_AGG(bl.LanguageName, ', ') AS AvailableLanguages
FROM BookList b
JOIN Language l ON b.BookID = l.BookID
JOIN BookLanguage bl ON l.LanguageID = bl.LanguageID
GROUP BY b.BookID, b.TitleBookName;

-- Display orders with customer, librarian and book details
SELECT o.OrderID, o.OrderDate, o.FinalPrice,
       p1.FirstName AS CustomerFirstName, p1.LastName AS CustomerLastName,
       p2.FirstName AS LibrarianFirstName, p2.LastName AS LibrarianLastName,
       b.TitleBookName
FROM Order_Table o
JOIN Customer c ON o.CustomerID = c.CustomerID
JOIN Person p1 ON c.CustomerID = p1.ID
JOIN Librarian l ON o.LibrarianID = l.LibrarianID
JOIN Person p2 ON l.LibrarianID = p2.ID
JOIN BookToOrder bo ON o.OrderID = bo.OrderID
JOIN BookList b ON bo.BookID = b.BookID;