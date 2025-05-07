/*
Query: List available languages for each book  

Description:  
This query returns a list of all books with the languages available  
for each book, total inventory, and price.  

Intended for:  
- Customers  
- Customer service staff  

Usage:  
Providing customers with information about book availability in different languages.  


שאילתה: הצגת השפות הזמינות לכל ספר

תיאור:  
מחזירה רשימה של כל הספרים עם השפות הזמינות לכל ספר,  
המלאי הכולל והמחיר.

מיועדת עבור:  
- לקוחות  
- צוות שירות לקוחות  

שימוש:  
הענקת מידע ללקוחות על זמינות ספרים בשפות שונות.
*/



SELECT 
    b.BookID,
    b.TitleBookName AS BookTitle,
    STRING_AGG(bl.LanguageName, ', ') AS AvailableLanguages,
    b.amount AS TotalInventory,
    b.price AS Price,
    a.FirstName || ' ' || a.LastName AS AuthorName
FROM BookList b
JOIN Author a ON b.AuthorID = a.AuthorID
LEFT JOIN Language l ON b.BookID = l.BookID
LEFT JOIN BookLanguage bl ON l.LanguageID = bl.LanguageID
GROUP BY b.BookID, BookTitle, TotalInventory, Price, AuthorName
ORDER BY BookTitle;