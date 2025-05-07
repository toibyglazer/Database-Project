/*
 * Query: Find the 20 most popular books by order quantity in the past year
 * 
 * Description: This query returns the top 20 best-selling books in the past year,
 * sorted from most to least popular. For each book, it displays book details,
 * author name, genre, quantity purchased, and number of orders.
 * 
 * Intended for: Library managers, procurement staff, marketing team
 * 
 * Usage: Helps identify which books are selling best to restock inventory,
 * make marketing decisions, and understand customer preferences.
 *
 *  שאילתה זו מחזירה את 20 הספרים הנמכרים ביותר בשנה האחרונה,
 * ממוינים מהפופולרי ביותר לפחות פופולרי. עבור כל ספר מוצגים פרטי הספר,
 * שם המחבר, הז'אנר, כמות שנרכשה ומספר ההזמנות.
 * 
 * מיועד עבור: מנהלי הספרייה, אחראי רכש, צוות שיווק
 * 
 * שימוש: מאפשרת לזהות אילו ספרים נמכרים הכי טוב כדי להזמין מלאי נוסף,
 * לקבל החלטות שיווקיות, ולהבין העדפות לקוחות.
 */

SELECT 
    b.BookID,
    b.TitleBookName AS BookTitle,
    a.FirstName || ' ' || a.LastName AS AuthorName,
    g.GenreName AS Genre,
    SUM(bo.BookQuantity) AS QuantityPurchased,
    COUNT(DISTINCT o.OrderID) AS NumberOfOrders
FROM BookList b
JOIN Author a ON b.AuthorID = a.AuthorID
JOIN GenreTypes g ON b.GenreID = g.GenreID
JOIN BookToOrder bo ON b.BookID = bo.BookID
JOIN Order_Table o ON bo.OrderID = o.OrderID
WHERE o.OrderDate >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY b.BookID, b.TitleBookName, AuthorName, g.GenreName
ORDER BY QuantityPurchased DESC
LIMIT 20;