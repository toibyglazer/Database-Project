import csv
import random
import os
from faker import Faker

# Initialize Faker for generating random book names
fake = Faker()

# Settings
NUM_BOOKS = 400
NUM_AUTHORS = 400
NUM_SHELF_LOCATIONS = 400
NUM_GENRES = 50

# List of common words in book titles to create more realistic titles
title_prefixes = ["The", "A", "My", "Our", "Their", "Her", "His", "Ancient", "Modern", "Secret", "Hidden", "Lost", "Forgotten"]
title_subjects = ["Journey", "Adventure", "Mystery", "Story", "Tale", "Chronicles", "Saga", "Legend", "Myth", "History", "Life", "Love", "War", "Peace", "Dream", "Nightmare", "Secret", "Quest", "Path", "Road", "Way", "Garden", "Forest", "Mountain", "River", "Ocean", "Sky", "Star", "Moon", "Sun", "Shadow", "Light", "Darkness", "Fire", "Ice", "Wind", "Storm", "Thunder", "Lightning", "Rain", "Snow", "Winter", "Summer", "Spring", "Fall", "Dawn", "Dusk", "Night", "Day"]
title_suffixes = ["of Time", "of Destiny", "of Fate", "of the Ancients", "of the Future", "of the Past", "of the Present", "of the Unknown", "of the Forgotten", "of the Remembered", "of the Lost", "of the Found", "of the Hidden", "of the Revealed", "of the Sacred", "of the Profane", "of the Divine", "of the Mundane", "of the Extraordinary", "of the Ordinary", "of the Impossible", "of the Possible", "of the Improbable", "of the Probable", "of the Unlikely", "of the Likely", "of the Unexpected", "of the Expected", "of the Surprising", "of the Unsurprising"]

# Function to generate a random book title
def generate_book_title():
    if random.random() < 0.7:  # 70% of titles will have a complex structure
        prefix = random.choice(title_prefixes) if random.random() < 0.7 else ""
        subject = random.choice(title_subjects)
        suffix = random.choice(title_suffixes) if random.random() < 0.5 else ""
        
        title = f"{prefix} {subject}" if prefix else subject
        title = f"{title} {suffix}" if suffix else title
        
        return title.strip()
    else:  # 30% of titles will be from Faker
        return fake.catch_phrase()

def generate_book_data():
    """Generates book data"""
    books = []
    
    # Create a list of unique titles
    book_titles = set()
    while len(book_titles) < NUM_BOOKS:
        title = generate_book_title()
        if len(title) <= 100:  # Ensure the title is not too long
            book_titles.add(title)
    
    book_titles = list(book_titles)
    
    # Create books
    for book_id in range(1, NUM_BOOKS + 1):
        # Book title
        title = book_titles[book_id - 1]
        
        # Publication year (between 1900 and 2024)
        publication_year = random.randint(1900, 2024)
        
        # Price (between 30 and 200 NIS)
        price = round(random.uniform(30, 200), 2)
        
        # Quantity in stock (between 1 and 50)
        amount = random.randint(1, 50)
        
        # Shelf location ID (between 1 and 400)
        shelf_location_id = random.randint(1, NUM_SHELF_LOCATIONS)
        
        # Author ID (between 1 and 400)
        author_id = random.randint(1, NUM_AUTHORS)
        
        # Genre ID (between 1 and 50)
        genre_id = random.randint(1, NUM_GENRES)
        
        # Add the book to the list
        books.append({
            'BookID': book_id,
            'TitleBookName': title,
            'PublicationYear': publication_year,
            'price': price,
            'amount': amount,
            'ShelfLocationID': shelf_location_id,
            'AuthorID': author_id,
            'GenreID': genre_id
        })
    
    return books

def save_to_csv(books):
    """Saves book data to a CSV file"""
    # Create output directory in the current directory if it doesn't exist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, 'BookList.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['BookID', 'TitleBookName', 'PublicationYear', 'price', 'amount', 'ShelfLocationID', 'AuthorID', 'GenreID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    
    print(f"CSV file created with {len(books)} rows: {output_file}")
    return output_file

def main():
    """Main function"""
    try:
        print("Generating book data...")
        books = generate_book_data()
        output_file = save_to_csv(books)
        
        # Display 10 examples
        print("\n10 sample rows:")
        for book in books[:10]:
            print(f"{book['BookID']},{book['TitleBookName']},{book['PublicationYear']},{book['price']},{book['amount']},{book['ShelfLocationID']},{book['AuthorID']},{book['GenreID']}")
        
        # Statistics
        print("\nStatistics:")
        
        # Calculate genre distribution
        genre_counts = {}
        for book in books:
            genre_id = book['GenreID']
            genre_counts[genre_id] = genre_counts.get(genre_id, 0) + 1
        
        print(f"Number of unique genres: {len(genre_counts)}")
        print(f"Average books per genre: {NUM_BOOKS / len(genre_counts):.2f}")
        
        # Calculate author distribution
        author_counts = {}
        for book in books:
            author_id = book['AuthorID']
            author_counts[author_id] = author_counts.get(author_id, 0) + 1
        
        print(f"Number of unique authors: {len(author_counts)}")
        print(f"Average books per author: {NUM_BOOKS / len(author_counts):.2f}")
        print(f"Maximum number of books by a single author: {max(author_counts.values())}")
        
        print(f"\nData successfully saved to file: {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()