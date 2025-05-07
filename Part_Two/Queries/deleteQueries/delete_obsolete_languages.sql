/*
 * File: delete_obsolete_languages.sql
 * 
 * Description: This script deletes obsolete or unpopular languages from the BookLanguage table.
 * This should be run AFTER delete_book_language_links.sql to ensure all references are removed first.
 * 
 * Intended for: Database administrators, system maintenance
 * 
 * Usage: Cleaning up unused languages to improve system performance and data quality.
 */

-- Display languages that will be deleted (for verification)
SELECT *
FROM BookLanguage
WHERE LanguageID IN (50, 51, 52, 53, 54)
ORDER BY LanguageID;

-- Delete obsolete languages
DELETE FROM BookLanguage
WHERE LanguageID IN (50, 51, 52, 53, 54);