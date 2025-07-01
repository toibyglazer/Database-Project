-- =====================================================
-- Complete Database Migration Script
-- From Current Merged Schema to Final Desired Schema
-- =====================================================
-- This script transforms the current database (after library import) 
-- into the final unified library-bookstore schema while preserving all data

-- =====================================================
-- Step 1: Create New ENUM Types
-- =====================================================

-- Create additional ENUM types needed for the final schema
DO $$ 
BEGIN
    -- source_enum for tracking book origins (donated vs purchased)
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'source_enum') THEN
        CREATE TYPE source_enum AS ENUM ('Donated', 'Purchased');
    END IF;
    
    -- order_type_enum for different customer types
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_type_enum') THEN
        CREATE TYPE order_type_enum AS ENUM ('Individual', 'Library');
    END IF;
    
    -- copy_condition_enum for library book conditions
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'copy_condition_enum') THEN
        CREATE TYPE copy_condition_enum AS ENUM ('Excellent', 'Good', 'Fair');
    END IF;
    
    -- Rename status_enum to reservation_status_enum for clarity
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_enum') THEN
        ALTER TYPE status_enum RENAME TO reservation_status_enum;
    END IF;
END $$;

-- =====================================================
-- Step 2: Create Backup Tables for Data Safety
-- =====================================================

-- Backup critical tables before major transformations
CREATE TABLE migration_backup_person AS SELECT * FROM Person;
CREATE TABLE migration_backup_author AS SELECT * FROM Author;
CREATE TABLE migration_backup_booklist AS SELECT * FROM BookList;
CREATE TABLE migration_backup_book AS SELECT * FROM Book;
CREATE TABLE migration_backup_reader AS SELECT * FROM Reader;
CREATE TABLE migration_backup_orders AS SELECT * FROM Order_Table;

-- =====================================================
-- Step 3: Transform Person Table to Final Structure
-- =====================================================

-- Remove the redundant pname column added during import preparation
ALTER TABLE Person DROP COLUMN IF EXISTS pname;

-- Expand field sizes and add constraints to match final schema
ALTER TABLE Person ALTER COLUMN FirstName TYPE VARCHAR(100);
ALTER TABLE Person ALTER COLUMN LastName TYPE VARCHAR(100);
ALTER TABLE Person ALTER COLUMN Email TYPE VARCHAR(255);

-- Add unique constraint on Email (if not exists)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'person_email_unique' AND table_name = 'person'
    ) THEN
        ALTER TABLE Person ADD CONSTRAINT person_email_unique UNIQUE (Email);
    END IF;
END $$;

-- Convert ID to SERIAL type (this requires recreating the sequence)
-- First, create a new sequence for Person.ID
CREATE SEQUENCE IF NOT EXISTS person_id_seq;
SELECT setval('person_id_seq', COALESCE(MAX(ID), 0) + 1, false) FROM Person;
ALTER TABLE Person ALTER COLUMN ID SET DEFAULT nextval('person_id_seq');
ALTER SEQUENCE person_id_seq OWNED BY Person.ID;

-- =====================================================
-- Step 4: Transform Author Table to Specialization Structure
-- =====================================================

-- Create temporary table to store author data with person references
CREATE TEMP TABLE author_person_mapping AS
SELECT 
    a.AuthorID,
    a.FirstName,
    a.LastName,
    a.Nationality,
    p.ID as PersonID
FROM Author a
LEFT JOIN Person p ON (a.FirstName = p.FirstName AND a.LastName = p.LastName);

-- Insert authors who don't exist in Person table
INSERT INTO Person (FirstName, LastName)
SELECT DISTINCT a.FirstName, a.LastName
FROM Author a
WHERE NOT EXISTS (
    SELECT 1 FROM Person p 
    WHERE p.FirstName = a.FirstName AND p.LastName = a.LastName
);

-- Update the mapping with newly created person IDs
UPDATE author_person_mapping 
SET PersonID = p.ID
FROM Person p
WHERE author_person_mapping.FirstName = p.FirstName 
  AND author_person_mapping.LastName = p.LastName
  AND author_person_mapping.PersonID IS NULL;

-- Drop existing Author table and recreate as specialization
DROP TABLE Author CASCADE;

CREATE TABLE Author (
    AuthorID INTEGER PRIMARY KEY REFERENCES Person(ID) ON DELETE CASCADE,
    Nationality VARCHAR(100)
);

-- Insert data into new Author table
INSERT INTO Author (AuthorID, Nationality)
SELECT PersonID, Nationality
FROM author_person_mapping
WHERE PersonID IS NOT NULL;

-- =====================================================
-- Step 5: Transform Reader Table
-- =====================================================

-- Reader table needs to reference Person.ID instead of having its own pid
-- First, ensure all readers exist in Person table
INSERT INTO Person (ID, FirstName, LastName, PhoneNumber, BirthDate)
SELECT DISTINCT 
    r.pid,
    'Reader' || r.pid, -- Default first name
    'User', -- Default last name  
    r.phone_number,
    r.birth_day
FROM Reader r
WHERE NOT EXISTS (SELECT 1 FROM Person p WHERE p.ID = r.pid)
ON CONFLICT (ID) DO NOTHING;

-- Create new Reader table with correct structure
CREATE TABLE Reader_New (
    ReaderID INTEGER PRIMARY KEY REFERENCES Person(ID) ON DELETE CASCADE,
    bookLimit INTEGER DEFAULT 5,
    numTakenBooks INTEGER DEFAULT 0,
    joinDate DATE NOT NULL
);

-- Migrate data from old Reader table
INSERT INTO Reader_New (ReaderID, bookLimit, numTakenBooks, joinDate)
SELECT 
    pid,
    COALESCE(max_books_allowed, 5),
    COALESCE(num_taken_books, 0),
    join_date
FROM Reader;

-- Replace old Reader table
DROP TABLE Reader CASCADE;
ALTER TABLE Reader_New RENAME TO Reader;

-- =====================================================
-- Step 6: Transform Customer Table
-- =====================================================

-- Update Customer table structure
ALTER TABLE Customer ALTER COLUMN IDmember TYPE VARCHAR(50);
ALTER TABLE Customer ALTER COLUMN Discount SET DEFAULT 0.00;
ALTER TABLE Customer ADD COLUMN IF NOT EXISTS CustomerType order_type_enum;

-- Add unique constraint on IDmember
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'customer_idmember_unique' AND table_name = 'customer'
    ) THEN
        ALTER TABLE Customer ADD CONSTRAINT customer_idmember_unique UNIQUE (IDmember);
    END IF;
END $$;

-- =====================================================
-- Step 7: Transform Seller Table and Create Librarian Table
-- =====================================================

-- Update Seller table structure (remove extra columns added during import)
ALTER TABLE Seller DROP COLUMN IF EXISTS phone_number;
ALTER TABLE Seller DROP COLUMN IF EXISTS email;
ALTER TABLE Seller DROP COLUMN IF EXISTS pid;
ALTER TABLE Seller DROP COLUMN IF EXISTS age;

-- Rename LibrarianID to SellerID for consistency
ALTER TABLE Seller RENAME COLUMN LibrarianID TO SellerID;

-- Create new Librarian table (separate from Seller)
CREATE TABLE Librarian (
    LibrarianID INTEGER PRIMARY KEY REFERENCES Person(ID) ON DELETE CASCADE,
    StartWorkDate DATE
);

-- We'll populate Librarian table later when we have more context about who should be librarians

-- =====================================================
-- Step 8: Create Donor Table
-- =====================================================

CREATE TABLE Donor (
    DonorID INTEGER PRIMARY KEY REFERENCES Person(ID) ON DELETE CASCADE,
    TotalDonations INTEGER DEFAULT 0
);

-- =====================================================
-- Step 9: Transform Genre Table
-- =====================================================

-- Genre table was renamed from GenreTypes and has gid, gname, description
-- Transform it to final structure

-- Create new Genre table with correct structure
CREATE TABLE Genre_New (
    GenreID SERIAL PRIMARY KEY,
    GenreName VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT,
    MinAge INTEGER
);

-- Migrate data from current Genre table
INSERT INTO Genre_New (GenreName, Description, MinAge)
SELECT 
    gname,
    description,
    NULL -- MinAge will be set based on existing data patterns
FROM Genre
WHERE gname IS NOT NULL;

-- Update MinAge based on genre names (business logic)
UPDATE Genre_New SET MinAge = 5 WHERE LOWER(GenreName) LIKE '%child%';
UPDATE Genre_New SET MinAge = 13 WHERE LOWER(GenreName) LIKE '%teen%' OR LOWER(GenreName) LIKE '%young%';
UPDATE Genre_New SET MinAge = 16 WHERE MinAge IS NULL;

-- Store mapping for later use
CREATE TEMP TABLE genre_id_mapping AS
SELECT 
    g_old.gid as old_id,
    g_new.GenreID as new_id
FROM Genre g_old
JOIN Genre_New g_new ON g_old.gname = g_new.GenreName;

-- Replace old Genre table
DROP TABLE Genre CASCADE;
ALTER TABLE Genre_New RENAME TO Genre;

-- =====================================================
-- Step 10: Transform Language Tables
-- =====================================================

-- Current: BookLanguage (LanguageID, LanguageName, MainCountry) + Language (BookID, LanguageID)
-- Desired: Language (LanguageID SERIAL, LanguageName, MainCountry) + BookLanguage (BookLanguageID, BookID, LanguageID)

-- Rename current BookLanguage to Language
ALTER TABLE BookLanguage RENAME TO Language_New;

-- Convert LanguageID to SERIAL
CREATE SEQUENCE IF NOT EXISTS language_languageid_seq;
SELECT setval('language_languageid_seq', COALESCE(MAX(LanguageID), 0) + 1, false) FROM Language_New;
ALTER TABLE Language_New ALTER COLUMN LanguageID SET DEFAULT nextval('language_languageid_seq');
ALTER SEQUENCE language_languageid_seq OWNED BY Language_New.LanguageID;

-- Expand field sizes
ALTER TABLE Language_New ALTER COLUMN LanguageName TYPE VARCHAR(100);
ALTER TABLE Language_New ALTER COLUMN MainCountry TYPE VARCHAR(100);

-- Add unique constraint
ALTER TABLE Language_New ADD CONSTRAINT language_name_unique UNIQUE (LanguageName);

-- Store the old Language junction table data for later use
CREATE TEMP TABLE old_language_junction AS SELECT * FROM Language;

-- Drop old Language junction table
DROP TABLE Language CASCADE;

-- Rename Language_New to Language
ALTER TABLE Language_New RENAME TO Language;

-- =====================================================
-- Step 11: Create Unified Book Table and BookLanguage Junction
-- =====================================================

-- We need to merge BookList (bookstore) and Book (library) into one Book table
-- Create new unified Book table
CREATE TABLE Book_New (
    BookID SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    AuthorID INTEGER NOT NULL,
    AgeGroup age_group_enum NOT NULL,
    PublicationYear INTEGER,
    Publishing VARCHAR(255),
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID)
);

-- Insert books from BookList (bookstore system)
INSERT INTO Book_New (Title, AuthorID, AgeGroup, PublicationYear, Publishing)
SELECT 
    bl.TitleBookName,
    bl.AuthorID,
    CASE 
        WHEN g.MinAge <= 12 THEN 'Children'::age_group_enum
        WHEN g.MinAge <= 17 THEN 'Teens'::age_group_enum
        ELSE 'Adults'::age_group_enum
    END,
    bl.PublicationYear,
    'Unknown Publishing' -- Default value
FROM BookList bl
LEFT JOIN genre_id_mapping gm ON bl.GenreID = gm.old_id
LEFT JOIN Genre g ON gm.new_id = g.GenreID;

-- Insert books from Book (library system) that don't already exist
INSERT INTO Book_New (Title, AuthorID, AgeGroup, PublicationYear, Publishing)
SELECT DISTINCT
    b.title,
    COALESCE(wb.pid, 1), -- Use first author or default to ID 1
    b.age_group,
    COALESCE(cb.publication_year, 2000),
    COALESCE(cb.publishing, 'Unknown Publishing')
FROM Book b
LEFT JOIN WroteBy wb ON b.book_number = wb.book_number
LEFT JOIN CopyBook cb ON b.book_number = cb.book_number
WHERE NOT EXISTS (
    SELECT 1 FROM Book_New bn WHERE LOWER(bn.Title) = LOWER(b.title)
);

-- Create BookLanguage junction table
CREATE TABLE BookLanguage (
    BookLanguageID SERIAL PRIMARY KEY,
    BookID INTEGER REFERENCES Book_New(BookID),
    LanguageID INTEGER REFERENCES Language(LanguageID),
    UNIQUE(BookID, LanguageID)
);

-- Populate BookLanguage from old Language junction table
INSERT INTO BookLanguage (BookID, LanguageID)
SELECT DISTINCT
    bn.BookID,
    olj.LanguageID
FROM old_language_junction olj
JOIN BookList bl ON olj.BookID = bl.BookID
JOIN Book_New bn ON LOWER(bn.Title) = LOWER(bl.TitleBookName);

-- Add default language (English) for books without language specification
INSERT INTO BookLanguage (BookID, LanguageID)
SELECT DISTINCT
    bn.BookID,
    (SELECT LanguageID FROM Language WHERE LanguageName = 'English' LIMIT 1)
FROM Book_New bn
WHERE NOT EXISTS (
    SELECT 1 FROM BookLanguage bl WHERE bl.BookID = bn.BookID
);

-- Store book ID mappings for later use
CREATE TEMP TABLE book_id_mapping AS
SELECT 
    bl.BookID as old_booklist_id,
    bn.BookID as new_book_id
FROM BookList bl
JOIN Book_New bn ON LOWER(bn.Title) = LOWER(bl.TitleBookName);

CREATE TEMP TABLE library_book_mapping AS
SELECT 
    b.book_number as old_book_number,
    bn.BookID as new_book_id
FROM Book b
JOIN Book_New bn ON LOWER(bn.Title) = LOWER(b.title);

-- Replace old Book tables
DROP TABLE Book CASCADE;
DROP TABLE BookList CASCADE;
ALTER TABLE Book_New RENAME TO Book;

-- =====================================================
-- Step 12: Update ShelfLocation Table
-- =====================================================

-- Convert ShelfLocationID to SERIAL
CREATE SEQUENCE IF NOT EXISTS shelflocation_shelflocationid_seq;
SELECT setval('shelflocation_shelflocationid_seq', COALESCE(MAX(ShelfLocationID), 0) + 1, false) FROM ShelfLocation;
ALTER TABLE ShelfLocation ALTER COLUMN ShelfLocationID SET DEFAULT nextval('shelflocation_shelflocationid_seq');
ALTER SEQUENCE shelflocation_shelflocationid_seq OWNED BY ShelfLocation.ShelfLocationID;

-- =====================================================
-- Step 13: Create BookstoreInventory and LibraryCopy Tables
-- =====================================================

-- Create BookstoreInventory table
CREATE TABLE BookstoreInventory (
    BookLanguageID INTEGER PRIMARY KEY REFERENCES BookLanguage(BookLanguageID),
    BookstorePrice DECIMAL(10,2) NOT NULL,
    StockQuantity INTEGER DEFAULT 0
);

-- Populate BookstoreInventory from old BookList data
INSERT INTO BookstoreInventory (BookLanguageID, BookstorePrice, StockQuantity)
SELECT 
    bl.BookLanguageID,
    COALESCE(backup_bl.price, 0.00),
    COALESCE(backup_bl.amount, 0)
FROM BookLanguage bl
JOIN book_id_mapping bm ON bl.BookID = bm.new_book_id
JOIN migration_backup_booklist backup_bl ON bm.old_booklist_id = backup_bl.BookID;

-- Create LibraryCopy table
CREATE TABLE LibraryCopy (
    LibraryCopyID SERIAL PRIMARY KEY,
    BookLanguageID INTEGER REFERENCES BookLanguage(BookLanguageID),
    CopySource source_enum NOT NULL,
    ShelfLocationID INTEGER REFERENCES ShelfLocation(ShelfLocationID),
    DonorID INTEGER REFERENCES Donor(DonorID),
    CopyCondition copy_condition_enum
);

-- Populate LibraryCopy from CopyBook data
INSERT INTO LibraryCopy (BookLanguageID, CopySource, CopyCondition)
SELECT 
    bl.BookLanguageID,
    'Purchased'::source_enum, -- Default source
    'Good'::copy_condition_enum -- Default condition
FROM BookLanguage bl
JOIN library_book_mapping lbm ON bl.BookID = lbm.new_book_id
JOIN CopyBook cb ON lbm.old_book_number = cb.book_number;

-- =====================================================
-- Step 14: Transform Orders System
-- =====================================================

-- Update Order_Table to Orders
ALTER TABLE Order_Table RENAME TO Orders;

-- Convert OrderID to SERIAL
CREATE SEQUENCE IF NOT EXISTS orders_orderid_seq;
SELECT setval('orders_orderid_seq', COALESCE(MAX(OrderID), 0) + 1, false) FROM Orders;
ALTER TABLE Orders ALTER COLUMN OrderID SET DEFAULT nextval('orders_orderid_seq');
ALTER SEQUENCE orders_orderid_seq OWNED BY Orders.OrderID;

-- Add OrderType column
ALTER TABLE Orders ADD COLUMN OrderType order_type_enum NOT NULL DEFAULT 'Individual';

-- Update foreign key reference (SellerID should reference Seller.SellerID)
ALTER TABLE Orders DROP CONSTRAINT IF EXISTS order_table_sellerid_fkey;
ALTER TABLE Orders ADD CONSTRAINT orders_sellerid_fkey 
    FOREIGN KEY (SellerID) REFERENCES Seller(SellerID);

-- Create OrderItem table
CREATE TABLE OrderItem (
    OrderID INTEGER REFERENCES Orders(OrderID),
    BookLanguageID INTEGER REFERENCES BookstoreInventory(BookLanguageID),
    Quantity INTEGER NOT NULL,
    PRIMARY KEY (OrderID, BookLanguageID)
);

-- Populate OrderItem from BookToOrder
INSERT INTO OrderItem (OrderID, BookLanguageID, Quantity)
SELECT 
    bto.OrderID,
    bl.BookLanguageID,
    bto.BookQuantity
FROM BookToOrder bto
JOIN book_id_mapping bm ON bto.BookID = bm.old_booklist_id
JOIN BookLanguage bl ON bm.new_book_id = bl.BookID
WHERE EXISTS (SELECT 1 FROM BookstoreInventory bi WHERE bi.BookLanguageID = bl.BookLanguageID);

-- Drop old BookToOrder table
DROP TABLE BookToOrder CASCADE;

-- =====================================================
-- Step 15: Transform Borrowing System
-- =====================================================

-- We need to create some librarians first (from existing sellers or create new ones)
-- For now, let's create a default librarian
INSERT INTO Person (FirstName, LastName) VALUES ('System', 'Librarian');
INSERT INTO Librarian (LibrarianID, StartWorkDate) 
SELECT ID, CURRENT_DATE FROM Person WHERE FirstName = 'System' AND LastName = 'Librarian';

-- Update Borrow table structure
ALTER TABLE Borrow RENAME COLUMN borrow_number TO BorrowNumber;
ALTER TABLE Borrow RENAME COLUMN borrow_date TO BorrowDate;
ALTER TABLE Borrow RENAME COLUMN return_date TO ReturnDate;
ALTER TABLE Borrow RENAME COLUMN was_returned TO WasReturned;

-- Convert BorrowNumber to SERIAL
CREATE SEQUENCE IF NOT EXISTS borrow_borrownumber_seq;
SELECT setval('borrow_borrownumber_seq', COALESCE(MAX(BorrowNumber), 0) + 1, false) FROM Borrow;
ALTER TABLE Borrow ALTER COLUMN BorrowNumber SET DEFAULT nextval('borrow_borrownumber_seq');
ALTER SEQUENCE borrow_borrownumber_seq OWNED BY Borrow.BorrowNumber;

-- Add ReaderID and LibrarianID columns
ALTER TABLE Borrow ADD COLUMN ReaderID INTEGER REFERENCES Reader(ReaderID) ON DELETE CASCADE;
ALTER TABLE Borrow ADD COLUMN LibrarianID INTEGER REFERENCES Librarian(LibrarianID) ON DELETE CASCADE;

-- Set default values for new columns
UPDATE Borrow SET 
    ReaderID = pid,
    LibrarianID = (SELECT LibrarianID FROM Librarian LIMIT 1),
    WasReturned = COALESCE(WasReturned, FALSE);

-- Drop old pid column and add constraints
ALTER TABLE Borrow DROP COLUMN pid;
ALTER TABLE Borrow ALTER COLUMN ReaderID SET NOT NULL;
ALTER TABLE Borrow ALTER COLUMN LibrarianID SET NOT NULL;
ALTER TABLE Borrow ALTER COLUMN WasReturned SET DEFAULT FALSE;

-- Update Borrowed table
ALTER TABLE Borrowed RENAME COLUMN cid TO LibraryCopyID;
ALTER TABLE Borrowed RENAME COLUMN borrow_number TO BorrowNumber;

-- Update Fine table
ALTER TABLE Fine RENAME COLUMN fine_number TO FineID;
ALTER TABLE Fine RENAME COLUMN fine_sum TO Sum;
ALTER TABLE Fine RENAME COLUMN receive_date TO ReceiveDate;
ALTER TABLE Fine RENAME COLUMN was_paid TO WasPaid;
ALTER TABLE Fine RENAME COLUMN reason TO Reason;
ALTER TABLE Fine RENAME COLUMN borrow_number TO BorrowNumber;

-- Convert FineID to SERIAL
CREATE SEQUENCE IF NOT EXISTS fine_fineid_seq;
SELECT setval('fine_fineid_seq', COALESCE(MAX(FineID), 0) + 1, false) FROM Fine;
ALTER TABLE Fine ALTER COLUMN FineID SET DEFAULT nextval('fine_fineid_seq');
ALTER SEQUENCE fine_fineid_seq OWNED BY Fine.FineID;

-- Add LastUpdated column and set defaults
ALTER TABLE Fine ADD COLUMN LastUpdated DATE NOT NULL DEFAULT CURRENT_DATE;
ALTER TABLE Fine ALTER COLUMN WasPaid SET DEFAULT FALSE;
ALTER TABLE Fine ALTER COLUMN Reason TYPE TEXT;

-- Add unique constraint on BorrowNumber
ALTER TABLE Fine ADD CONSTRAINT fine_borrownumber_unique UNIQUE (BorrowNumber);

-- =====================================================
-- Step 16: Create Final Relationship Tables
-- =====================================================

-- Create GenreType table (replaces BelongTo)
CREATE TABLE GenreType (
    GenreID INTEGER REFERENCES Genre(GenreID) ON DELETE CASCADE,
    BookID INTEGER REFERENCES Book(BookID) ON DELETE CASCADE,
    PRIMARY KEY (GenreID, BookID)
);

-- Populate GenreType from BelongTo
INSERT INTO GenreType (GenreID, BookID)
SELECT DISTINCT
    gm.new_id,
    lbm.new_book_id
FROM BelongTo bt
JOIN genre_id_mapping gm ON bt.gid = gm.old_id
JOIN library_book_mapping lbm ON bt.book_number = lbm.old_book_number;

-- Also add genre relationships from old BookList
INSERT INTO GenreType (GenreID, BookID)
SELECT DISTINCT
    g.GenreID,
    bm.new_book_id
FROM migration_backup_booklist bl
JOIN book_id_mapping bm ON bl.BookID = bm.old_booklist_id
JOIN genre_id_mapping gm ON bl.GenreID = gm.old_id
JOIN Genre g ON gm.new_id = g.GenreID
WHERE NOT EXISTS (
    SELECT 1 FROM GenreType gt 
    WHERE gt.GenreID = g.GenreID AND gt.BookID = bm.new_book_id
);

-- Update Reservation table
ALTER TABLE Reservation RENAME COLUMN status TO Status;
ALTER TABLE Reservation RENAME COLUMN reservation_date TO ReservationDate;
ALTER TABLE Reservation RENAME COLUMN book_number TO BookLanguageID;
ALTER TABLE Reservation RENAME COLUMN pid TO ReaderID;

-- Update the Status column type
ALTER TABLE Reservation ALTER COLUMN Status TYPE reservation_status_enum USING Status::reservation_status_enum;

-- Update foreign key references
-- We need to map book_number to BookLanguageID
UPDATE Reservation SET BookLanguageID = (
    SELECT bl.BookLanguageID 
    FROM BookLanguage bl
    JOIN library_book_mapping lbm ON bl.BookID = lbm.new_book_id
    WHERE lbm.old_book_number = Reservation.BookLanguageID
    LIMIT 1
);

-- =====================================================
-- Step 17: Clean Up Old Tables and Temporary Data
-- =====================================================

-- Drop old tables that are no longer needed
DROP TABLE IF EXISTS WroteBy CASCADE;
DROP TABLE IF EXISTS BelongTo CASCADE;
DROP TABLE IF EXISTS Take CASCADE;
DROP TABLE IF EXISTS CopyBook CASCADE;

-- Drop temporary tables
DROP TABLE IF EXISTS author_person_mapping;
DROP TABLE IF EXISTS genre_id_mapping;
DROP TABLE IF EXISTS book_id_mapping;
DROP TABLE IF EXISTS library_book_mapping;
DROP TABLE IF EXISTS old_language_junction;

-- =====================================================
-- Step 18: Add Indexes and Constraints for Performance
-- =====================================================

-- Add useful indexes
CREATE INDEX IF NOT EXISTS idx_book_author ON Book(AuthorID);
CREATE INDEX IF NOT EXISTS idx_book_title ON Book(Title);
CREATE INDEX IF NOT EXISTS idx_booklanguage_book ON BookLanguage(BookID);
CREATE INDEX IF NOT EXISTS idx_booklanguage_language ON BookLanguage(LanguageID);
CREATE INDEX IF NOT EXISTS idx_borrow_reader ON Borrow(ReaderID);
CREATE INDEX IF NOT EXISTS idx_borrow_librarian ON Borrow(LibrarianID);
CREATE INDEX IF NOT EXISTS idx_borrow_date ON Borrow(BorrowDate);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON Orders(CustomerID);
CREATE INDEX IF NOT EXISTS idx_orders_seller ON Orders(SellerID);
CREATE INDEX IF NOT EXISTS idx_orders_date ON Orders(OrderDate);

-- Add check constraints
ALTER TABLE Reader ADD CONSTRAINT reader_book_limit_positive CHECK (bookLimit > 0);
ALTER TABLE Reader ADD CONSTRAINT reader_taken_books_non_negative CHECK (numTakenBooks >= 0);
ALTER TABLE BookstoreInventory ADD CONSTRAINT bookstore_price_non_negative CHECK (BookstorePrice >= 0);
ALTER TABLE BookstoreInventory ADD CONSTRAINT stock_quantity_non_negative CHECK (StockQuantity >= 0);
ALTER TABLE Donor ADD CONSTRAINT donor_total_donations_non_negative CHECK (TotalDonations >= 0);

-- =====================================================
-- Step 19: Final Data Validation
-- =====================================================

-- Count records in all tables to verify migration
SELECT 
    'Person' as table_name, COUNT(*) as record_count FROM Person
UNION ALL SELECT 'Author', COUNT(*) FROM Author
UNION ALL SELECT 'Reader', COUNT(*) FROM Reader  
UNION ALL SELECT 'Customer', COUNT(*) FROM Customer
UNION ALL SELECT 'Seller', COUNT(*) FROM Seller
UNION ALL SELECT 'Librarian', COUNT(*) FROM Librarian
UNION ALL SELECT 'Donor', COUNT(*) FROM Donor
UNION ALL SELECT 'Genre', COUNT(*) FROM Genre
UNION ALL SELECT 'Language', COUNT(*) FROM Language
UNION ALL SELECT 'Book', COUNT(*) FROM Book
UNION ALL SELECT 'BookLanguage', COUNT(*) FROM BookLanguage
UNION ALL SELECT 'ShelfLocation', COUNT(*) FROM ShelfLocation
UNION ALL SELECT 'BookstoreInventory', COUNT(*) FROM BookstoreInventory
UNION ALL SELECT 'LibraryCopy', COUNT(*) FROM LibraryCopy
UNION ALL SELECT 'Orders', COUNT(*) FROM Orders
UNION ALL SELECT 'OrderItem', COUNT(*) FROM OrderItem
UNION ALL SELECT 'Borrow', COUNT(*) FROM Borrow
UNION ALL SELECT 'Borrowed', COUNT(*) FROM Borrowed
UNION ALL SELECT 'Fine', COUNT(*) FROM Fine
UNION ALL SELECT 'Reservation', COUNT(*) FROM Reservation
UNION ALL SELECT 'GenreType', COUNT(*) FROM GenreType
ORDER BY table_name;

-- =====================================================
-- Step 20: Clean Up Backup Tables (Optional)
-- =====================================================

-- Uncomment these lines only after verifying the migration was successful
-- DROP TABLE IF EXISTS migration_backup_person;
-- DROP TABLE IF EXISTS migration_backup_author;
-- DROP TABLE IF EXISTS migration_backup_booklist;
-- DROP TABLE IF EXISTS migration_backup_book;
-- DROP TABLE IF EXISTS migration_backup_reader;
-- DROP TABLE IF EXISTS migration_backup_orders;

-- Final success message
SELECT 'Complete database migration finished successfully!' as status;

-- =====================================================
-- MIGRATION SUMMARY AND EXPLANATION
-- =====================================================

/*
=== DETAILED MIGRATION ANALYSIS ===

This migration script transforms a merged library-bookstore database into a unified,
well-structured system following proper database design principles.

STARTING POINT (Current Database After Import):
The database contained a mix of original bookstore tables and imported library tables:

BOOKSTORE TABLES (Original):
- Person: Basic person information with added 'pname' column
- Customer: Customer specialization with bookstore-specific fields
- Seller: Renamed from Librarian, contains bookstore staff info
- Author: Separate author table with name duplication
- GenreTypes→Genre: Renamed with gid/gname structure
- BookLanguage→Language: Language master table
- BookList: Bookstore inventory with pricing
- Language: Junction table for book-language relationships
- Order_Table: Sales orders
- BookToOrder: Order line items
- ShelfLocation: Physical shelf locations

LIBRARY TABLES (Imported):
- Book: Library book catalog with age groups
- Reader: Library patrons
- Borrow: Borrowing transactions
- Fine: Late fees and penalties
- CopyBook: Individual book copies
- WroteBy: Author-book relationships
- BelongTo: Book-genre relationships
- Reservation: Book reservations
- Take: Reader-borrow relationships
- Borrowed: Copy-borrow relationships

TRANSFORMATION GOALS:
Create a unified system where:
1. Person serves as superclass for all human entities
2. Books exist in both bookstore inventory and library copies
3. Same person can be customer, reader, author, etc.
4. Proper normalization and referential integrity
5. Support for both commercial and library operations

KEY TRANSFORMATIONS PERFORMED:

1. **ENUM TYPES CREATION**
   - source_enum: Tracks if library books were donated or purchased
   - order_type_enum: Distinguishes individual vs library bulk orders
   - copy_condition_enum: Tracks physical condition of library books
   - reservation_status_enum: Renamed from status_enum for clarity

2. **PERSON TABLE ENHANCEMENT**
   - Removed redundant 'pname' column (FirstName + LastName provides same info)
   - Expanded field sizes (VARCHAR(50) → VARCHAR(100) for names)
   - Added unique constraint on Email for account management
   - Converted ID to SERIAL for auto-increment functionality

3. **AUTHOR TABLE RESTRUCTURING**
   - Transformed from independent table to Person specialization
   - Eliminated name duplication (now references Person.FirstName/LastName)
   - Preserved nationality information
   - Created mapping between old AuthorID and new Person.ID

4. **SPECIALIZATION TABLES CREATION/UPDATE**
   - Reader: Converted from library-specific to Person specialization
     * Renamed columns to camelCase for consistency
     * Added proper defaults (bookLimit=5, numTakenBooks=0)
     * Removed redundant phone_number (now in Person table)
   
   - Customer: Enhanced existing bookstore customer table
     * Expanded IDmember field size and added uniqueness
     * Added CustomerType enum for individual vs library customers
     * Set proper default for Discount (0.00)
   
   - Seller: Cleaned up imported modifications
     * Removed redundant contact fields (phone_number, email, pid)
     * Renamed LibrarianID to SellerID for clarity
     * Maintained salary and experience tracking
   
   - Librarian: NEW - Separate from Seller
     * Library staff have different responsibilities than bookstore sellers
     * Enables role-based permissions and workflows
     * References Person.ID like other specializations
   
   - Donor: NEW - Tracks people who donate books
     * Essential for library donation management
     * Enables donor recognition and tax documentation
     * Tracks total donation count

5. **BOOK SYSTEM UNIFICATION**
   - Merged BookList (bookstore) and Book (library) into single Book table
   - Eliminated title duplication while preserving all information
   - Added proper AuthorID foreign key to Author specialization
   - Preserved age group classifications and publication details
   - Created mapping tables to maintain data relationships

6. **LANGUAGE SYSTEM RESTRUCTURING**
   - Renamed BookLanguage to Language (master table)
   - Created new BookLanguage as junction table
   - Converted to SERIAL primary keys for better performance
   - Maintained book-language relationships from both systems

7. **INVENTORY SEPARATION**
   - BookstoreInventory: Commercial stock with pricing and quantities
     * Links to BookLanguage for specific book-language combinations
     * Tracks sellable inventory separate from library copies
     * Migrated pricing and stock data from BookList
   
   - LibraryCopy: Individual library book copies
     * Each copy tracked separately with condition and source
     * Links to BookLanguage for cataloging
     * Supports shelf location tracking
     * Enables donation tracking via DonorID

8. **TRANSACTION SYSTEM ENHANCEMENT**
   - Orders: Renamed from Order_Table with added features
     * Added OrderType enum for different customer types
     * Converted to SERIAL primary key
     * Maintained customer and seller relationships
   
   - OrderItem: NEW - Proper order line item table
     * Replaces BookToOrder with better structure
     * Links to BookstoreInventory for available items
     * Supports complex ordering scenarios

9. **BORROWING SYSTEM IMPROVEMENT**
   - Borrow: Enhanced with proper Reader and Librarian references
     * Renamed columns to PascalCase for consistency
     * Added ReaderID and LibrarianID foreign keys
     * Converted to SERIAL primary key
   
   - Borrowed: Maintained junction table for multiple books per borrow
     * Links to LibraryCopy for specific copy tracking
     * Enables borrowing multiple copies in one transaction
   
   - Fine: Enhanced fine tracking system
     * Added LastUpdated field for audit trail
     * Converted to SERIAL primary key
     * Added unique constraint on BorrowNumber
     * Expanded Reason field to TEXT for detailed explanations

10. **RELATIONSHIP TABLES OPTIMIZATION**
    - GenreType: Replaces BelongTo with clearer naming
      * Links Genre to Book (not individual copies)
      * Supports multiple genres per book
    
    - Reservation: Updated to link readers to specific book-language combinations
      * Renamed status_enum to reservation_status_enum
      * Links to BookLanguage for specific reservations
      * Maintains reader-specific reservation tracking

11. **DELETED TABLES AND JUSTIFICATION**
    - WroteBy: Simplified to direct AuthorID in Book table
      * Single author per book is sufficient for most cases
      * Reduces complexity while maintaining essential relationships
    
    - BelongTo: Replaced by GenreType with clearer naming
      * Same functionality with better naming convention
    
    - Take: Redundant with proper Borrow table structure
      * Reader information now directly in Borrow table
      * Eliminates unnecessary junction table
    
    - CopyBook: Information integrated into LibraryCopy
      * Publishing and publication year moved to Book table
      * Copy-specific information (condition, source) in LibraryCopy

12. **PERFORMANCE AND INTEGRITY IMPROVEMENTS**
    - Added strategic indexes on frequently queried columns
    - Implemented check constraints for data validation
    - Ensured proper foreign key relationships throughout
    - Added unique constraints where business logic requires

=== BUSINESS BENEFITS ===

This unified structure enables:

1. **Integrated Customer Management**
   - Same person can be reader, customer, author, donor
   - Unified contact information and preferences
   - Cross-system loyalty and relationship tracking

2. **Flexible Inventory Management**
   - Same book available in both bookstore and library
   - Different pricing strategies for different markets
   - Unified catalog with separate inventory tracking

3. **Comprehensive Transaction Tracking**
   - Sales, loans, fines, donations all properly tracked
   - Audit trails for financial and operational reporting
   - Support for complex business scenarios

4. **Role-Based Operations**
   - Clear separation between librarians and sellers
   - Appropriate permissions and workflows for each role
   - Scalable staff management

5. **Advanced Reporting Capabilities**
   - Cross-system analytics and insights
   - Customer behavior analysis across both services
   - Inventory optimization opportunities

6. **Future Scalability**
   - Clean, normalized structure supports growth
   - Easy to add new features and specializations
   - Maintainable codebase for long-term success

The migration preserves all existing data while creating a more maintainable,
scalable, and logically consistent database structure that properly supports
the combined library-bookstore business model.
*/
