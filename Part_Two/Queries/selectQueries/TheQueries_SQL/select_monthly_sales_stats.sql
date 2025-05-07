/*
 * Query: Calculate average number of books ordered by month and year
 * 
 * Description: This query returns sales statistics by month and year, including
 * number of orders, number of books sold, total amount, and average books per order.
 * 
 * Intended for: Senior management, finance managers, marketing team
 * 
 * Usage: Analyzing seasonal sales trends and making business decisions.
 *
 *  שאילתה זו מחזירה סטטיסטיקות מכירות לפי חודש ושנה, כולל מספר הזמנות,
 * מספר ספרים שנמכרו, סכום כולל וממוצע ספרים להזמנה.
 * 
 * מיועד עבור: הנהלה בכירה, מנהלי כספים, צוות שיווק
 * 
 * שימוש: ניתוח מגמות מכירה עונתיות וקבלת החלטות עסקיות.
 */

SELECT 
    EXTRACT(YEAR FROM o.OrderDate) AS Year,
    EXTRACT(MONTH FROM o.OrderDate) AS Month,
    COUNT(DISTINCT o.OrderID) AS NumberOfOrders,
    SUM(bo.BookQuantity) AS NumberOfBooksSold,
    SUM(o.FinalPrice) AS TotalAmount,
    ROUND(AVG(bo.BookQuantity), 2) AS AverageBooksPerOrder
FROM Order_Table o
JOIN BookToOrder bo ON o.OrderID = bo.OrderID
WHERE o.OrderDate >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY Year, Month
ORDER BY Year DESC, Month DESC;