/*
Query: List books by genre with appropriate age group  

Description:  
This query returns a list of books for a specific genre with appropriate age group,  
including book details, author, price, and available inventory.  

Intended for:  
- Customers  
- Parents  
- Customer service staff  

Usage:  
Helping customers find age-appropriate books for children and young adults.  


הצגת ספרים לפי ז'אנר עם קבוצת גיל מתאימה

תיאור:  
השאילתה מחזירה רשימת ספרים בז'אנר מסוים עם קבוצת גיל מתאימה,  
כולל פרטי הספר, שם הסופר, מחיר וכמות במלאי.

מיועדת עבור:  
- לקוחות  
- הורים  
- נציגי שירות  

שימוש:  
מסייעת ללקוחות למצוא ספרים מתאימים לגיל עבור ילדים ובני נוער.
*/


SELECT 
    g.GenreName AS Genre,
    g.MinAge AS RecommendedMinimumAge,
    b.BookID,
    b.TitleBookName AS BookTitle,
    a.FirstName || ' ' || a.LastName AS AuthorName,
    b.price AS Price,
    b.amount AS AvailableInventory,
    STRING_AGG(DISTINCT bl.LanguageName, ', ') AS AvailableLanguages
FROM GenreTypes g
JOIN BookList b ON g.GenreID = b.GenreID
JOIN Author a ON b.AuthorID = a.AuthorID
LEFT JOIN Language l ON b.BookID = l.BookID
LEFT JOIN BookLanguage bl ON l.LanguageID = bl.LanguageID
WHERE g.GenreID = :genre_id  -- Replace with the desired genre ID
  AND g.MinAge <= :reader_age  -- Replace with the reader's age
GROUP BY Genre, RecommendedMinimumAge, b.BookID, BookTitle, AuthorName, Price, AvailableInventory
ORDER BY BookTitle;