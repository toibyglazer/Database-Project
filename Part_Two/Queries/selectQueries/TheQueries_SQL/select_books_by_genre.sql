/*
Query: List books by genre sorted by popularity

Description:
Returns a list of books within a specified genre, sorted from most to least popular.

Intended for:
- Customers
- Customer service staff
- Inventory managers

Usage:
Helps users find trending books easily.


הצגת ספרים לפי ז'אנר, ממוינים לפי פופולריות

תיאור:
מחזירה רשימת ספרים בז'אנר מסוים, ממוינים מהפופולריים ביותר לפחות.

מיועדת עבור:
- לקוחות
- נציגי שירות
- מנהלי מלאי

שימוש:
מאפשר ללקוחות למצוא בקלות את הספרים המבוקשים ביותר בז'אנר המבוקש.
*/

SELECT 
    g.GenreName AS Genre,
    g.MinAge AS RecommendedMinimumAge,
    b.BookID,
    b.TitleBookName AS BookTitle,
    a.FirstName || ' ' || a.LastName AS AuthorName,
    b.price AS Price,
    b.amount AS AvailableInventory,
    STRING_AGG(DISTINCT bl.LanguageName, ', ') AS AvailableLanguages,
    COALESCE(SUM(bo.BookQuantity), 0) AS QuantityPurchased
FROM GenreTypes g
JOIN BookList b ON g.GenreID = b.GenreID
JOIN Author a ON b.AuthorID = a.AuthorID
LEFT JOIN Language l ON b.BookID = l.BookID
LEFT JOIN BookLanguage bl ON l.LanguageID = bl.LanguageID
LEFT JOIN BookToOrder bo ON b.BookID = bo.BookID
LEFT JOIN Order_Table o ON bo.OrderID = o.OrderID
WHERE g.GenreID = :genre_id  -- Replace with the desired genre ID
GROUP BY g.GenreName, g.MinAge, b.BookID, BookTitle, AuthorName, b.price, b.amount
ORDER BY QuantityPurchased DESC, BookTitle;