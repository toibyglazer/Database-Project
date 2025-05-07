/*
 File: UpdateBookPrices.sql

 Description:
 This script updates book prices based on the total number of orders for each book, 
 regardless of order date.

 Logic:
 - If a book has 2 or more total orders, increase its price by 10%.
 - Otherwise, decrease its price by 2%.

 A final SELECT query displays the updated prices along with the total number of orders per book.
*/

-- Update book prices based on total order count (ignoring dates)
UPDATE BookList
SET price = 
    CASE
        -- Books with 2 or more orders: increase price by 10%
        WHEN (
            SELECT COUNT(*)
            FROM BookToOrder bo
            WHERE bo.BookID = BookList.BookID
        ) >= 2 THEN price * 1.10
        -- Other books: decrease price by 2%
        ELSE price * 0.98
    END;

-- Display updated book prices and total orders per book
SELECT 
    b.BookID,
    b.TitleBookName,
    b.price AS current_price,
    (
        SELECT COUNT(*)
        FROM BookToOrder bo
        WHERE bo.BookID = b.BookID
    ) AS total_orders
FROM BookList b
ORDER BY total_orders DESC;
