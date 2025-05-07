/*
Query: Find the top 30 club members by order frequency in the past year

Description:
Returns a table with customer ID, name, club membership status, and number of orders
placed in the past year for the top 30 club members, sorted by order frequency.

Intended for:
- Marketing team
- Customer relationship managers

Usage:
Identifying the most active club members for special promotions and loyalty rewards.

שאילתה: מציאת 30 חברי המועדון המובילים לפי תדירות הזמנות בשנה האחרונה

תיאור:
מחזירה טבלה עם מזהה לקוח, שם, סטטוס חברות במועדון, ומספר הזמנות
שבוצעו בשנה האחרונה עבור 30 חברי המועדון המובילים, ממוינים לפי תדירות הזמנות.

מיועד עבור:
- צוות שיווק
- מנהלי קשרי לקוחות

שימוש:
זיהוי חברי המועדון הפעילים ביותר למבצעים מיוחדים ותגמולי נאמנות.
*/


SELECT 
    p.ID,
    p.FirstName || ' ' || p.LastName AS Customer_Name,
    'Yes' AS Club_Member,  -- All results are club members based on the filter
    COUNT(DISTINCT o.OrderID) AS Number_Of_Orders
FROM Person p
JOIN Customer c ON p.ID = c.CustomerID
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE 
    c.IDmember IS NOT NULL  -- Only club members
    AND o.OrderDate >= CURRENT_DATE - INTERVAL '5 year'  -- Only orders from the past year
GROUP BY p.ID, Customer_Name
ORDER BY Number_Of_Orders DESC
LIMIT 30;