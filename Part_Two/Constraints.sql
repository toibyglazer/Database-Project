/*
 File: Constraints.sql

 Description:
 This script defines and adds various constraints to tables in the library database 
 in order to enforce data integrity and consistency.

 Constraints implemented:
 1. CHECK constraints on BookList (price and amount)
 2. DEFAULT constraint on Orders (OrderDate)
 3. NOT NULL constraints on Author (FirstName, LastName)
 4. UNIQUE constraint on Customer (IDmember)
 5. CHECK constraint on BookToOrder (BookQuantity)
 6. CHECK constraint on Customer (Discount range)
 7. CHECK constraints on ShelfLocation (Floor, RowNum, ShelfNumber)
*/


-- 1. CHECK constraints on BookList table
-- Ensures book price is positive and amount is non-negative
ALTER TABLE BookList
ADD CONSTRAINT chk_book_price_positive CHECK (price > 0),
ADD CONSTRAINT chk_book_amount_nonnegative CHECK (amount >= 0);

-- 2. DEFAULT constraint on Orders
-- Sets current date as default order date
ALTER TABLE Orders
ALTER COLUMN OrderDate SET DEFAULT CURRENT_DATE;

-- 3. NOT NULL constraints on Author table
-- Ensures author names cannot be empty
ALTER TABLE Author
ALTER COLUMN FirstName SET NOT NULL,
ALTER COLUMN LastName SET NOT NULL;

-- 4. UNIQUE constraint on Customer table
-- Ensures member IDs are unique
ALTER TABLE Customer
ADD CONSTRAINT unique_idmember UNIQUE (IDmember);

-- 5. CHECK constraint on BookToOrder table
-- A constraint that ensures that the quantity of books on order is positive
ALTER TABLE BookToOrder
ADD CONSTRAINT chk_book_quantity_positive CHECK (BookQuantity > 0);

-- 6. CHECK constraint on Customer table
-- A constraint that ensures that the discount percentage is within a reasonable range
ALTER TABLE Customer
ADD CONSTRAINT chk_discount_range CHECK (Discount BETWEEN 0 AND 70);

-- 7. CHECK constraint on ShelfLocation table
-- A constraint that ensures that the floor, row, and shelf numbers are positive
ALTER TABLE ShelfLocation
ADD CONSTRAINT chk_floor_positive CHECK (Floor > 0);

ALTER TABLE ShelfLocation
ADD CONSTRAINT chk_row_positive CHECK (RowNum > 0);

ALTER TABLE ShelfLocation
ADD CONSTRAINT chk_shelf_positive CHECK (ShelfNumber > 0);


