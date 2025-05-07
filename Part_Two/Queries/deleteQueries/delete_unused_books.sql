/*
 * Query: Delete books that have never been ordered and are from authors with no other books
 * 
 * Description: This query deletes books that have never been ordered and belong to
 * authors who have no other books in the system.
 * 
 * Intended for: Inventory managers, procurement staff
 * 
 * Usage: Removing unpopular items from inventory, freeing up space for new inventory.
 */

DELETE FROM BookList
WHERE BookID IN (
    SELECT b.BookID
    FROM BookList b
    LEFT JOIN BookToOrder bo ON b.BookID = bo.BookID
    WHERE bo.BookID IS NULL
    AND b.AuthorID IN (
        SELECT a.AuthorID
        FROM Author a
        JOIN BookList bl ON a.AuthorID = bl.AuthorID
        GROUP BY a.AuthorID
        HAVING COUNT(bl.BookID) = 1
    )
);