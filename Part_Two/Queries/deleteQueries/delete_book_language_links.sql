/*
 * File: delete_book_language_links.sql
 * 
 * Description: This script deletes links between books and obsolete or unpopular languages
 * from the Language table.
 * 
 * Intended for: Database administrators, system maintenance
 * 
 * Usage: Cleaning up unused language links to improve system performance and data quality.
 */

-- Display records that will be deleted (for verification)
SELECT l.*, b.TitleBookName
FROM Language l
JOIN BookList b ON l.BookID = b.BookID
WHERE l.LanguageID IN (50, 51, 52, 53, 54)
ORDER BY l.LanguageID, l.BookID;

-- Delete links between books and obsolete languages
DELETE FROM Language
WHERE LanguageID IN (50, 51, 52, 53, 54);