/*
 * Query: Update customer discounts based on purchase history and membership duration
 * 
 * Description: This query updates customer discount percentages based on their purchase history
 * and membership duration. Customers who spend more money or have been members longer
 * receive higher discounts.
 * 
 * Intended for: Customer relationship managers, marketing team
 * 
 * Usage: Rewarding loyal customers, encouraging repeat purchases, improving customer satisfaction.
 */

UPDATE Customer
SET Discount = 
    CASE
        WHEN total_spent >= 5000 THEN 20.00  -- VIP customers
        WHEN total_spent >= 2000 OR membership_years >= 5 THEN 15.00  -- Loyal customers
        WHEN total_spent >= 1000 OR membership_years >= 3 THEN 10.00  -- Regular customers
        WHEN total_spent >= 500 THEN 5.00  -- New regular customers
        ELSE 0.00  -- Basic customers
    END
FROM (
    SELECT 
        c.CustomerID,
        COALESCE(SUM(o.FinalPrice), 0) AS total_spent,
        EXTRACT(YEAR FROM CURRENT_DATE) - c.StartYearMember AS membership_years
    FROM Customer c
    LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
    WHERE o.OrderDate >= CURRENT_DATE - INTERVAL '5 years' OR o.OrderDate IS NULL
    GROUP BY c.CustomerID, c.StartYearMember
) AS customer_stats
WHERE Customer.CustomerID = customer_stats.CustomerID;