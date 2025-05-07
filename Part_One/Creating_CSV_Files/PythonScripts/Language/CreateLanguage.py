import csv
import random
import os
import urllib.request

# URL of the BookLanguage CSV file
BOOK_LANGUAGE_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/BookLanguage-IiAVKfDQLDbavYwRluaO1VRoTYRvww.csv"

# Settings
NUM_BOOKS = 400
NUM_LANGUAGES = 60
MIN_LANGUAGES_PER_BOOK = 1
MAX_LANGUAGES_PER_BOOK = 3  # Maximum number of languages per book
TOTAL_RELATIONSHIPS = 800   # Approximate number of book-language relationships to generate

# Language popularity weights (some languages are more common than others)
# The first few languages will be more common (like English, Spanish, Chinese, etc.)
def get_language_weights():
    weights = []
    for i in range(1, NUM_LANGUAGES + 1):
        if i <= 5:  # Top 5 languages are more common
            weights.append(10)
        elif i <= 15:  # Next 10 languages are somewhat common
            weights.append(5)
        else:  # The rest are less common
            weights.append(1)
    return weights

def download_csv(url, local_filename):
    """Download a CSV file from a URL"""
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(local_filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Download the file
        print(f"Downloading {url} to {local_filename}...")
        
        # Use urllib with SSL verification disabled if needed
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        
        urllib.request.urlretrieve(url, local_filename)
        print(f"Download complete: {local_filename}")
        return True
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return False

def load_csv(filename):
    """Load data from a CSV file"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Error loading CSV file {filename}: {str(e)}")
        return None

def generate_language_relationships():
    """Generate relationships between books and languages"""
    language_relationships = []
    
    # Track which combinations we've already created to avoid duplicates
    # (since BookID, LanguageID is a primary key)
    combinations = set()
    
    # Language weights for weighted random selection
    language_weights = get_language_weights()
    
    # First, ensure each book has at least one language
    for book_id in range(1, NUM_BOOKS + 1):
        # Decide how many languages this book will have
        num_languages = random.randint(MIN_LANGUAGES_PER_BOOK, MAX_LANGUAGES_PER_BOOK)
        
        # Select languages for this book using weighted random selection
        selected_languages = random.choices(
            range(1, NUM_LANGUAGES + 1),
            weights=language_weights,
            k=min(num_languages, NUM_LANGUAGES)  # Can't select more languages than exist
        )
        
        # Remove duplicates (in case random.choices selected the same language twice)
        selected_languages = list(set(selected_languages))
        
        # Add relationships for this book
        for language_id in selected_languages:
            if (book_id, language_id) not in combinations:
                language_relationships.append({
                    'BookID': book_id,
                    'LanguageID': language_id
                })
                combinations.add((book_id, language_id))
    
    # If we need more relationships to reach TOTAL_RELATIONSHIPS, add random ones
    while len(language_relationships) < TOTAL_RELATIONSHIPS:
        book_id = random.randint(1, NUM_BOOKS)
        language_id = random.choices(
            range(1, NUM_LANGUAGES + 1),
            weights=language_weights,
            k=1
        )[0]
        
        if (book_id, language_id) not in combinations:
            language_relationships.append({
                'BookID': book_id,
                'LanguageID': language_id
            })
            combinations.add((book_id, language_id))
    
    return language_relationships

def save_to_csv(data, filename):
    """Save data to a CSV file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, filename)
    
    if not data:
        print(f"No data to save to {output_file}")
        return None
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"CSV file created with {len(data)} rows: {output_file}")
    return output_file

def main():
    """Main function"""
    try:
        print("Starting Language table generation...")
        
        # Create temporary directory for downloaded files
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # Download BookLanguage CSV file to verify language IDs
        book_language_file = os.path.join(temp_dir, 'BookLanguage.csv')
        
        if not download_csv(BOOK_LANGUAGE_URL, book_language_file):
            print("Failed to download BookLanguage.csv, but continuing anyway...")
        else:
            # Load language data to verify
            language_data = load_csv(book_language_file)
            if language_data:
                print(f"Loaded {len(language_data)} languages from BookLanguage.csv")
                
                # Verify language IDs
                language_ids = set(int(lang['LanguageID']) for lang in language_data if lang['LanguageID'].isdigit())
                if max(language_ids, default=0) != NUM_LANGUAGES or min(language_ids, default=0) != 1:
                    print(f"Warning: Expected language IDs 1-{NUM_LANGUAGES}, but found range {min(language_ids, default=0)}-{max(language_ids, default=0)}")
        
        # Generate language relationships
        print("Generating language relationships...")
        language_relationships = generate_language_relationships()
        
        # Save to CSV
        language_file = save_to_csv(language_relationships, 'Language.csv')
        
        # Display statistics
        print("\nStatistics:")
        print(f"Total book-language relationships: {len(language_relationships)}")
        
        # Count languages per book
        book_counts = {}
        for rel in language_relationships:
            book_id = rel['BookID']
            book_counts[book_id] = book_counts.get(book_id, 0) + 1
        
        print(f"Average languages per book: {sum(book_counts.values()) / len(book_counts):.2f}")
        print(f"Maximum languages per book: {max(book_counts.values())}")
        
        # Count books per language
        language_counts = {}
        for rel in language_relationships:
            language_id = rel['LanguageID']
            language_counts[language_id] = language_counts.get(language_id, 0) + 1
        
        print(f"Average books per language: {sum(language_counts.values()) / len(language_counts):.2f}")
        print(f"Maximum books per language: {max(language_counts.values())}")
        
        # Display 10 sample relationships
        print("\n10 sample book-language relationships:")
        for rel in language_relationships[:10]:
            print(f"{rel['BookID']},{rel['LanguageID']}")
        
        print(f"\nData successfully saved to file: {language_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()