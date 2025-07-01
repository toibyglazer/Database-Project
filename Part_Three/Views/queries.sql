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


------------------------------------------------------------------------------------

-- Queries on the second view - BorrowingAndFinesDetails
-- This view provides detailed borrowing and fines information from the perspective of the receiving department.

-- Query 1: Find readers with overdue borrowings and unpaid fines
SELECT 
    ReaderName,
    ReaderPhone,
    COUNT(CASE WHEN BorrowStatus = 'Overdue' THEN 1 END) AS OverdueBooks,
    COUNT(CASE WHEN FinePaid = FALSE THEN 1 END) AS UnpaidFines,
    SUM(CASE WHEN FinePaid = FALSE THEN fine_sum ELSE 0 END) AS TotalUnpaidAmount,
    MIN(borrow_date::date) AS FirstBorrowDate,
    MAX(return_date::date) AS LatestReturnDate,
    (CURRENT_DATE - MIN(borrow_date::date)) AS DaysSinceFirstBorrow
FROM BorrowingAndFinesDetails
WHERE BorrowStatus = 'Overdue' OR FinePaid = FALSE
GROUP BY ReaderName, ReaderPhone
HAVING COUNT(CASE WHEN BorrowStatus = 'Overdue' THEN 1 END) > 0 
    OR SUM(CASE WHEN FinePaid = FALSE THEN fine_sum ELSE 0 END) > 0
ORDER BY TotalUnpaidAmount DESC, OverdueBooks DESC;

-- Query 2: Analysis of Borrowing Patterns by Age Groups and Genres
SELECT 
    CASE 
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, r.birth_day)) < 18 THEN 'Children (under 18)'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, r.birth_day)) BETWEEN 18 AND 35 THEN 'Young Adults (18-35)'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, r.birth_day)) BETWEEN 36 AND 60 THEN 'Adults (36-60)'
        ELSE 'Seniors (60+)'
    END AS AgeGroup,
    COUNT(DISTINCT b.ReaderName) AS TotalReaders,  -- Count of unique readers in each age group
    COUNT(DISTINCT b.borrow_number) AS TotalBorrows,  -- Total number of borrows in each age group
    AVG(b.return_date - b.borrow_date) AS AvgBorrowDays,  -- Average borrow duration in days
    COUNT(CASE WHEN b.BorrowStatus = 'Overdue' THEN 1 END) AS OverdueCount  -- Number of overdue borrows
FROM BorrowingAndFinesDetails b
JOIN Reader r ON b.ReaderName = (SELECT pname FROM Person WHERE pid = r.pid)  -- Joining to get reader's birth date
WHERE b.borrow_date >= CURRENT_DATE - INTERVAL '12 months'  -- Filtering borrows from the last 6 months
GROUP BY 
    CASE 
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, r.birth_day)) < 18 THEN 'Children (under 18)'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, r.birth_day)) BETWEEN 18 AND 35 THEN 'Young Adults (18-35)'
        WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, r.birth_day)) BETWEEN 36 AND 60 THEN 'Adults (36-60)'
        ELSE 'Seniors (60+)'
    END
ORDER BY TotalBorrows DESC;  -- Order groups by total number of borrows descending
