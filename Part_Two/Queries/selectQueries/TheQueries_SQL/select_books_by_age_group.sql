/*
 * Query: Find the most popular books by age group (top 3 for each age group)
 * 
 * Description: This query returns the top 3 most popular books for each age group
 * (under 18, 18-30, 31-50, over 50), including book title, author name, genre, and quantity purchased.
 * 
 * Intended for: Marketing team, procurement staff
 * 
 * Usage: Tailoring inventory and promotions to different age groups' preferences,
 * improving targeted marketing strategies.
 * 
 * 
 * שאילתה: מציאת הספרים הפופולריים ביותר לפי קבוצת גיל (3 המובילים בכל קבוצה)
 * 
 * תיאור: שאילתה זו מחזירה את 3 הספרים הפופולריים ביותר בכל קבוצת גיל
 * (מתחת לגיל 18, 18-30, 31-50, מעל 50), כולל שם הספר, שם המחבר, ז'אנר וכמות שנרכשה.
 * 
 * מיועדת עבור: צוות שיווק, אנשי רכש
 * 
 * שימוש: התאמת מלאי ומבצעים להעדפות של קבוצות גיל שונות,
 * שיפור אסטרטגיות שיווק ממוקדות.
 */

WITH AgeGroups AS (
    SELECT 
        CASE 
            WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.BirthDate) < 18 THEN 'Under 18'
            WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.BirthDate) BETWEEN 18 AND 30 THEN '18-30'
            WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.BirthDate) BETWEEN 31 AND 50 THEN '31-50'
            ELSE 'Over 50'
        END AS AgeGroup,
        bo.BookID,
        SUM(bo.BookQuantity) AS QuantityPurchased
    FROM Person p
    JOIN Customer c ON p.ID = c.CustomerID
    JOIN Order_Table o ON c.CustomerID = o.CustomerID
    JOIN BookToOrder bo ON o.OrderID = bo.OrderID
    WHERE p.BirthDate IS NOT NULL
    GROUP BY AgeGroup, bo.BookID
),
RankedBooks AS (
    SELECT 
        ag.AgeGroup,
        b.BookID,
        b.TitleBookName AS BookTitle,
        a.FirstName || ' ' || a.LastName AS AuthorName,
        g.GenreName AS Genre,
        ag.QuantityPurchased,
        ROW_NUMBER() OVER (PARTITION BY ag.AgeGroup ORDER BY ag.QuantityPurchased DESC) AS Rank
    FROM AgeGroups ag
    JOIN BookList b ON ag.BookID = b.BookID
    JOIN Author a ON b.AuthorID = a.AuthorID
    JOIN GenreTypes g ON b.GenreID = g.GenreID
)
SELECT AgeGroup, BookTitle, AuthorName, Genre, QuantityPurchased
FROM RankedBooks
WHERE Rank <= 3
ORDER BY AgeGroup, Rank;