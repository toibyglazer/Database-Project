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
     b.BookID AS BookID,
     b.TitleBookName AS BookName,
	 STRING_AGG(DISTINCT bl.LanguageName, ', ') AS AvailableLanguages,
     g.MinAge AS MinimumAge,
	 b.amount AS StockQuantity
   
FROM GenreTypes g
JOIN BookList b ON g.GenreID = b.GenreID
JOIN Author a ON b.AuthorID = a.AuthorID
LEFT JOIN Language l ON b.BookID = l.BookID
LEFT JOIN BookLanguage bl ON l.LanguageID = bl.LanguageID
LEFT JOIN BookToOrder bo ON b.BookID = bo.BookID
WHERE g.GenreID = 43  -- Replace with the desired genre ID
GROUP BY b.BookID, b.TitleBookName, a.FirstName, a.LastName, g.MinAge, b.amount, b.price
ORDER BY COALESCE(SUM(bo.BookQuantity), 0) DESC, b.TitleBookName;