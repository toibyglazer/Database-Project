/*
Query: Find all books written by a specific author  

Description:  
This query returns all books written by a specific author,  
including book details, inventory, price, and available languages.  

Intended for:  
- Customers  
- Customer service staff  

Usage:  
Helping customers find all books by their favorite authors.  


שאילתה: מציאת כל הספרים שנכתבו על ידי מחבר מסוים

תיאור:  
מחזירה את כל הספרים שנכתבו על ידי מחבר מסוים,  
כולל פרטי הספר, מלאי, מחיר ושפות זמינות.

מיועדת עבור:  
- לקוחות  
- נציגי שירות  

שימוש:  
עוזרת ללקוחות למצוא את כל הספרים של המחברים האהובים עליהם.
*/


SELECT 
    b.BookID,
    b.TitleBookName AS BookTitle,
    b.PublicationYear,
    g.GenreName AS Genre,
    b.price AS Price,
    b.amount AS AvailableInventory,
    STRING_AGG(bl.LanguageName, ', ') AS AvailableLanguages,
    sl.Floor,
    sl.RowNum AS Row,
    sl.ShelfNumber
FROM BookList b
JOIN Author a ON b.AuthorID = a.AuthorID
JOIN GenreTypes g ON b.GenreID = g.GenreID
JOIN ShelfLocation sl ON b.ShelfLocationID = sl.ShelfLocationID
LEFT JOIN Language l ON b.BookID = l.BookID
LEFT JOIN BookLanguage bl ON l.LanguageID = bl.LanguageID
WHERE a.AuthorID = :author_id  -- Replace with the desired author ID
GROUP BY b.BookID, BookTitle, b.PublicationYear, Genre, Price, AvailableInventory, Floor, Row, ShelfNumber
ORDER BY b.PublicationYear DESC;