/*
Query: List books by shelf location

Description: This query returns a list of books organized by shelf location,
including floor, row, shelf number, and book details.

Intended for: Library staff, inventory managers

Usage: Helping staff locate books and manage physical inventory organization.


תיאור בעברית: שאילתה זו מחזירה רשימת ספרים מאורגנת לפי מיקום מדף,
כולל קומה, שורה, מספר מדף ופרטי הספר.

מיועד עבור: צוות הספרייה, מנהלי מלאי

שימוש: עזרה לצוות באיתור ספרים וניהול ארגון המלאי הפיזי.
*/

SELECT 
    sl.Floor,
    sl.RowNum AS Row,
    sl.ShelfNumber,
    b.BookID,
    b.TitleBookName AS BookTitle,
    a.FirstName || ' ' || a.LastName AS AuthorName,
    g.GenreName AS Genre,
    b.amount AS AvailableInventory
FROM ShelfLocation sl
JOIN BookList b ON sl.ShelfLocationID = b.ShelfLocationID
JOIN Author a ON b.AuthorID = a.AuthorID
JOIN GenreTypes g ON b.GenreID = g.GenreID
ORDER BY sl.Floor, sl.RowNum, sl.ShelfNumber, BookTitle;