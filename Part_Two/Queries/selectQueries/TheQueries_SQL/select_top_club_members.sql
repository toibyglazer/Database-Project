/*
 * Query: Find top club members by order frequency
 * 
 * Description: This query returns a list of club members sorted by the number of
 * orders they've placed, from highest to lowest.
 * 
 * Intended for: Marketing team, customer relationship managers
 * 
 * Usage: Identifying the most active club members for special promotions and loyalty rewards.
 *
 *  שאילתה זו מחזירה רשימת חברי מועדון ממוינים לפי מספר ההזמנות
 * שביצעו, מהגבוה לנמוך.
 * 
 * מיועד עבור: צוות שיווק, מנהלי קשרי לקוחות
 * 
 * שימוש: זיהוי חברי המועדון הפעילים ביותר למבצעים מיוחדים ותגמולי נאמנות.
 */

SELECT 
    p.ID,
    p.FirstName || ' ' || p.LastName AS Customer_Name,
    p.Email,
   
    c.IDmember AS Member_Number,
    c.StartYearMember AS Start_Year_Member,
    COUNT(DISTINCT o.OrderID) AS Number_Of_Orders,
   
    MAX(o.OrderDate) AS Last_Order_Date
   
FROM Person p
JOIN Customer c ON p.ID = c.CustomerID
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE c.IDmember IS NOT NULL  -- רק חברי מועדון
GROUP BY p.ID, Customer_Name, p.Email, p.PhoneNumber, c.IDmember, c.StartYearMember
ORDER BY Number_Of_Orders DESC;