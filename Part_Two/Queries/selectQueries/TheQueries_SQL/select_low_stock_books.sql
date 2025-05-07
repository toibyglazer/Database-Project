/*
Query: Find books that are low in stock with their shelf location and language

Description: This query returns a list of books with relatively low inventory
(less than 50% of the average), including shelf location, available languages,
and author name.

Intended for: Inventory managers, procurement staff

Usage: Helps manage inventory and alerts when books need to be reordered.


 שאילתה זו מחזירה רשימת ספרים שהמלאי שלהם נמוך יחסית 
(פחות מ-50% מהממוצע), כולל מיקום המדף, שפות זמינות ושם המחבר.

מיועד עבור: מנהלי מלאי, צוות רכש

שימוש: מסייעת בניהול המלאי ומתריעה על ספרים שיש להזמין מחדש.
*/

SELECT 
    b.BookID,
    b.TitleBookName AS BookTitle,
    b.amount AS StockQuantity,
    sl.Floor,
    sl.RowNum AS Row,
    sl.ShelfNumber,
    STRING_AGG(bl.LanguageName, ', ') AS AvailableLanguages,
    a.FirstName || ' ' || a.LastName AS AuthorName
FROM BookList b
JOIN ShelfLocation sl ON b.ShelfLocationID = sl.ShelfLocationID
JOIN Author a ON b.AuthorID = a.AuthorID
LEFT JOIN Language l ON b.BookID = l.BookID
LEFT JOIN BookLanguage bl ON l.LanguageID = bl.LanguageID
GROUP BY b.BookID, BookTitle, StockQuantity, Floor, Row, ShelfNumber, AuthorName
HAVING b.amount < (SELECT AVG(amount) * 0.5 FROM BookList)
ORDER BY StockQuantity ASC;