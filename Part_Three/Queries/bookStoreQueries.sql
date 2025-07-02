-- Queries on the first view - CustomerOrderDetails
-- This view contains detailed customer order data from the original department's perspective.

-- Query 1: Find the most active customers in the last year by total spending
SELECT 
    CustomerName,
    Email,
    COUNT(DISTINCT OrderID) AS TotalOrders,
    SUM(FinalPrice) AS TotalSpent,
    StartYearMember
FROM CustomerOrderDetails
WHERE OrderDate >= CURRENT_DATE - INTERVAL '1 year'  -- Filter orders from the last year
GROUP BY CustomerName, Email, StartYearMember           -- Group results by customer info to aggregate orders and spending
HAVING SUM(FinalPrice) > 500                            -- Include only customers with total spending above 500
ORDER BY TotalSpent DESC;                               -- Sort customers by total amount spent, descending

-- Query 2: Top 20 best-selling books in the last year
SELECT 
    TitleBookName,
    AuthorName,
    GenreName,
    SUM(BookQuantity) AS TotalSold,
    SUM(TotalBookPrice) AS TotalRevenue
FROM CustomerOrderDetails
WHERE OrderDate >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY TitleBookName, AuthorName, GenreName
ORDER BY TotalSold DESC
LIMIT 20;


