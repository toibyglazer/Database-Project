CREATE TABLE IF NOT EXISTS Person
(
  ID INT NOT NULL,
  FirstName VARCHAR(50) NOT NULL,
  LastName VARCHAR(50) NOT NULL,
  Email VARCHAR(100),
  PhoneNumber VARCHAR(20),
  BirthDate DATE,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Customer
(
  CustomerID INT NOT NULL,
  IDmember INT UNIQUE,
  Discount NUMERIC(5,2),
  StartYearMember INT,
  PRIMARY KEY (CustomerID),
  FOREIGN KEY (CustomerID) REFERENCES Person(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Librarian
(
  LibrarianID INT NOT NULL,
  StartWorkDate DATE NOT NULL,
  ExperienceYears INT,
  age INT,
  Salary NUMERIC(10,2) NOT NULL,
  PRIMARY KEY (LibrarianID),
  FOREIGN KEY (LibrarianID) REFERENCES Person(ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ShelfLocation
(
  ShelfLocationID INT NOT NULL,
  Floor INT NOT NULL,
  RowNum INT NOT NULL,
  ShelfNumber INT NOT NULL,
  PRIMARY KEY (ShelfLocationID)
);

CREATE TABLE IF NOT EXISTS Author
(
  AuthorID INT NOT NULL,
  FirstName VARCHAR(50) NOT NULL,
  LastName VARCHAR(50) NOT NULL,
  Nationality VARCHAR(50),
  PRIMARY KEY (AuthorID)
);

CREATE TABLE IF NOT EXISTS GenreTypes
(
  GenreID INT NOT NULL,
  GenreName VARCHAR(50) NOT NULL,
  MinAge INT,
  PRIMARY KEY (GenreID)
);

CREATE TABLE IF NOT EXISTS BookLanguage
(
  LanguageID INT NOT NULL,
  LanguageName VARCHAR(50) NOT NULL,
  MainCountry VARCHAR(50),
  PRIMARY KEY (LanguageID)
);

CREATE TABLE IF NOT EXISTS BookList
(
  BookID INT NOT NULL,
  TitleBookName VARCHAR(100) NOT NULL,
  PublicationYear INT,
  price NUMERIC(10,2),
  amount INT NOT NULL,
  ShelfLocationID INT,
  AuthorID INT,
  GenreID INT,
  PRIMARY KEY (BookID),
  FOREIGN KEY (ShelfLocationID) REFERENCES ShelfLocation(ShelfLocationID),
  FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID),
  FOREIGN KEY (GenreID) REFERENCES GenreTypes(GenreID)
);

CREATE TABLE IF NOT EXISTS Language
(
  BookID INT NOT NULL,
  LanguageID INT NOT NULL,
  PRIMARY KEY (BookID, LanguageID),
  FOREIGN KEY (BookID) REFERENCES BookList(BookID) ON DELETE CASCADE,
  FOREIGN KEY (LanguageID) REFERENCES BookLanguage(LanguageID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Order_Table
(
  OrderID INT NOT NULL,
  OrderDate DATE NOT NULL,
  FinalPrice NUMERIC(10,2) NOT NULL,
  CustomerID INT NOT NULL,
  LibrarianID INT,
  PRIMARY KEY (OrderID),
  FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
  FOREIGN KEY (LibrarianID) REFERENCES Librarian(LibrarianID)
);

CREATE TABLE IF NOT EXISTS BookToOrder
(
  OrderID INT NOT NULL,
  BookID INT NOT NULL,
  BookQuantity INT NOT NULL,
  PRIMARY KEY (OrderID, BookID),
  FOREIGN KEY (OrderID) REFERENCES Order_Table(OrderID) ON DELETE CASCADE,
  FOREIGN KEY (BookID) REFERENCES BookList(BookID) ON DELETE CASCADE
);