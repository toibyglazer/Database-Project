-- Insert data into Person table
INSERT INTO Person (ID, FirstName, LastName, Email, PhoneNumber, BirthDate)
VALUES 
(1, 'David', 'Cohen', 'david.cohen@email.com', '0501234567', '1985-05-15'),
(2, 'Sarah', 'Levy', 'sarah.levy@email.com', '0521234567', '1990-08-22'),
(3, 'Moshe', 'Goldberg', 'moshe.goldberg@email.com', '0531234567', '1978-03-10'),
(4, 'Yael', 'Avraham', 'yael.avraham@email.com', '0541234567', '1995-11-28'),
(5, 'Daniel', 'Mizrahi', 'daniel.mizrahi@email.com', '0551234567', '1982-07-03'),
(6, 'Tamar', 'Katz', 'tamar.katz@email.com', '0561234567', '1988-12-17'),
(7, 'Avi', 'Peretz', 'avi.peretz@email.com', '0571234567', '1975-09-05'),
(8, 'Michal', 'Levi', 'michal.levi@email.com', '0581234567', '1992-04-20'),
(9, 'Yossi', 'Biton', 'yossi.biton@email.com', '0591234567', '1980-01-30'),
(10, 'Noa', 'Shalom', 'noa.shalom@email.com', '0501234568', '1993-06-12');

-- Insert data into Customer table
INSERT INTO Customer (CustomerID, IDmember, Discount, StartYearMember)  -- שיניתי מ-ID ל-CustomerID
VALUES 
(1, 101, 10.00, 2020),
(2, 102, 15.00, 2019),
(3, NULL, 0.00, NULL),
(4, 104, 10.00, 2021),
(5, NULL, 0.00, NULL),
(6, 106, 20.00, 2018);

-- Insert data into Librarian table
INSERT INTO Librarian (LibrarianID, StartWorkDate, ExperienceYears, age, Salary)  -- שיניתי מ-ID ל-LibrarianID
VALUES 
(7, '2015-03-10', 8, 48, 12000.00),
(8, '2018-06-15', 5, 31, 10000.00),
(9, '2010-01-20', 13, 43, 15000.00),
(10, '2020-09-01', 3, 30, 9000.00);

-- Insert data into ShelfLocation table
INSERT INTO ShelfLocation (ShelfLocationID, Floor, RowNum, ShelfNumber)
VALUES 
(1, 1, 1, 1),
(2, 1, 1, 2),
(3, 1, 2, 1),
(4, 1, 2, 2),
(5, 2, 1, 1),
(6, 2, 1, 2),
(7, 2, 2, 1),
(8, 2, 2, 2);

-- Insert data into Author table
INSERT INTO Author (AuthorID, FirstName, LastName, Nationality)
VALUES 
(1, 'Amos', 'Oz', 'Israeli'),
(2, 'David', 'Grossman', 'Israeli'),
(3, 'Yuval Noah', 'Harari', 'Israeli'),
(4, 'J.K.', 'Rowling', 'British'),
(5, 'George R.R.', 'Martin', 'American'),
(6, 'Agatha', 'Christie', 'British');

-- Insert data into GenreTypes table
INSERT INTO GenreTypes (GenreID, GenreName, MinAge)
VALUES 
(1, 'Fiction', 12),
(2, 'Non-Fiction', 14),
(3, 'Fantasy', 10),
(4, 'Mystery', 12),
(5, 'Science Fiction', 13),
(6, 'Biography', 15);

-- Insert data into BookLanguage table
INSERT INTO BookLanguage (LanguageID, LanguageName, MainCountry)
VALUES 
(1, 'Hebrew', 'Israel'),
(2, 'English', 'United Kingdom'),
(3, 'Arabic', 'Egypt'),
(4, 'Russian', 'Russia'),
(5, 'French', 'France');

-- Insert data into BookList table
INSERT INTO BookList (BookID, TitleBookName, PublicationYear, price, amount, ShelfLocationID, AuthorID, GenreID)
VALUES 
(1, 'A Tale of Love and Darkness', 2002, 85.50, 10, 1, 1, 1),
(2, 'To the End of the Land', 2008, 95.00, 8, 2, 2, 1),
(3, 'Sapiens: A Brief History of Humankind', 2011, 120.00, 15, 3, 3, 2),
(4, 'Harry Potter and the Philosopher''s Stone', 1997, 75.00, 20, 4, 4, 3),
(5, 'A Game of Thrones', 1996, 110.00, 12, 5, 5, 3),
(6, 'Murder on the Orient Express', 1934, 65.00, 7, 6, 6, 4),
(7, 'Homo Deus: A Brief History of Tomorrow', 2015, 125.00, 10, 3, 3, 2),
(8, 'Harry Potter and the Chamber of Secrets', 1998, 75.00, 18, 4, 4, 3),
(9, 'And Then There Were None', 1939, 60.00, 5, 6, 6, 4),
(10, 'A Clash of Kings', 1998, 110.00, 10, 5, 5, 3);

-- Insert data into Language table (book-language relationships)
INSERT INTO Language (BookID, LanguageID)
VALUES 
(1, 1), -- Hebrew
(1, 2), -- English
(2, 1),
(2, 2),
(3, 1),
(3, 2),
(3, 5), -- French
(4, 2),
(5, 2),
(6, 2),
(6, 5),
(7, 1),
(7, 2),
(8, 2),
(9, 2),
(9, 5),
(10, 2);

-- Insert data into Order_Table
INSERT INTO Order_Table (OrderID, OrderDate, FinalPrice, CustomerID, LibrarianID)  -- שיניתי מ-CostumerID ל-CustomerID
VALUES 
(1, '2023-01-15', 160.50, 1, 7),
(2, '2023-02-20', 75.00, 2, 8),
(3, '2023-03-10', 195.00, 3, 9),
(4, '2023-04-05', 120.00, 4, 10),
(5, '2023-05-12', 85.50, 5, 7),
(6, '2023-06-18', 170.00, 6, 8),
(7, '2023-07-22', 135.00, 1, 9),
(8, '2023-08-30', 110.00, 2, 10);

-- Insert data into BookToOrder
INSERT INTO BookToOrder (OrderID, BookID, BookQuantity)
VALUES 
(1, 1, 1), -- Order 1: A Tale of Love and Darkness
(1, 3, 1), -- Order 1: Sapiens
(2, 4, 1), -- Order 2: Harry Potter 1
(3, 5, 1), -- Order 3: Game of Thrones
(3, 6, 1), -- Order 3: Murder on the Orient Express
(4, 3, 1), -- Order 4: Sapiens
(5, 1, 1), -- Order 5: A Tale of Love and Darkness
(6, 7, 1), -- Order 6: Homo Deus
(6, 8, 1), -- Order 6: Harry Potter 2
(7, 9, 1), -- Order 7: And Then There Were None
(7, 10, 1), -- Order 7: A Clash of Kings
(8, 5, 1); -- Order 8: Game of Thrones