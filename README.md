# Book Store
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
- [Part Two: Integration](#part-two-integration)
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
  <img src="Part_One/Screenshots/Person/Image6.png" width="800" />
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


