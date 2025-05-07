/*
Query: Analyze librarian performance based on order processing and sales

Description:  
This query evaluates librarian performance based on the number of orders  
processed, total sales amount, and percentage of total sales. It can be limited to  
a specific time period and number of results.

Intended for:  
- HR managers  
- Senior management

Usage:  
Employee performance evaluation, bonus determination, and identifying top performers.

שאילתה: ניתוח ביצועי הספרנים על פי עיבוד הזמנות ומכירות

תיאור:  
שאילתה זו מעריכה את ביצועי הספרנים על בסיס מספר ההזמנות שטופלו,  
סכום המכירות הכולל, ואחוז מסך המכירות. ניתן להגביל אותה לתקופת זמן מסוימת  
ולמספר תוצאות מוגדר.

מיועד עבור:  
- מנהלי משאבי אנוש  
- הנהלה בכירה

שימוש:  
הערכת ביצועי עובדים, קביעת בונוסים, וזיהוי עובדים מצטיינים.
*/



WITH TotalSales AS (
    SELECT SUM(FinalPrice) AS total_amount
    FROM Order_Table
    WHERE OrderDate >= CURRENT_DATE - INTERVAL '1 year'
)
SELECT 
    p.ID,
    p.FirstName || ' ' || p.LastName AS LibrarianName,
    l.ExperienceYears,
    COUNT(o.OrderID) AS NumberOfOrders,
    SUM(o.FinalPrice) AS TotalSalesAmount,
    ROUND((SUM(o.FinalPrice) / ts.total_amount) * 100, 2) AS SalesPercentage,
    ROUND(AVG(o.FinalPrice), 2) AS AverageOrderValue
FROM Person p
JOIN Librarian l ON p.ID = l.LibrarianID
JOIN Order_Table o ON l.LibrarianID = o.LibrarianID
CROSS JOIN TotalSales ts
WHERE o.OrderDate >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY p.ID, LibrarianName, l.ExperienceYears, ts.total_amount
ORDER BY NumberOfOrders DESC
LIMIT :limit_count;  -- Parameter to control number of results