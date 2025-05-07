/*
Query: Order history by customer

Description: This query returns the order history for a specific customer,
including order ID, date, final price, items ordered, and the librarian who processed it.

Intended for: Customer service staff, customers

Usage: Providing customers with their purchase history and helping staff resolve customer inquiries.

 שאילתה זו מחזירה את היסטוריית ההזמנות עבור לקוח מסוים,
כולל מזהה הזמנה, תאריך, מחיר סופי, פריטים שהוזמנו והספרן שטיפל בהזמנה.

מיועד עבור: צוות שירות לקוחות, לקוחות

שימוש: מתן היסטוריית רכישות ללקוחות ועזרה לצוות בפתרון שאלות לקוחות.
*/

SELECT 
    p.ID AS CustomerID,
    p.FirstName || ' ' || p.LastName AS CustomerName,
    o.OrderID,
    o.OrderDate,
    o.FinalPrice,
    STRING_AGG(b.TitleBookName || ' (' || bo.BookQuantity || ')', ', ') AS ItemsOrdered,
    pl.FirstName || ' ' || pl.LastName AS LibrarianName
FROM Person p
JOIN Customer c ON p.ID = c.CustomerID
JOIN Order_Table o ON c.CustomerID = o.CustomerID
JOIN BookToOrder bo ON o.OrderID = bo.OrderID
JOIN BookList b ON bo.BookID = b.BookID
LEFT JOIN Librarian l ON o.LibrarianID = l.LibrarianID
LEFT JOIN Person pl ON l.LibrarianID = pl.ID
WHERE p.ID = :customer_id  -- Replace with the desired customer ID
GROUP BY CustomerID, CustomerName, o.OrderID, o.OrderDate, o.FinalPrice, LibrarianName
ORDER BY o.OrderDate DESC;