/*
 File: UpdateBookAmounts.sql

 Description:
 This script performs two separate transactions:
 1. Randomly sets the 'amount' of each book in the BookList table to a value between 1 and 100.
 2. Randomly sets the amount to 0 for approximately 5% of the books.

 Notes:
 - Each transaction is wrapped with BEGIN and COMMIT to ensure atomicity.
 - Due to the use of RANDOM(), results will vary on each execution.
*/

-- Transaction 1: Set a random amount (1-100) for every book
BEGIN;

UPDATE BookList
SET amount = FLOOR(RANDOM() * 100) + 1; -- RANDOM() generates a float between 0 and 1

-- Show updated book amounts
SELECT BookID, TitleBookName, amount
FROM BookList;

COMMIT;

-- Transaction 2: Randomly select ~5% of books and set their amount to 0
BEGIN;

UPDATE BookList
SET amount = 0
WHERE BookID IN (
    SELECT BookID
    FROM BookList
    ORDER BY RANDOM() -- Shuffle the list randomly
    LIMIT (SELECT CEIL(COUNT(*) * 0.05) FROM BookList) -- Choose ~5% of total books
);

-- Show books whose amount was set to 0
SELECT BookID, TitleBookName, amount
FROM BookList
WHERE amount = 0;

COMMIT;

-- Final check: Display all books and their current amount
SELECT BookID, TitleBookName, amount
FROM BookList;
