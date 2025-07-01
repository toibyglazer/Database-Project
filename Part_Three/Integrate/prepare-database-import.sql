-- ------------------------------------------------------------------
-- Backup Import Preparation Script
-- Run this script BEFORE importing the backup from the external company.
-- It prepares the current database to be compatible with the external backup.
-- ------------------------------------------------------------------

-- Step 1: Create required ENUM types if they don't already exist
-- These ENUMs are used in the external system's tables and must exist to allow import.
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'age_group_enum') THEN
        CREATE TYPE age_group_enum AS ENUM ('Adults', 'Teens', 'Children');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_enum') THEN
        CREATE TYPE status_enum AS ENUM ('Waiting', 'Completed');
    END IF;
END $$;

-- Step 2: Rename table "Librarian" to "Seller"
-- The external system uses the term "Seller" instead of "Librarian" for the staff entity.
-- We rename to avoid confusion and align with their schema.
ALTER TABLE Librarian RENAME TO Seller;

-- Step 3: Rename the column "LibrarianID" in "orders" table to "SellerID"
-- This aligns foreign key column names with the renamed "Seller" table.
ALTER TABLE orders RENAME COLUMN LibrarianID TO SellerID;

-- Step 4: Update foreign key constraints on orders table accordingly
ALTER TABLE orders DROP CONSTRAINT IF EXISTS order_table_librarianid_fkey;
ALTER TABLE orders ADD CONSTRAINT order_table_sellerid_fkey 
    FOREIGN KEY (SellerID) REFERENCES Seller(LibrarianID);

-- Step 5: Prepare "GenreTypes" table to match external "Genre" table structure
-- Rename columns to match external schema
ALTER TABLE GenreTypes RENAME COLUMN GenreID TO gid;
ALTER TABLE GenreTypes RENAME COLUMN GenreName TO gname;

-- Add "description" column which exists in external schema but not locally
ALTER TABLE GenreTypes ADD COLUMN IF NOT EXISTS description VARCHAR(255);

-- Rename table to "Genre" to match external table name
ALTER TABLE GenreTypes RENAME TO Genre;

-- Step 6: Backup important existing tables before making further changes
-- This allows rollback or data reference if needed
CREATE TABLE IF NOT EXISTS backup_person AS SELECT * FROM Person;
CREATE TABLE IF NOT EXISTS backup_author AS SELECT * FROM Author;
CREATE TABLE IF NOT EXISTS backup_genretypes AS SELECT * FROM Genre;
CREATE TABLE IF NOT EXISTS backup_seller AS SELECT * FROM Seller;

-- Step 7: Add missing columns to existing tables for compatibility with external schema

-- Person table: add "pname" for full name, which the external system uses
ALTER TABLE Person ADD COLUMN IF NOT EXISTS pname VARCHAR(100);

-- Fill "pname" by concatenating FirstName and LastName if empty
UPDATE Person SET pname = CONCAT(FirstName, ' ', LastName) WHERE pname IS NULL;

-- Author table: add "birth_year" and "pid" columns to match external schema
ALTER TABLE Author ADD COLUMN IF NOT EXISTS birth_year INTEGER;
ALTER TABLE Author ADD COLUMN IF NOT EXISTS pid INTEGER;

-- Add a check constraint on "birth_year" to ensure valid years
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'author_birth_year_check'
    ) THEN
        ALTER TABLE Author ADD CONSTRAINT author_birth_year_check 
        CHECK (birth_year BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE));
    END IF;
END $$;

-- Genre table: add missing columns if needed (for backup safety)
ALTER TABLE Genre ADD COLUMN IF NOT EXISTS gname VARCHAR(100);
ALTER TABLE Genre ADD COLUMN IF NOT EXISTS description VARCHAR(255);
ALTER TABLE Genre ADD COLUMN IF NOT EXISTS gid INTEGER;

-- Fill gname with gname values from existing GenreName if needed
UPDATE Genre SET gname = gname WHERE gname IS NULL;

-- Seller table (previously Librarian): add missing contact columns and pid key
ALTER TABLE Seller ADD COLUMN IF NOT EXISTS phone_number VARCHAR(12);
ALTER TABLE Seller ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE Seller ADD COLUMN IF NOT EXISTS pid INTEGER;

-- Step 8: Create new tables from the external schema that don't exist locally

-- Book table (different from local BookList)
CREATE TABLE IF NOT EXISTS Book (
    book_number INT NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    num_copies INT NOT NULL CHECK (num_copies >= 0),
    age_group age_group_enum NOT NULL
);

-- Genre table (already renamed in step 5, but ensuring it exists)
CREATE TABLE IF NOT EXISTS Genre (
    gid INT NOT NULL PRIMARY KEY,
    gname VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255)
);

-- Reader table (new)
CREATE TABLE IF NOT EXISTS Reader (
    pid INT NOT NULL PRIMARY KEY,
    phone_number VARCHAR(12) NOT NULL CHECK (LENGTH(phone_number) BETWEEN 9 AND 12),
    birth_day DATE NOT NULL,
    join_date DATE NOT NULL,
    num_taken_books INT NOT NULL CHECK (num_taken_books >= 0),
    max_books_allowed INT,
    FOREIGN KEY (pid) REFERENCES Person(ID)
);

-- Borrow table (new)
CREATE TABLE IF NOT EXISTS Borrow (
    borrow_number INT NOT NULL PRIMARY KEY,
    pid INT NOT NULL,
    borrow_date DATE NOT NULL CHECK (borrow_date <= CURRENT_DATE),
    return_date DATE NOT NULL CHECK (return_date >= borrow_date),
    was_returned BOOLEAN NOT NULL,
    FOREIGN KEY (pid) REFERENCES Seller(LibrarianID)
);

-- Fine table (new)
CREATE TABLE IF NOT EXISTS Fine (
    fine_number INT NOT NULL PRIMARY KEY,
    reason VARCHAR(255) NOT NULL,
    fine_sum DECIMAL(10,2) NOT NULL CHECK (fine_sum > 0),
    receive_date DATE NOT NULL,
    was_paid BOOLEAN NOT NULL,
    borrow_number INT NOT NULL,
    FOREIGN KEY (borrow_number) REFERENCES Borrow(borrow_number)
);

-- CopyBook table (new)
CREATE TABLE IF NOT EXISTS CopyBook (
    cid INT NOT NULL PRIMARY KEY,
    book_number INT NOT NULL,
    publishing VARCHAR(255) NOT NULL,
    publication_year INTEGER NOT NULL CHECK (publication_year BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)),
    FOREIGN KEY (book_number) REFERENCES Book(book_number)
);

-- Relationship tables (new)

-- WroteBy: links Authors to Books
CREATE TABLE IF NOT EXISTS WroteBy (
    pid INT NOT NULL,
    book_number INT NOT NULL,
    PRIMARY KEY (pid, book_number),
    FOREIGN KEY (pid) REFERENCES Author(AuthorID),
    FOREIGN KEY (book_number) REFERENCES Book(book_number)
);

-- BelongTo: links Books to Genres
CREATE TABLE IF NOT EXISTS BelongTo (
    book_number INT NOT NULL,
    gid INT NOT NULL,
    PRIMARY KEY (book_number, gid),
    FOREIGN KEY (book_number) REFERENCES Book(book_number),
    FOREIGN KEY (gid) REFERENCES Genre(gid)
);

-- Reservation table (new)
CREATE TABLE IF NOT EXISTS Reservation (
    status status_enum NOT NULL,
    reservation_date DATE NOT NULL,
    book_number INT NOT NULL,
    pid INT NOT NULL,
    PRIMARY KEY (book_number, pid),
    FOREIGN KEY (book_number) REFERENCES Book(book_number),
    FOREIGN KEY (pid) REFERENCES Reader(pid)
);

-- Take table (new)
CREATE TABLE IF NOT EXISTS Take (
    pid INT NOT NULL,
    borrow_number INT NOT NULL,
    PRIMARY KEY (pid, borrow_number),
    FOREIGN KEY (pid) REFERENCES Reader(pid),
    FOREIGN KEY (borrow_number) REFERENCES Borrow(borrow_number)
);

-- Borrowed table (new)
CREATE TABLE IF NOT EXISTS Borrowed (
    cid INT NOT NULL,
    borrow_number INT NOT NULL,
    PRIMARY KEY (cid, borrow_number),
    FOREIGN KEY (cid) REFERENCES CopyBook(cid),
    FOREIGN KEY (borrow_number) REFERENCES Borrow(borrow_number)
);


-- ------------------------------------------------------------------
-- Post-import Data Restoration Script
-- Run this script AFTER successful backup import.
-- It restores missing data and validates integrity.
-- ------------------------------------------------------------------

-- Restore missing pid values in Author table
UPDATE Author 
SET pid = AuthorID 
WHERE pid IS NULL;

-- Restore missing gid values in Genre table (was GenreTypes)
UPDATE Genre 
SET gid = gid -- redundant; originally SET gid = GenreID
WHERE gid IS NULL;

-- Restore missing pid values in Seller table (was Librarian)
UPDATE Seller 
SET pid = LibrarianID 
WHERE pid IS NULL;


-- Data validation: count records in key tables to verify import success
SELECT 
    'Person' as table_name, 
    COUNT(*) as record_count 
FROM Person
UNION ALL
SELECT 
    'Author' as table_name, 
    COUNT(*) as record_count 
FROM Author
UNION ALL
SELECT 
    'Book' as table_name, 
    COUNT(*) as record_count 
FROM Book
UNION ALL
SELECT 
    'Genre' as table_name, 
    COUNT(*) as record_count 
FROM Genre
UNION ALL
SELECT 
    'Reader' as table_name, 
    COUNT(*) as record_count 
FROM Reader
UNION ALL
SELECT 
    'Borrow' as table_name, 
    COUNT(*) as record_count 
FROM Borrow;

-- Completion message for restoration
SELECT 'Post-import data restoration completed!' as status;


-- ------------------------------------------------------------------
-- Backup Tables Cleanup Script
-- Run this script ONLY AFTER verifying the system works correctly.
-- It removes backup tables to clean the database.
-- ------------------------------------------------------------------

DROP TABLE IF EXISTS backup_person;
DROP TABLE IF EXISTS backup_author;
DROP TABLE IF EXISTS backup_genretypes;
DROP TABLE IF EXISTS backup_seller;

-- Completion message for cleanup
SELECT 'Backup tables cleanup completed!' as status;


-- ------------------------------------------------------------------
-- CURRENT DATABASE SCHEMA SUMMARY
-- Summary of tables created/modified with main columns and keys.
-- ------------------------------------------------------------------

/*
Person
  - ID (INT, PRIMARY KEY)
  - FirstName (VARCHAR)
  - LastName (VARCHAR)
  - Email (VARCHAR)
  - PhoneNumber (VARCHAR)
  - BirthDate (DATE)
  - pname (VARCHAR) -- Full name (FirstName + LastName)

Seller (formerly Librarian)
  - LibrarianID (INT, PRIMARY KEY)
  - StartWorkDate (DATE)
  - ExperienceYears (INT)
  - Age (INT)
  - Salary (NUMERIC)
  - phone_number (VARCHAR)
  - email (VARCHAR)
  - pid (INT)

Genre (formerly GenreTypes)
  - gid (INT, PRIMARY KEY)
  - gname (VARCHAR, UNIQUE)
  - description (VARCHAR)

Author
  - AuthorID (INT, PRIMARY KEY)
  - FirstName (VARCHAR)
  - LastName (VARCHAR)
  - Nationality (VARCHAR)
  - birth_year (INT)
  - pid (INT)

Book
  - book_number (INT, PRIMARY KEY)
  - title (VARCHAR)
  - num_copies (INT)
  - age_group (ENUM: Adults, Teens, Children)

Reader
  - pid (INT, PRIMARY KEY, FK to Person.ID)
  - phone_number (VARCHAR)
  - birth_day (DATE)
  - join_date (DATE)
  - num_taken_books (INT)
  - max_books_allowed (INT)

Borrow
  - borrow_number (INT, PRIMARY KEY)
  - pid (INT, FK to Seller.LibrarianID)
  - borrow_date (DATE)
  - return_date (DATE)
  - was_returned (BOOLEAN)

Fine
  - fine_number (INT, PRIMARY KEY)
  - reason (VARCHAR)
  - fine_sum (DECIMAL)
  - receive_date (DATE)
  - was_paid (BOOLEAN)
  - borrow_number (INT, FK to Borrow.borrow_number)

CopyBook
  - cid (INT, PRIMARY KEY)
  - book_number (INT, FK to Book.book_number)
  - publishing (VARCHAR)
  - publication_year (INT)

WroteBy (relationship)
  - pid (INT, FK to Author.AuthorID)
  - book_number (INT, FK to Book.book_number)
  - PRIMARY KEY (pid, book_number)

BelongTo (relationship)
  - book_number (INT, FK to Book.book_number)
  - gid (INT, FK to Genre.gid)
  - PRIMARY KEY (book_number, gid)

Reservation
  - status (ENUM: Waiting, Completed)
  - reservation_date (DATE)
  - book_number (INT, FK to Book.book_number)
  - pid (INT, FK to Reader.pid)
  - PRIMARY KEY (book_number, pid)

Take
  - pid (INT, FK to Reader.pid)
  - borrow_number (INT, FK to Borrow.borrow_number)
  - PRIMARY KEY (pid, borrow_number)

Borrowed
  - cid (INT, FK to CopyBook.cid)
  - borrow_number (INT, FK to Borrow.borrow_number)
  - PRIMARY KEY (cid, borrow_number)
*/

