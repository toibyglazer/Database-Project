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




