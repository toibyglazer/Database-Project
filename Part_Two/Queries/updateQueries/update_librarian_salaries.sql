/*
 * Query: Update librarian salaries based on performance and experience
 * 
 * Description: This query updates librarian salaries based on their performance
 * (number of orders and average value) and experience. Librarians with higher
 * performance receive more significant raises.
 * 
 * Intended for: HR managers, senior management
 * 
 * Usage: Fair compensation adjustment, performance-based incentives, employee retention.
 */

UPDATE Librarian
SET Salary = 
    CASE
        WHEN performance_score >= 90 THEN Salary * 1.15  -- Outstanding performance: 15% raise
        WHEN performance_score >= 75 THEN Salary * 1.10  -- Excellent performance: 10% raise
        WHEN performance_score >= 60 THEN Salary * 1.07  -- Good performance: 7% raise
        WHEN performance_score >= 40 THEN Salary * 1.05  -- Average performance: 5% raise
        WHEN performance_score >= 20 THEN Salary * 1.03  -- Below average: 3% raise
        ELSE Salary * 1.02  -- Minimum raise: 2%
    END
FROM (
    SELECT 
        l.LibrarianID,
        (
            (COUNT(o.OrderID) * 0.4) + 
            (COALESCE(AVG(o.FinalPrice), 0) / 10 * 0.3) + 
            (l.ExperienceYears * 2 * 0.3)
        ) AS performance_score
    FROM Librarian l
    LEFT JOIN Order_Table o ON l.LibrarianID = o.LibrarianID
    WHERE o.OrderDate >= CURRENT_DATE - INTERVAL '1 year' OR o.OrderDate IS NULL
    GROUP BY l.LibrarianID, l.ExperienceYears
) AS librarian_performance
WHERE Librarian.LibrarianID = librarian_performance.LibrarianID;