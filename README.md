# **Book Store**
Bookstore Management System - A Comprehensive Solution for Cataloging, Sales, and Customer Management  
Database Project By Toiby Glazer 326484524 | Semester B, Spring 2025 
## Table of Contents
- [Part One: Design and Build the Database](#part-one-design-and-build-the-database)
  - [Introduction](#introduction)
  - [ERD (Entity-Relationship Diagram)](#erd-entity-relationship-diagram)
  - [DSD (Data Structure Diagram)](#dsd-data-structure-diagram)
  - [SQL Scripts](#sql-scripts)
  - [Data](#data)
  - [Screenshots of the Dataset](#screenshots-of-the-dataset)
  - [Backup](#backup)
- [Part Two: Queries and Constraints](#part-two-queries-and-constraints)  
  - [Queries](#queries)  
    - [Select Queries](#select-queries) 
    - [Delete Queries](#delete-queries)  
    - [Update Queries](#update-queries)  
  - [Constraints](#constraints)  
  - [Rollback and Commit](#rollback-and-commit)  
  - [Backup Part-Two](#backup-part-two) 
- [Part Three: Integration and Views](#part-three-integration-and-views)
  - [Library Department ERD & DSD](#library-department-erd--dsd)
  - [Post-Integration ERD & DSD](#post-integration-erd--dsd)
  - [Integration Process and Decisions](#integration-process-and-decisions)
  - [Views](#views)
  - [Queries](#queries)
  - [Backup Part-Three](#backup-part-three)
- [Part Four: Functions, Procedures, Triggers & Main Program Execution](#part-four-functions-procedures-triggers--main-program-execution)
  - [Functions](#functions)
  - [Procedures](#procedures)
  - [Triggers](#triggers)
  - [Main Programs](#main-programs)
    - [Main Program 1: Book Borrowing](#main-program-1-book-borrowing)
    - [Main Program 2: Ordering from the Bookstore](#main-program-2-ordering-from-the-bookstore)
  - [Demonstration Screenshots](#demonstration-screenshots)  
  - [PL/pgSQL Exceptions](#plpgsql-exceptions)
  - [Backup Part-Four](#backup-part-four)
- [Part Five: Graphical User Interface](#part-five-graphical-user-interface)
  - [Technology Stack](#technology-stack)
  - [Application Architecture](#application-architecture)
  - [Main Menu Layout](#main-menu-layout)
  - [CRUD Management Screens](#crud-management-screens)
  - [Information Function Screens](#information-function-screens)
  - [Statistics Screens](#statistics-screens)
  - [Query Screens](#query-screens)
  - [Procedure Screens](#procedure-screens)
  - [Main Program Screens](#main-program-screens)
  - [How to Run the Application](#how-to-run-the-application)
  - [Screenshots](#screenshots)


## Part One: Design and Build the Database
### Introduction
The **Bookstore Management System Database** is designed to efficiently manage information related to books, customers, librarians, authors, and sales transactions. This comprehensive system ensures smooth organization and tracking of essential details such as inventory management, customer memberships, book categorization, and sales history.

#### Purpose of the Database

This database serves as a structured and reliable solution for bookstores to:

- Organize and track book inventory including titles, authors, genres, languages, and shelf locations
- Manage customer information, including membership status and discount eligibility
- Record and process book orders and sales transactions
- Track librarian/staff information including experience, salary, and responsibilities
- Maintain detailed book metadata such as publication years, prices, and available languages
- Monitor book availability and stock levels across different categories and languages

 #### **Potential Use Cases**  
  - **Bookstore Managers and Administrators**
    - Track inventory levels and identify bestselling or understocked items
    - Monitor sales performance and revenue generation
    - Manage staff assignments and evaluate employee performance
    - Generate reports on sales trends, customer preferences, and inventory status
    - Make informed decisions about book ordering and promotional strategies

  - **Librarians and Sales Staff**
    - Process customer orders efficiently with access to complete book information
    - Quickly locate books on shelves using the shelf location system
    - Identify membership status and applicable discounts for customers
    - Access author and genre information to assist customers with recommendations
    - Track order history for customer service inquiries

  - **Customers**
    - Browse available books by genre, author, or language
    - Check book availability and pricing information
    - Track order history and purchase records
    - Utilize membership benefits and discounts
    - Receive personalized book recommendations based on purchase history

  - **Publishers and Authors**
    - Track book performance and sales metrics
    - Identify popular genres and language preferences
    - Analyze market trends to inform future publishing decisions


 #### Database Structure

The database is organized into several logical sections, each consisting of related tables:

#### Database Structure

- **Person Management**
  - Person: Core personal information (name, contact details, birth date)
  - Customer: Membership details and discount eligibility
  - Librarian: Staff information including experience, salary, and work history

- **Book Metadata**
  - Author: Information about book authors
  - GenreTypes: Categories of books with age recommendations
  - BookLanguage: Languages available for books

- **Inventory Management**
  - BookList: Comprehensive book information including title, price, and stock levels
  - ShelfLocation: Physical location tracking for efficient retrieval
  - Language: Tracks which books are available in which languages

- **Sales and Orders**
  - Order_Table: Transaction records including dates, prices, and involved parties
  - BookToOrder: Detailed order contents linking books to specific orders  

This structured database helps streamline bookstore operations, improving inventory management, customer service, and business intelligence capabilities. The system provides a comprehensive solution for modern bookstores seeking to optimize their operations and enhance the customer experience.
### ERD (Entity-Relationship Diagram)
![ERD Diagram](Part_One/ERD_DSD_Files/ERD_diagram.png)
### DSD (Data Structure Diagram)
![DSD Diagram](Part_One/ERD_DSD_Files/DSD_diagram.png)
### SQL Scripts

- [Create Tables Script](Part_One/SQL_Script_Files/create_tables.sql)  Creates the database tables.
- [Insert Data Script](Part_One/SQL_Script_Files/insert_tables.sql)  Inserts initial data into the tables.
- [Drop Tables Script](Part_One/SQL_Script_Files/drop_tables.sql)  Deletes the tables from the database.
- [Select All Tables Script](Part_One/SQL_Script_Files/selectAll_tables.sql)  Retrieves all data from the tables.
### Data

#### **First tool** using [Mockaroo](https://mockaroo.com/) to create CSV files.

  - Inserting data into the **Author** (Scope: 1 - 400) table [View Author.csv](Part_One/Mockaroo/Author.csv)

  - Inserting data into the **Person** (Scope 1 - 800) table [View Person.csv](Part_One/Mockaroo/Person.csv) 
#### **Second tool** using [generatedata.com](https://generatedata.com/) to create CSV files.

  - Inserting data into the **ShelfLocation** (Scope 1 - 400) table [View Author.csv](Part_One/GenerateData/ShelfLocation.csv) 
#### **Third tool** using Python to create CSV files.
I developed a Python script that automatically generates CSV files with predefined values and constraints. The script streamlines the process by creating structured data based on specific criteria, making it easier to manage and analyze large datasets.
  - Inserting data into the **GenreTypes** (Scope 1 - 50) table [View GenreTypes.csv](Part_One/PythonScripts/GenreTypes/GenreTypes.csv) 
    **Code view**  [View GenreTypes.py](Part_One/PythonScripts/GenreTypes/CreateGenreTypes.py)

  - Inserting data into the **BookLanguage** (Scope 1 - 60) table [View BookLanguage.csv](Part_One/PythonScripts/BookLanguage/BookLanguage.csv) 
    **Code view**  [View BookLanguage.py](Part_One/PythonScripts/BookLanguage/CreateBookLanguage.py)

  - Inserting data into the **Customer** (Scope 1 - 400) table [View Customer.csv](Part_One/PythonScripts/Customer/Customer.csv) **Code view**  [View Customer.py](Part_One/PythonScripts/Customer/CreateCustomer.py)

  - Inserting data into the **Librarian** (Scope 1 - 400) table [View Librarian.csv](Part_One/PythonScripts/Librarian/Librarian.csv) **Code view**  [View Librarian.py](Part_One/PythonScripts/Librarian/CreateLibrarian.py)

  - Inserting data into the **BookList** (Scope 1 - 400) table [View BookList.csv](Part_One/PythonScripts/BookList/BookList.csv)  **Code view**  [View BookList.py](Part_One/PythonScripts/BookList/CreateBookList.py)

  - Inserting data into the **Language** (Scope 1 - 800) table [View Language.csv](Part_One/PythonScripts/Language/Language.csv)  **Code view**  [View Language.py](Part_One/PythonScripts/Language/CreateLanguage.py)

  - Inserting data into the **Orders** (Scope 1 - 800) table [View Orders.csv](Part_One/PythonScripts/Orders/Orders.csv)   **Code view**  [View Orders.py](Part_One/PythonScripts/Orders/CreateOrders.py)

  - Inserting data into the **BookToOrder** (Scope 1 - 900) table [View BookToOrder.csv](Part_One/PythonScripts/BookToOrder/BookToOrder.csv)   **Code view**  [View BookToOrder.py](Part_One/PythonScripts/BookToOrder/CreateBookToOrder.py)
### Screenshots of the Dataset

Below are the screenshots of the data for **Author**, **Person**, and **ShelfLocation** tables that I uploaded to the project. I created the values using the **GenerateData** and **Mockaroo** tools. For all the other tables, I created values using Python code.

**Author Table**:  
<div align="center">
  <img src="Part_One/Screenshots/Author/Image1.png" width="800" />
  <img src="Part_One/Screenshots/Author/Image2.png" width="800" />
</div>

**Person Table**:  
<div align="center">
  <img src="Part_One/Screenshots/Person/Image3.png" width="800" />
  <img src="Part_One/Screenshots/Person/Image4.png" width="800" />
  <img src="Part_One/Screenshots/Person/Image5.png" width="800" />
  <img src="Part_One/Screenshots/Person/Image7.png" width="800" />
</div>

**ShelfLocation Table**:  
<div align="center">
  <img src="Part_One/Screenshots/ShelfLocation/Image8.png" width="800" />
  <img src="Part_One/Screenshots/ShelfLocation/Image9.png" width="800" />
</div>

### Backup
**Data backup file** [View BackupFile.backup](Part_One/Backup/backup_2025_04_29.backup)  


**Recovery Test** To check that the data backup file indeed contains all the required tables and files that were in the original database, I created a new database **Restore Database** to check that everything was indeed backed up and restored as required.
<p float="left">
  <img src="Part_One/Screenshots/Backup/Image13.png" width="45%" />
  <img src="Part_One/Screenshots/Backup/Image11.png" width="45%" />
   
</p>
<p float="left">
  <img src="Part_One/Screenshots/Backup/Image14.png" width="45%" />
   <img src="Part_One/Screenshots/Backup/Image15.png" width="45%" />
</p>



## Part Two: Queries and Constraints

**Overview** In this part, we explore and implement fundamental SQL operations essential for bookstore database management. Through practical examples of queries, constraints, and transactions, we demonstrate how to effectively retrieve business insights, maintain data integrity, and safely modify database content to support day-to-day bookstore operations.
### Queries

The queries section demonstrates the practical application of SQL to extract meaningful information from our database, modify data, and maintain database integrity. These operations are essential for day-to-day bookstore management and business intelligence.

### Select Queries

This section contains SELECT queries that retrieve specific information from the database to support various business needs and decision-making processes.

**1. Select Author Books** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_author_books.sql)
   
This query retrieves all books written by a specific author, providing a comprehensive view of an author's work available in the store.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_author_books.png" width="800" />
</div>
 <br>

**2. Select Customer Order History** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_customer_order_history.sql)
   
This query retrieves a customer's complete order history, supporting customer service and personalized marketing efforts.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_customer_order_history.png" width="800" />
</div>
 <br>

**3. Select Books by Genre** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_books_by_genre.sql)
   
This query lists books by genre sorted by popularity (from most to least popular), facilitating genre-based browsing and helping customers find trending books within their preferred genres.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_books_by_genre.png" width="800" />
</div>
 <br>
 
**4. Select Books by Language** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_books_by_language.sql)
   
This query identifies books available in specific languages, supporting multilingual customer needs and inventory diversity tracking.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_books_by_language.png" width="800" />
</div>  <br>

**5. Select Books by Location** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_books_by_location.sql)
   
This query finds books based on their physical location in the store, aiding staff in quickly locating items for customers.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_books_by_location.png" width="800" />
</div> <br>

**6. Select Books by Age Group** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_books_by_age_group.sql)
   
This query identifies the top 3 most popular books for each customer age group (under 18, 18-30, 31-50, over 50), enabling targeted marketing strategies and inventory decisions based on age-specific reading preferences.   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_books_by_age_group.png" width="800" />
</div> <br>

**7. Select Low Stock Books** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_low_stock_books.sql)
   
This query identifies books with low inventory levels, helping prevent stockouts and maintain optimal inventory levels.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_low_stock_books.png" width="800" />
</div> <br>

**8. Select Monthly Sales Statistics** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_monthly_sales_stats.sql)
   
This query analyzes sales performance by month, providing valuable insights for seasonal planning and performance evaluation.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_monthly_sales_stats.png" width="800" />
</div> <br>



**9. Select Popular Books** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_popular_books.sql)
   
This query identifies the most frequently purchased books, informing restocking decisions and promotional strategies.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_popular_books.png" width="800" />
</div> <br>

**10. Select Top Club Members** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_top_club_members.sql)
   
This query identifies the most active club members based on purchase history, supporting loyalty program management and targeted marketing.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_top_club_members.png" width="800" />
</div> <br>

**11. Select Top Librarians** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_top_librarians.sql)
   
This query identifies the most productive librarians based on sales performance, aiding in staff evaluation and incentive programs.
   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_top_librarians.png" width="800" />
</div> <br>

**12. Select Top Non-Members** [View SQL](Part_Two/Queries/selectQueries/TheQueries_SQL/select_top_non_members.sql)
   
This query identifies the most active club members based on order frequency in the past year, supporting targeted promotions and loyalty rewards for existing members.   
<div align="center">
  <img src="Part_Two/Screenshots/selectQueries/select_top_non_members.png" width="800" />
</div>
<br>

#### Query Execution Results in CSV Files

The following CSV files contain the results of executing the SELECT queries described above:

1. [Author Books Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_author_books.csv) - Lists all books by specific authors
2. [Books by Age Group Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_books_by_age_group.csv) - Shows books categorized by recommended age groups
3. [Books by Genre Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_books_by_genre.csv) - Presents books organized by literary genres
4. [Books by Language Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_books_by_language.csv) - Displays books available in various languages
5. [Books by Location Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_books_by_location.csv) - Shows books organized by their physical location in the store
6. [Customer Order History Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_customer_order_history.csv) - Contains detailed purchase history for individual customers
7. [Low Stock Books Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_low_stock_books.csv) - Lists books with inventory levels below the threshold
8. [Monthly Sales Statistics Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_monthly_sales_stats.csv) - Presents sales data aggregated by month
9. [Popular Books Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_popular_books.csv) - Shows the most frequently purchased books
10. [Top Club Members Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_top_club_members.csv) - Lists the most active members based on purchase volume
11. [Top Librarians Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_top_librarians.csv) - Presents the highest-performing staff members
12. [Top Non-Members Results](Part_Two/Queries/selectQueries/RunResults_CSV/select_top_non_members.csv) - Identifies frequent customers who are not yet members

### Delete Queries

This section demonstrates DELETE operations that maintain database cleanliness by removing obsolete or unnecessary data.

**1. Delete Book Language Links** [View SQL](Part_Two/Queries/deleteQueries/delete_book_language_links.sql)
   
   This query removes language associations for books that are no longer in stock, maintaining referential integrity in the database.
   
   **During Execution:**
   <div align="center">
     <img src="Part_Two/Screenshots/deleteQueries/RUNNING_delete_book_language_links.png" width="800" />
   </div>
   
  **Before and After Execution:**
  <div align="center">
     <p float="left">
       <img src="Part_Two/Screenshots/deleteQueries/BEFORE_delete_book_language_links.png" width="20.8%" />
       <img src="Part_Two/Screenshots/deleteQueries/AFTER_delete_book_language_links.png" width="21%" />
     </p>
  </div> <br>
  

**2. Delete Obsolete Languages** [View SQL](Part_Two/Queries/deleteQueries/delete_obsolete_languages.sql)
   
   This query removes language records that are no longer associated with any books, streamlining the database.
   
   **During Execution:**
   <div align="center">
     <img src="Part_Two/Screenshots/deleteQueries/RUNNING_delete_obsolete_languages.png" width="800" />
   </div>
   
   
   **Before and After Execution:**
   <div align="center">
     <p float="left">
       <img src="Part_Two/Screenshots/deleteQueries/BEFORE_delete_obsolete_languages.png" width="39.1%" />
       <img src="Part_Two/Screenshots/deleteQueries/AFTER_delete_obsolete_languages.png" width="39.1%" />
     </p>
  </div> <br>


**3. Delete Unused Books** [View SQL](Part_Two/Queries/deleteQueries/delete_unused_books.sql)
   
   This query removes book records that have zero inventory and no recent sales, cleaning up the database.
   
   **During Execution:**
   <div align="center">
     <img src="Part_Two/Screenshots/deleteQueries/RUNNING_delete_unused_books.png" width="800" />
   </div>
   
   **Before and After Execution:**
    <div align="center">
     <p float="left">
       <img src="Part_Two/Screenshots/deleteQueries/BEFORE_delete_unused_books.png" width="39.3%" />
       <img src="Part_Two/Screenshots/deleteQueries/AFTER_delete_unused_books.png" width="39.3%" />
     </p>
 </div> 

### Update Queries

This section demonstrates UPDATE operations that modify existing data to reflect changes in business conditions or correct information.

**1. Update Book Prices** [View SQL](Part_Two/Queries/updateQueries/update_book_prices.sql)
   
   This query adjusts book prices based on popularity and inventory levels, implementing dynamic pricing strategies.
   
   **During Execution:**
   <div align="center">
     <img src="Part_Two/Screenshots/updateQueries/RUNNING_update_book_prices.png" width="800" />
   </div>
   
   **Before and After Execution:**
    <div align="center">
     <p float="center">
       <img src="Part_Two/Screenshots/updateQueries/BEFORE_update_book_prices.png" width="39.6%" />
       <img src="Part_Two/Screenshots/updateQueries/AFTER_update_book_prices.png" width="39.6%" />
     </p>
     </div><br>

**2. Update Customer Discounts** [View SQL](Part_Two/Queries/updateQueries/update_customer_discounts.sql)
   
   This query updates customer discount rates based on purchase history and membership status, rewarding loyal customers.
   
   **During Execution:**
   <div align="center">
     <img src="Part_Two/Screenshots/updateQueries/RUNNING_update_customer_discounts.png" width="800" />
   </div>
   
   **Before and After Execution:**
    <div align="center">
     <p float="center">
       <img src="Part_Two/Screenshots/updateQueries/BEFORE_update_customer_discounts.png" width="39.4%" />
       <img src="Part_Two/Screenshots/updateQueries/AFTER_update_customer_discounts.png" width="39.4%" />
     </p>
     </div><br>

**3. Update Librarian Salaries** [View SQL](Part_Two/Queries/updateQueries/update_librarian_salaries.sql)
   
   This query adjusts librarian salaries based on performance metrics and experience, supporting fair compensation practices.
   
   **During Execution:**
   <div align="center">
     <img src="Part_Two/Screenshots/updateQueries/RUNNING_update_librarian_salaries.png" width="800" />
   </div>
   
   **Before and After Execution:**
    <div align="center">
     <p float="center">
       <img src="Part_Two/Screenshots/updateQueries/BEFORE_update_librarian_salaries.png" width="39.5%" />
       <img src="Part_Two/Screenshots/updateQueries/AFTER_update_librarian_salaries.png" width="39.5%" />
     </p>
     </div>
     
### Constraints

This section demonstrates the implementation of database constraints that enforce data integrity rules, ensuring the reliability and consistency of the stored information. [View Constraints SQL](Part_Two/Constraints.sql)

**1. Author First Name Not Null**
   
This constraint ensures that every author record includes a first name, maintaining complete author information.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/authorFirstNameNotNull.png" width="800" />
</div>

**2. Author Last Name Not Null**
   
This constraint ensures that every author record includes a last name, maintaining complete author information.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/authorLastNameNotNull.png" width="800" />
</div>

**3. Book Amount Positive**
   
This constraint ensures that book quantities in orders are always positive numbers, preventing invalid order entries.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/bookAmountPositive.png" width="800" />
</div>

**4. Book Price Positive**
   
This constraint ensures that book prices are always positive values, preventing pricing errors.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/bookPricePositive.png" width="800" />
</div>

**5. Book Quantity Positive**
   
This constraint ensures that book inventory quantities are always positive numbers, maintaining accurate stock levels.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/BookQuantityPositive.png" width="800" />
</div>

**6. Floor Positive**
   
This constraint ensures that shelf location floor numbers are always positive, maintaining valid location data.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/floorPositive.png" width="800" />
</div>

**7. Member ID Unique**
   
This constraint ensures that each customer has a unique membership ID, preventing duplicate memberships.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/memberIdUnique.png" width="800" />
</div>

**8. Row Positive**
   
This constraint ensures that shelf row numbers are always positive, maintaining valid location data.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/rowPositive.png" width="800" />
</div>

**9. Shelf Positive**
   
This constraint ensures that shelf numbers are always positive, maintaining valid location data.
   
<div align="center">
  <img src="Part_Two/Screenshots/alterTable/shelfPositive.png" width="800" />
</div> 

### Rollback and Commit

This section demonstrates transaction management using ROLLBACK and COMMIT operations, which are essential for maintaining database consistency during complex operations. [View Rollback and Commit SQL](Part_Two/RollbackCommit.sql)

To perform the rollback and commit tests, I wanted to change the database for testing purposes. I wanted to create some books in the database with a quantity of 0, meaning books that were out of stock, and then restore the database to its original state - meaning a database containing only books that were in stock.

**Starting a Transaction And Some Changes**
   
To do this, first of all, I made sure that the entire database indeed contained an amount greater than zero. To do this, I ran a query that would change the quantity by selecting a random integer number:
   
<div align="center">
  <img src="Part_Two/Screenshots/RollbackCommit/Image1.png" width="800" />
</div>

 
**Saving Changes Using Commit**
   
After we saw in the run that the entire database indeed contained an amount greater than zero, we will commit the changes. That is, now the changes are saved and no book is out of stock:
   
<div align="center">
  <img src="Part_Two/Screenshots/RollbackCommit/Image2.png" width="800" />
</div>

 
**Starting a second transaction to make changes a second time**
   
In the next step, we will want to insert books with zero stock into the database for testing purposes. We will run to verify and see that some such books have indeed been inserted:
   
<div align="center">
  <img src="Part_Two/Screenshots/RollbackCommit/Image3.png" width="800" />
</div>

 
**Rollback Operation**
   
After we have performed the tests, we will want to return the database to its previous state, so that there will be no books with zero stock, so we will perform a rollback:
   
<div align="center">
  <img src="Part_Two/Screenshots/RollbackCommit/Image4.png" width="800" />
</div>  


<br>
You can see that the entire list is back to normal, with a database containing only books that are in stock as in the state we started in.



As demonstrated, the ROLLBACK command effectively undoes all changes made during the transaction, returning our database to its original consistent state with no out-of-stock books. This powerful feature allows for safe testing and protects against data corruption by ensuring operations are either fully completed or completely reversed, maintaining the integrity and reliability of our bookstore database system.
### Backup Part-Two

To ensure data safety and provide disaster recovery capabilities, a comprehensive backup of the database was created after completing all operations in Part Two.

**Data Backup File** [View Backup File](Part_Two/Backup/backup_2025_05_11.backup)

This backup contains the complete database state, including all tables, constraints, and data as of May 11, 2025. It can be used to restore the database to this point in time if needed.

## Part Three: Integration and Views

The original system was designed to manage a bookstore, including inventory tracking, order and payment records, and management of sellers and customers. The focus was exclusively on selling books to individual customers.

At this stage, I received a backup of a separate library system and was required to integrate both systems into one unified and logical solution.  
I began by considering how to conceptually combine the library system with the bookstore. The chosen approach was to treat the bookstore as a supplier of books to the library, while still serving private customers.

The library, on the other hand, manages its own borrowing system, but can request books from the bookstore as new reader demands arise.  
This results in a hybrid system where the bookstore continues selling to private customers but also acts as an official supplier to the library—enabling partial, coordinated data sharing between the two domains.

### Library Department ERD & DSD

The system describes a digital library including representations of books, copies, readers, librarians, and authors, along with operations such as borrowing, ordering, and fines. The data is connected through logical relationships enabling comprehensive and accurate tracking of library activities and daily management.

#### ERD (Entity-Relationship Diagram)  
![ERD Diagram](./Part_Three/PartnerLibraryDiagrams/ERD.png)

#### DSD (Data Structure Diagram)  
![View DSD Diagram](./Part_Three/PartnerLibraryDiagrams/DSD.png)

### Post-Integration ERD & DSD

The integrated system, after merging the library system with the bookstore, has been designed and planned following numerous changes and endless discussions on the diagrams above:

#### ERD (Entity-Relationship Diagram)  
![View ERD Diagram](./Part_Three/IntegrationDiagrams/ERD.png)

#### DSD (Data Structure Diagram)  
![View DSD Diagram](./Part_Three/IntegrationDiagrams/DSD.png)

### Integration Process and Decisions

The creation of the final database was carried out through a step-by-step renovation and correction of my existing bookstore database. The workflow was divided into two main stages:

First, I prepared the bookstore database to optimally import the backup data from the library system. This involved careful handling of identical tables to ensure that the values from both the existing data and the backup would be properly merged. This process included creating new columns, renaming tables, and creating empty tables to receive data from the new backup.

Only after successfully completing the backup import—with all data placed in the correct locations, was I able to upgrade and refine the system to the precise logical design I had planned.

First, I will attach the two relevant files through which I modified the single database into the integrated database.
These two files are like the required Integrate.sql file in the assignment, but split into two separate files for convenience.  

**Phase One: Prepare Database** [View Prepare DB Script](./Part_Three/Integrate/prepare-database-import.sql)  
**Phase Two: Complete Migration** [View Complete Migration Script](./Part_Three/Integrate/complete-database-migration.sql)


#### Phase One – Preparing the Database for Backup Import

To enable the import of the library system backup, I made adjustments to the bookstore database to fit the new data structure. The process included three main parts:

**1. Structural Preparation**

- ENUM types matching the library’s values were defined, table and column names were changed for full compatibility, and new columns were added to existing tables to handle additional information. Every change was done while checking to prevent duplicates and allow repeated script execution.

- Existing tables were backed up before structural changes to allow recovery if needed. Foreign key relationships were updated to the new names while maintaining referential integrity between entities.

- New empty tables representing entities that exist only in the library system were created to enable direct import of the backup data.

**2. Data Restoration After Import**

- After importing the backup, missing fields were restored based on existing keys. Validation commands were added to verify data integrity and detect issues early.

**3. Cleanup of Backup Tables**

- After verification and approval of system stability, deliberate cleanup of backup tables was performed to maintain a clean and organized database containing only active tables.

Throughout these stages, the bookstore database was fully adapted to safely and reliably support the import of library data.  
At this stage, the connection between the two systems was mainly technical — meaning first I wanted to create a database containing all data from the second system with all common tables and import also those that weren’t common, and only afterward begin the necessary fixes and changes to ensure the whole system works correctly also logically.

#### Phase Two – Post-Import Adjustments and Optimization

After data import, important changes were made to align the integrated system with the combined design. The commands and fixes executed at this stage aimed to unify the library and bookstore systems more from the logical perspective — ensuring all table relationships are correct, and the entire system operates in a logical and coherent collaboration as one complete and perfect system.

The optimizations included saving storage space, preventing duplication, and maintaining data consistency by updating table structures and their relationships through targeted SQL commands.

The final result from running these two scripts is a clean, normalized database supporting the combined activity of library and bookstore, with proper inheritance, referential integrity, and scalability for future expansion.

#### Conflicts and Dilemmas Encountered During the Work:

During the integration phase between the **bookstore system** and the **library system**, I encountered several **key challenges** that required **significant decisions** regarding the database structure.

First, I realized that the **table names and structures** in the two systems did **not match** each other, so **adjustments and renaming** were necessary to **prevent conflicts** when merging the data. For example, the **`Librarian`** table was renamed to **`Seller`** to accurately reflect the role of users in the integrated system, and the corresponding column in the **`Orders`** table was also renamed accordingly. Additionally, in the library system, some tables had **missing or different columns**, so I added the **necessary columns** to existing tables to allow **full preservation** of all backup data, while carefully checking for the existence of columns to avoid issues when running scripts repeatedly.

Furthermore, **new tables missing** from the bookstore system were added, such as **`Reader`**, **`Borrow`**, and **`Fine`**, which are essential for managing loans and fines in the library. This created a **new layer** that integrates library operations within the expanded system. At the same time, I **consolidated existing tables** with similar content, successfully **reducing duplication** and **improving the underlying logic** of the data — for example, unifying the link tables between books and authors and genres.

The process also presented **logical challenges**, such as the need to **separate different roles** of people in the system (**readers, sellers, librarians, authors**). Therefore, I created a **hierarchy of tables** based on a single **`Person`** parent table, from which specialized tables inherit. This decision significantly improved **data management** and **consistency**, as well as facilitating **future system extensions**.

In summary, the new system created is a **hybrid and integrated system** that efficiently combines the **commercial activity** of the bookstore with **library management**, maintaining **data integrity** and **flexibility** for various purposes, all while solving **complex design problems** that arose during the integration process.

### Views  
#### View 1: On Bookstore Orders `CustomerOrderDetails`

You can view the SQL code that defines this view here: [Book Store View SQL](./Part_Three/Views/bookStoreView.sql)  
CSV file showing the **first ten rows** of the view output: [Book Store View Data CSV](./Part_Three/Views/viewDataCSV/bookStoreViewData.csv)


This view consolidates detailed order information from the **original department's perspective** (the bookstore).  
It combines data about orders, customers, books, authors, genres, and the librarians involved in the order process.

- Displays order ID, date, final price, customer name and email, membership discount and start year.  
- Shows book details including title, author, genre, quantity ordered, price per book, and total price for the quantity.  
- Includes librarian’s name responsible for the order (if assigned).  
- Uses multiple JOINs to gather related information across tables.  
- A LEFT JOIN is used for librarian data to ensure orders without assigned librarians still appear.  
- Calculates the total book price per order item to assist revenue analysis.

This view supports rich queries to analyze sales, customer behavior, and order fulfillment.

<div align="center">
  <img src="./Part_Three/Views/screenshots/bookStore.png" width="900" />
</div>


#### View 2: On Library Borrowings  `BorrowingAndFinesDetails`

You can view the SQL code that defines this view here: [Library View SQL](./Part_Three/Views/libraryView.sql)  
CSV file showing the **first ten rows** of the view output: [Library View Data CSV](./Part_Three/Views/viewDataCSV/libraryViewData.csv)

This view presents detailed information about borrowing transactions and fines from the **receiving department's perspective** (the library).

- Shows borrowing records including borrow number, reader's name, phone, birth date, and membership start date.  
- Includes borrowing and return dates, plus a calculated status: 'Overdue', 'Returned', or 'Active'.  
- Lists related fines with reason, amount, payment status, and fine date.  
- Provides librarian contact info overseeing the borrowing and fine management.  
- Uses JOINs to combine data from Borrow, Reader, Person, Librarian, and Fine tables.  
- Uses a LEFT JOIN on fines to include borrowings without fines.

The view simplifies tracking and management of loans and fines, improving oversight and communication.

<div align="center">
  <img src="./Part_Three/Views/screenshots/library.png" width="900" />
</div>



### Queries

#### Queries for the Bookstore View `CustomerOrderDetails`

You can view the full SQL script containing all bookstore-related queries here: [View Bookstore Queries SQL](./Part_Three/Queries/bookStoreQueries.sql)  
CSV file showing the **query result** for the top-spending customers: [First Query Bookstore Data CSV](./Part_Three/Queries/viewDataCSV/firstQuerieBookStore.csv)  
CSV file showing the **query result** for the top 20 bestsellers: [Second Query Bookstore Data CSV](./Part_Three/Queries/viewDataCSV/secondQuerieBookStore.csv) 

**1. Most Active Customers**  
Display customers who spent more than 500 in the past year.

   - Filters only orders from the past year.  
   - Groups results by customer name and email.  
   - Counts the number of orders each customer placed (`COUNT(DISTINCT OrderID)`).  
   - Calculates total amount spent by each customer (`SUM(FinalPrice)`).  
   - Includes only customers who spent more than 500.  
   - Sorts the output by total spending in descending order.  

The result shows a detailed list of customers who were most engaged in purchasing over the past year. For each customer, it includes their name and contact email, the total number of distinct orders they placed, their cumulative spending above 500, and the year they began their membership. This helps identify loyal and high-value customers, enabling targeted marketing or rewards strategies. 

<div align="center">
  <img src="./Part_Three/Queries/screenshots/firstQuerieBookStore.png" width="900" />
</div>


**2. Top 20 Best-Selling Books**  
Display the 20 best-selling books in the last year.
 
   - Filters orders placed within the past year.  
   - Groups by book title, author name, and genre name.  
   - Sums the total quantity sold for each book (`SUM(BookQuantity)`).  
   - Calculates total revenue per book (`SUM(TotalBookPrice)`).  
   - Returns the top 20 books with the highest sales (`ORDER BY TotalSold DESC LIMIT 20`).  

This query highlights the most popular books in the store over the past year by aggregating sales data. It shows each book’s title, author, genre, total quantity sold, and the total revenue generated. This insight is valuable for inventory management, promotional planning, and understanding customer preferences.  

<div align="center">
  <img src="./Part_Three/Queries/screenshots/secondQuerieBookStore.png" width="900" />
</div>



#### Queries for the Library View `BorrowingAndFinesDetails`  

You can view the full SQL script containing all library-related queries here: [View Library Queries SQL](./Part_Three/Queries/libraryQueries.sql)  
CSV file showing the **query result** for overdue readers and unpaid fines: [First Query Library Data CSV](./Part_Three/Queries/viewDataCSV/firstQuerieLibrary.csv)  
CSV file showing the **query result** for borrowing patterns by age group: [Second Query Library Data CSV](./Part_Three/Queries/viewDataCSV/secondQuerieLibrary.csv)  

**1. Overdue Readers and Unpaid Fines**  
Display readers who have overdue books or unpaid fines.

   - Combines borrow and fine records from the library system.  
   - Groups by reader to count how many books are overdue and how many fines are unpaid.  
   - Sums the total amount owed.  
   - Calculates how long each reader has been active in the system.  
   - Filters based on borrowing status and fine payment status.  

The output provides detailed information about each reader with outstanding issues: their name and phone number, how many books are currently overdue, the number of unpaid fines, the total amount owed, and the duration of their membership based on their first borrowing date. This overview helps library staff prioritize follow-ups and understand reader behavior regarding returns and fines.   

<div align="center">
  <img src="./Part_Three/Queries/screenshots/firstQuerieLibrary.png" width="900" />
</div>

**2. Borrowing Patterns by Age Group**  
Analyze how different age groups borrow books over the past year.

   - Groups all borrow records by reader age group.  
   - Counts total number of readers and borrows per group.  
   - Calculates the average duration of borrowing (`AVG(return_date - borrow_date)`).  
   - Counts how many of those borrows were overdue.  
   - Helps identify trends by age demographic.  

This analysis highlights borrowing behaviors across different demographics by showing the size of each age group in terms of readers and borrowing activity, the average time books are kept, and the frequency of overdue returns. These insights support library management in tailoring services and outreach efforts to each age group’s needs and habits. 

<div align="center">
  <img src="./Part_Three/Queries/screenshots/secondQuerieLibrary.png" width="900" />
</div>



### Backup Part-Three

After successfully integrating and unifying the bookstore and library systems into a single, cohesive database, a comprehensive backup was created to ensure data safety and provide disaster recovery capabilities.

This backup includes the entire state of the combined system, capturing all merged and synchronized data from both the original library and bookstore systems after integration.

**Data Backup File** [View Backup File](./Part_Three/Backup/backup3.backup)

This backup contains all tables, constraints, and integrated data reflecting the unified system, ready for restoration if needed.

## Part Four: Functions, Procedures, Triggers & Main Program Execution
In this stage, we focused on writing advanced PL/pgSQL programs based on the database built in previous stages. The programs include functions, procedures, triggers, and main programs that simulate client-side operations. The goal of this stage was to implement complex logic on the database using programming elements such as conditions, loops, exception handling, records, and cursors.

The files are organized into folders by program type, each accompanied by a corresponding SQL file, documentation, and proof of successful execution.
### Functions
The file containing all functions can be found here [Functions](./Part_Four/SQL/functions.sql).

Below is a brief explanation of each function:

**1.** `get_all_available_copies()`  
   **Retrieve All Available Copies in the Library**

   This function returns all physical copies in the library that are currently available (i.e., not borrowed).  
It returns a table with details about the book, the copy, language, shelf location, and the condition of the copy.  
Data is retrieved from multiple tables and filtered to include only copies that are not currently loaned out.

**2.** `check_book_availability(book_id INTEGER)`  
   **Check Book Availability by Book ID**

   This function takes a book ID and checks how many available copies exist in the library.  
   It uses a cursor to return all available copies with details on their location and condition.  
   If the book is not found or no copies are available, appropriate notices are raised.

**3.** `get_book_borrowers(book_id INTEGER)`  
   **Get List of Current Borrowers for a Specific Book**

   This function returns a list of all readers who currently have copies of a specific book borrowed and not yet returned.  
   It shows information about the reader, loan and expected return dates, and the number of days overdue if applicable.  
   Exception handling is included for cases when the book is not found or no active loans exist.

**4.** `get_top_selling_books()`  
   **Retrieve Top Ten Best-Selling Books**

   This function returns the top ten best-selling books based on the number of copies sold and total revenue.  
   It uses a cursor to loop through the sales data and ranks books accordingly.  
   If no sales data is found, a notice is raised.


### Procedures
The file containing all procedures can be found here [Procedures](./Part_Four/SQL/procedures.sql).

Below is a brief explanation of each procedure:

**1.** `proc_borrow_specific_copy(p_reader_id INTEGER, p_library_copy_id INTEGER)`  
   **Borrow a Specific Library Copy**

   This procedure allows a reader to borrow a specific library copy, identified by its LibraryCopyID.
   Before proceeding, it checks whether the selected copy is already borrowed and not yet returned.
   If the copy is currently unavailable, an exception is raised.
   Otherwise, a borrow record is created and the copy is linked to that transaction.

**2.** `proc_place_multi_book_order(p_customer_id INTEGER, p_booklanguage_ids INTEGER[], p_quantities INTEGER[])`  
   **Place a Multi-Book Order**

   This procedure creates a new order for a customer that can include multiple books with specified quantities.  
   It validates that the arrays of book IDs and quantities match in length, checks stock availability for each book, and adds them to the order.  
   The total price is calculated and updated in the Orders table.  
   If stock is insufficient or a book is not found, appropriate exceptions are raised.  
   On success, a notice with the order ID and total price is displayed.


### Triggers

The file containing all triggers can be found here [Triggers](./Part_Four/SQL/triggers.sql).

Below is a brief explanation of each trigger:

**1.** `trg_update_reader_books()` (trigger function)  
   **Update Reader’s Number of Borrowed Books**

   This trigger function automatically increments the `numTakenBooks` field in the `Reader` table whenever a new borrowing entry is inserted.  
   It ensures the count of books currently borrowed by the reader is updated after an insert into the `Borrowed` table.  
   The associated trigger `trg_after_borrow_insert` fires **after insert** on the `Borrowed` table to execute this function.

**2.** `trg_update_inventory_after_order()` (trigger function)  
   **Update Inventory After New Order Item**

   This trigger function updates the bookstore inventory by subtracting the quantity of a newly ordered book from the stock.  
   It is executed after an insert on the `OrderItem` table via the trigger `trg_after_orderitem_insert`.  
   This keeps the inventory stock accurate and reflects items sold.  
   (Optional validation to prevent negative stock levels can be added.)

### Main Programs
#### Main Program 1: Book Borrowing
You can view the first main program code here [main_borrow_interactive.sql](./Part_Four/MainPrograms/mainFirst.sql)  
This main procedure guides the process of borrowing a book from the library in five continuous steps:

**1.** The program begins by prompting the user to enter the Book ID they wish to borrow and their Reader ID. In this implementation, the inputs are simulated (hardcoded) rather than dynamically entered by the user.

**2.** It then checks whether any available copies of the requested book exist by calling the function [`check_book_availability`](#check_book_availabilitybook_id-integer). This function searches the database for copies of the specified book that are not currently borrowed. The procedure counts the returned rows to determine availability.

**3.** If copies are available, the user is shown a list of all available copies with detailed information, such as language, condition, shelf, floor, and row. This information is again retrieved using [`check_book_availability`](#check_book_availabilitybook_id-integer). The user is then prompted to choose a specific copy by its LibraryCopyID, and the corresponding BookLanguageID is retrieved from the `LibraryCopy` table.

**4.** The procedure proceeds to call [`proc_borrow_book_by_lang_id`](#proc_borrow_book_by_lang_idp_reader_id-integer-p_booklanguage_id-integer), which performs the actual borrowing process. It assigns the selected book copy to the reader and inserts a new borrow record into the system. Following this step, the trigger [`trg_update_reader_books`](#trg_update_reader_books-trigger-function) is automatically fired, updating the reader’s `numTakenBooks` count in the `Reader` table.

**5.** If no copies are available, the procedure calls the function [`get_book_borrowers`](#get_book_borrowersbook_id-integer) to retrieve information about current borrowers of that book. It then prints details such as the borrower's name, borrow date, and days overdue (if applicable), and informs the user that they will be notified once a copy becomes available.

#### Summary

This main program acts as the interactive core of the borrowing system. It checks for available copies, guides the user through the selection process, initiates the borrowing operation, and ensures that all relevant tables and triggers are updated accordingly. In cases of unavailability, it provides transparency into current loans, offering a clear and helpful user experience.

#### Main Program 2: Ordering from the Bookstore
You can view the code for the second main program here [main_order_books.sql](./Part_Four/MainPrograms/mainSecond.sql)  
This main procedure allows a customer to place an order for one or more books from the bookstore. The process unfolds in five continuous steps:

**1.** The procedure starts by displaying a list of the top 10 best-selling books using the function [`get_top_selling_books`](#get_top_selling_books). The list includes rank, book title, author, total copies sold, and total revenue, giving the customer a quick overview of popular choices.

**2.** The user is then prompted to enter their Customer ID. This ID is used to associate the order with the correct customer in the system. (In this version, the ID is hardcoded for demonstration purposes.)

**3.** A new order record is created in the `Orders` table with today's date, order type, a starting total price of 0, the seller ID, and the provided customer ID. The newly created `OrderID` is saved for use in the next steps.

**4.** The program enters a loop that enables the customer to add multiple books to the order. For each item:
   - The customer is asked to enter the `BookLanguageID` of the book they want to order.
   - The program checks stock availability from the `BookstoreInventory`.
   - If the stock is sufficient, the user specifies the quantity they want.
   - The quantity is validated against the stock, and if it's valid, an entry is added to the `OrderItem` table.
   - At this point, the trigger [`trg_update_inventory_after_order`](#trg_update_inventory_after_order-trigger-function) is automatically activated, reducing the available stock accordingly.
   - The customer is then asked if they wish to add another item to the order.

**5.** After all items have been added, the program calculates the final total price for the order. This is done by summing up the quantity of each item multiplied by its unit price, taken from the `BookstoreInventory`. The result is stored back in the `Orders` table under `FinalPrice`. Finally, a message confirms the successful completion of the order and displays the order number.

#### Summary

This main program simulates a dynamic and interactive ordering system for the bookstore. It presents top-selling books to the customer, creates a new order, allows adding multiple books with quantity validation, and ensures that the stock is accurately updated through a trigger. In the end, it updates the order’s total price, completing a smooth and traceable purchase flow.


### Demonstration Screenshots
Below are screenshots demonstrating the execution of the `main_place_order_interactive` procedure:
#### Main Program 1: Book Borrowing

We inserted fixed values instead of real user input for testing purposes.
We simulated a reader with ReaderID = 30 wanting to borrow a book with BookID = 343.
The program checked and displayed available copies of that book in the library.
The reader selected the copy with LibraryCopyID = 405.
The borrow transaction was successfully created.

 - The Borrow and Borrowed tables were updated accordingly after the procedure executed.  
 - The reader's NumTakenBooks counter was automatically updated by a trigger.  
 - If no copies were available, the program displayed the current borrowers with borrow dates and overdue information.  
 - If the reader tries to borrow more books than their limit, an exception is raised and the borrow is rejected.  
<!-- עטיפה כוללת ברוחב קבוע ומרכז -->
<div style="width: 1000px; margin: auto;">

  <!-- שתי התמונות הראשונות בשורה אחת, באותו גובה, במרכז ובמרווח בין -->
  <div style="display: flex; justify-content: center; gap: 20px; align-items: center; margin-bottom: 20px;">
    <img src="./Part_Four/Screenshots/RunningFirstMainProgram/CopiesAvailable.png" alt="Copies Available" style="height: 700px; object-fit: contain;">
    <img src="./Part_Four/Screenshots/RunningFirstMainProgram/CopiesUnavailable.png" alt="Copies Unavailable" style="height: 700px; object-fit: contain;">
  </div>

  <!-- שאר התמונות כל אחת בשורה משלה, רחבות למקסימום ומרכזיות -->
  <div style="display: flex; flex-direction: column; gap: 20px; align-items: center;">
    <img src="./Part_Four/Screenshots/RunningFirstMainProgram/BorrowAfter.png" alt="Borrow After" style="max-width: 100%; height: auto;">
    <img src="./Part_Four/Screenshots/RunningFirstMainProgram/BorrowedAfter.png" alt="Borrowed After" style="max-width: 100%; height: auto;">
    <img src="./Part_Four/Screenshots/RunningFirstMainProgram/NumTakenBooksBefore.png" alt="Num Taken Books Before" style="max-width: 100%; height: auto;">
    <img src="./Part_Four/Screenshots/RunningFirstMainProgram/NumTakenBooksAfter.png" alt="Num Taken Books After" style="max-width: 100%; height: auto;">
    <img src="./Part_Four/Screenshots/RunningFirstMainProgram/BookLimitExeption.png" alt="Book Limit Exception" style="max-width: 100%; height: auto;">
  </div>

</div>

#### Main Program 2: Ordering from the Bookstore  
We inserted fixed values instead of real user input for testing purposes.  
We simulated an order for book with `BookLanguageID = 302`.  
As shown in the run, 41 copies of this book were available in stock.  
We requested 12 copies for our order. That was all we wanted to order, and the order was placed successfully.
- In the `OrderItem` and `Orders` tables after the procedure executed.
- And in the `BookstoreInventory` table after the trigger automatically reduced the stock.  

<div style="width: 1000px; margin: auto;">

  <!-- תמונה ראשונה -->
  <img src="./Part_Four/Screenshots/RunningSecondMainProgram/successfulRun.png" alt="Successful order run" style="width: 100%; margin-bottom: 20px;">

  <!-- תמונה חדשה אחת, ברוחב מלא -->
  <img src="./Part_Four/Screenshots/RunningSecondMainProgram/final.png" alt="Final result table" style="width: 100%;">

</div>



### PL/pgSQL Exceptions
1. **check_book_availability - Book not found in library**  
Explanation: Ensures the book exists before returning available copies.    

    ```plpgsql
    RAISE EXCEPTION 'Book with ID % not found in library', book_id;
   ```
2. **check_book_availability - No copies available**  
Explanation: Indicates no available copies because all are currently borrowed, returns no results.

     ```plpgsql
      RAISE NOTICE 'No copies available for book ID % - all copies are currently borrowed', book_id;
      RETURN;
      ```
3. **check_book_availability - General error handling**  
Explanation: Catches any unexpected errors and reports them.
      ```plpgsql
      EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in check_book_availability: %', SQLERRM;
        RAISE;
      ```
4. **get_book_borrowers - Book not found**  
Explanation: Checks if the book exists before returning borrower info.
   ```plpgsql
      RAISE EXCEPTION 'Book with ID % not found', book_id;
      ```
5. **get_book_borrowers - No active borrowers**  
Explanation: Indicates there are no active borrowers currently.
    ```plpgsql
     RAISE NOTICE 'No current borrowers found for book ID: %', book_id;
     RETURN;
      ```
6. **get_book_borrowers - General error handling**  
Explanation: Catches and reports errors.
     ```plpgsql
    EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in get_book_borrowers: %', SQLERRM;
        RAISE;
      ```
7. **get_top_selling_books - No sales data**  
Explanation: Indicates no sales data is available in the system.
   ```plpgsql
   RAISE NOTICE 'No sales data found in the system';
   RETURN;
   ```
8. **get_top_selling_books - No books with sales data found**  
Explanation: Indicates no books were found with sales information.
   ```plpgsql
   RAISE NOTICE 'No books found with sales data';
   ```
9. **get_top_selling_books - General error handling**  
Explanation: Catches any unexpected errors and reports them.
    ```plpgsql
    EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in get_top_selling_books: %', SQLERRM;
        RAISE;
    ```
10. **proc_borrow_specific_copy - Copy already borrowed**  
Explanation: Prevents borrowing a copy that is currently on loan.
    ```plpgsql
    RAISE EXCEPTION 'This copy is already borrowed.';
    ```
11. **proc_place_multi_book_order - Array length mismatch**  
Explanation: Ensures the order parameters arrays have matching lengths.
    ```plpgsql 
    RAISE EXCEPTION 'BookLanguageID array and quantity array must be of the same length';
     ```
12. **proc_place_multi_book_order - Book not found in inventory**  
Explanation: Prevents adding an item not present in stock.
     ```plpgsql 
     RAISE EXCEPTION 'BookLanguageID % not found in inventory', p_booklanguage_ids[i];
     ```
13. **proc_place_multi_book_order - Insufficient stock**  
Explanation: Prevents ordering quantity greater than available stock.
    ```plpgsql
    RAISE EXCEPTION 'Not enough stock for BookLanguageID %: Available %, Requested %',
    p_booklanguage_ids[i], v_stock, p_quantities[i];
    ```
14. **main_place_order_interactive - Error handling during order**  
Explanation: Reports error, cancels order, and stops loop.
    ```plpgsql
     EXCEPTION
     WHEN OTHERS THEN
        RAISE NOTICE 'Error: %', SQLERRM;
        RAISE NOTICE 'Order cancelled due to error.';
        v_continue := FALSE;
        v_error_occurred := TRUE;
       ```
15. **main_borrow_interactive - No available copies**  
Explanation: Notifies no available copies and shows current borrowers. 
     ```plpgsql 
     RAISE NOTICE 'No available copies. Showing current borrowers of BookID %:', v_book_id;
     ```

### Backup Part-Four

After completing the implementation of advanced PL/pgSQL programs — including functions, procedures, triggers, and interactive main programs — a full backup of the enhanced database was created to preserve the current state of the system.

This backup captures all developed logic, code, and structural changes applied during this programming stage, such as:
- Custom business logic through non-trivial functions and procedures
- Trigger-based automation for consistent data handling
- Main programs that simulate real-world scenarios in the system

**Data Backup File** [View Backup File](./Part_Four/Backup/backup4.backup)

This backup reflects the complete and updated version of the extended unified system after all logical and structural enhancements of Part Four.

## Part Five: Graphical User Interface

In this final stage, a desktop graphical user interface was developed to interact directly with the integrated Bookstore/Library database built in Parts One through Four. The application allows a user to browse, create, update and delete records, run reporting queries from Part Two, and trigger the PL/pgSQL functions and procedures written in Part Four — all without writing SQL by hand.

### Technology Stack

- **Language:** Python 3
- **GUI Framework:** Tkinter (`tkinter`, `tkinter.ttk`) - the standard Python GUI toolkit, chosen for its simplicity and native integration with Python, requiring no external GUI runtime.
- **Database Driver:** `psycopg2` - connects directly to the PostgreSQL database built in Parts One-Four.
- **Charts:** `matplotlib`, embedded inside Tkinter windows via `FigureCanvasTkAgg`, used for the statistics dashboards.

### Application Architecture

The code is organized into four parts:

- **`main.py`** - the application's entry point. It builds the main menu window and opens every other screen as a `Toplevel` window on demand.
- **`config.py`** - holds the PostgreSQL connection settings (host, port, database name, user, password).
- **`db_manager.py`** - a shared data-access layer. Every CRUD operation and every call to a Part Four function/procedure is wrapped here in a dedicated Python function, so the screen files never contain raw SQL for basic operations.
- **`screens/`** - a package containing one module per database table's CRUD screen (`reader_gui.py`, `book_gui.py`, `booklanguage_gui.py`, `bookstoreinventory_gui.py`, `borrow_gui.py`, `borrowed_gui.py`, `language_gui.py`, `librarycopy_gui.py`, `orderitem_gui.py`, `orders_gui.py`). Each module defines one class implementing a full Create/Read/Update/Delete screen for its table.

### Main Menu Layout

Launching the application (`python main.py`) opens a single main window, divided into **six labeled category panels** side by side. Each panel is a `LabelFrame` containing buttons; every button opens a dedicated window for that specific action:

1. **CRUD Table Management** ("ניהול טבלאות CRUD")
2. **Information Functions** ("פונקציות מידע") - includes a nested **Statistics** panel
3. **Queries**
4. **Procedures** ("פרוצדורות")
5. **Main Programs** ("תוכניות ראשיות")

This main window is the required "entry screen" from which every other screen in the system can be reached.

### CRUD Management Screens

Ten buttons, one per table: **Reader, BookstoreInventory, BookLanguage, Language, Book, LibraryCopy, Borrow, Borrowed, Orders, OrderItem** (this satisfies the requirement of at least 3 CRUD-capable tables including a junction table, since `OrderItem` and `Borrowed` both link two other tables together).

Every CRUD screen follows the same consistent pattern:
- Four **Radiobuttons** to switch mode: Create / Read / Update / Delete.
- A form with one input field per column; fields are automatically enabled/disabled/read-only depending on the selected mode.
- A single **Execute** button whose label and behaviour change per mode (e.g. "Add Reader", "Search Reader", "Load for Update" → "Update Reader", "Delete Reader").
- A results table (`ttk.Treeview`) showing all current rows, with a live row-count label above it.
- Clicking a row in the table auto-fills the form (for Read/Update).
- Client-side validation (e.g. phone number format, date format `YYYY-MM-DD`) before sending data to the database.
- A confirmation dialog before any Delete operation.

### Information Function Screens

Four buttons that call the PL/pgSQL **functions** written in Part Four and display the results in a table, each with a short Hebrew description panel explaining what the function does:

- **"הצג עותקים זמינים בספריה"** (Show available library copies) - optional BookID filter, calls `get_available_copies`.
- **"הצג השאלות פעילות בספריה"** (Show active borrows) - optional BookID filter, calls `get_current_borrowers`.
- **"ספירת עותקים לכל ספר"** (Copy count for a book) - takes a BookID, calls `get_book_copy_count`.
- **"הצג את הספרים הנמכרים ביותר"** (Show top-selling books) - calls `get_top_selling_books`, no input required.

### Statistics Screens

Two analytics dashboards, combining KPI text tiles with `matplotlib` charts embedded in the Tkinter window:

- **"סטטיסטיקות חנות הספרים"** (Bookstore Analytics): total revenue, total orders, average order value, and low-stock item count as KPI tiles; a table of top-selling genres; a pie chart of customer types (Individual vs. Library); a bar chart of the top 5 selling genres.
- **"סטטיסטיקות הספריה"** (Library Analytics): total borrows, active readers, return rate, and unpaid fines as KPI tiles; a bar chart of the top 5 most-borrowed genres with a color legend; a pie chart comparing overdue vs. on-time borrows.

### Query Screens

Six buttons, each running one of the SELECT queries from Part Two (or a close variant adapted for the integrated schema) directly against the database, displayed with a description panel and a results table:

- **"הצג מלאי נמוך בחנות הספרים"** - books with stock below 5, joined with author/language/genre and total units sold.
- **"הצג 10 הזמנות אחרונות"** - the 10 most recent orders, with customer, seller, discount, item count, total price and the list of books ordered.
- **"חיפוש ספרים לפי ז'אנר וגיל"** - a filterable search (genre dropdown + age-group dropdown) showing each book's availability in both the bookstore and the library.
- **"הצג 10 קנסות אחרונים"** - the 10 most recent fines, with reader, librarian, dates, amount, reason and payment status.
- **"הצג מלאי בחנות הספרים"** - the full bookstore stock list, sorted by quantity.
- **"הצג ספרים זמינים בספריה"** - every library copy that is not currently borrowed.

### Procedure Screens

Two guided forms, each calling one of the Part Four **procedures** directly:

- **"השאלת ספר בספריה"** → calls `create_new_borrow(reader_id, librarian_id, copy_ids[])`. The user enters a Reader ID and a Librarian ID (with "הצג קוראים" / "הצג ספרנים" lookup buttons to browse valid IDs), then multi-selects one or more currently-available library copies from a listbox. The form validates that the reader and librarian IDs actually exist before calling the procedure, and displays the database's `RAISE NOTICE` message as a success popup.
- **"בצע הזמנה בחנות הספרים"** → calls `create_new_order(customer_id, seller_id, booklanguage_ids[], quantities[])`. The user enters a Customer ID (with a "הצג לקוחות" lookup) — the form automatically detects and displays whether this is an **"הזמנת ספריה"** (Library-type) or **"הזמנה פרטית"** (Individual-type) order based on the customer's `CustomerType` — and a Seller ID (with a "הצג מוכרים" lookup). The user then multi-selects books from the in-stock catalog, sets a quantity per book (capped at available stock via a Spinbox), and submits; the database's success notice is shown to the user.

### Main Program Screens

Two end-to-end guided "wizards" that reuse the Part Four functions and procedures to simulate a full real-world flow:

- **"ביצוע השאלה בספריה"** (Library borrow wizard): live-validates a Reader ID, lets the user search/filter a book catalog with available-copy counts, shows the specific available copies of the selected book (shelf location, condition, language), and performs the borrow with a single click (also supports double-click and the `Ctrl+Enter` / `Ctrl+B` keyboard shortcuts). If no copies are available, it automatically shows the book's current borrowers instead.
- **"ביצוע הזמנה בחנות הספרים"** (Bookstore order wizard): opens by showing the current Top-10 best-selling books, live-validates a Customer ID and displays their discount percentage, lets the user search the in-stock catalog and add items to a floating shopping-cart window (with quantity +/- controls and a running total that already applies the customer's discount), and finally shows a checkout summary before placing the order.

Together, the CRUD, Query, Procedure and Main Program screens add up to well over the minimum of 5 required screens.

### How to Run the Application

Full setup and run instructions are provided in a separate file: [RunInstructions.md](Part_Five/RunInstructions.md).

In short: make sure the PostgreSQL database from Part Four is running and reachable, install the Python dependencies (`psycopg2-binary`, `matplotlib`, `numpy`, `pillow`), then run:

```bash
python main.py
