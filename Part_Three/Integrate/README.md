## Database Migration Documentation

### Phase 1: Library System Integration (backup-import-preparation.sql)

### Purpose

Prepared the existing bookstore database to integrate with an external library system backup by making structural adjustments and creating compatibility layers.

### Key Changes

**Table Modifications:**

- `Librarian` → `Seller` (renamed to align with external system terminology)
- `GenreTypes` → `Genre` (renamed columns: GenreID→gid, GenreName→gname, added description)
- `Person` - added `pname` column for full name compatibility
- `Author` - added `birth_year` and `pid` columns for external system compatibility
- `Order_Table` - updated LibrarianID→SellerID references


**New Tables Added:**

- `Book` - library book catalog with age groups
- `Reader` - library patrons with borrowing limits
- `Borrow` - borrowing transactions
- `Fine` - late fees and penalties
- `CopyBook` - individual book copy details
- `WroteBy` - author-book relationships
- `BelongTo` - book-genre relationships
- `Reservation` - book reservations
- `Take` - reader-borrow relationships
- `Borrowed` - copy-borrow relationships


**ENUMs Created:**

- `age_group_enum` ('Adults', 'Teens', 'Children')
- `status_enum` ('Waiting', 'Completed')


### Result

Successfully merged bookstore and library systems into a single database with dual functionality, maintaining all original bookstore data while adding comprehensive library management capabilities.



## Phase 2: Schema Unification (complete-database-migration.sql)

### Purpose

Transformed the merged database into a clean, unified schema following proper database design principles with Person as a superclass for all human entities.

### Key Changes

**Core Structure:**

- `Person` - converted to superclass with SERIAL ID, expanded field sizes, added email uniqueness
- `Author` - transformed to Person specialization (removed name duplication)
- Created new specializations: `Librarian`, `Donor`
- Updated existing specializations: `Reader`, `Customer`, `Seller`


**Book System Unification:**

- Merged `BookList` + `Book` → unified `Book` table
- `BookLanguage` - new junction table for book-language relationships
- `Language` - restructured as master language table
- Separated inventory: `BookstoreInventory` (commercial) + `LibraryCopy` (library)


**Transaction System:**

- `Order_Table` → `Orders` with OrderType enum
- `BookToOrder` → `OrderItem` with improved structure
- Enhanced borrowing system with proper Reader/Librarian references
- Improved `Fine` tracking with audit trail


**Relationship Tables:**

- `BelongTo` → `GenreType` (cleaner naming)
- Updated `Reservation` to link readers to specific book-language combinations
- Removed redundant `Take` table


**New ENUMs:**

- `source_enum` ('Donated', 'Purchased')
- `order_type_enum` ('Individual', 'Library')
- `copy_condition_enum` ('Excellent', 'Good', 'Fair')
- `status_enum` → `reservation_status_enum`


### Result

Clean, normalized database supporting unified library-bookstore operations with proper inheritance, referential integrity, and scalable architecture for future enhancements.
