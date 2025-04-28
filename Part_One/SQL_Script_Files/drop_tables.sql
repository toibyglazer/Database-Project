-- Drop Tables Script
-- This script drops all tables in the correct order to avoid foreign key constraint violations

-- Drop junction tables first (tables with foreign keys to multiple tables)
DROP TABLE IF EXISTS BookToOrder;
DROP TABLE IF EXISTS Language;

-- Drop tables with foreign keys to other tables
DROP TABLE IF EXISTS Order_Table;
DROP TABLE IF EXISTS BookList;

-- Drop tables that are referenced by the tables above
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Librarian;
DROP TABLE IF EXISTS ShelfLocation;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS GenreTypes;
DROP TABLE IF EXISTS BookLanguage;

-- Drop base tables last
DROP TABLE IF EXISTS Person;