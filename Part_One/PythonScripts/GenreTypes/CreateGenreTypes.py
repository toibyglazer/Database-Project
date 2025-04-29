import csv
import os
import sys
import traceback

# List of 50 book genres with appropriate minimum ages
genres_min_ages = [
    ("Fiction", 12),
    ("Non-Fiction", 14),
    ("Fantasy", 10),
    ("Mystery", 12),
    ("Science Fiction", 13),
    ("Biography", 15),
    ("Romance", 16),
    ("Thriller", 14),
    ("Horror", 16),
    ("Historical Fiction", 12),
    ("Young Adult", 13),
    ("Children's", 5),
    ("Adventure", 10),
    ("Poetry", 12),
    ("Drama", 14),
    ("Satire", 15),
    ("Self-Help", 14),
    ("Memoir", 15),
    ("Travel", 10),
    ("Cookbook", 8),
    ("Art", 10),
    ("Philosophy", 16),
    ("Psychology", 16),
    ("History", 12),
    ("Science", 12),
    ("Technology", 13),
    ("Business", 16),
    ("Economics", 16),
    ("Politics", 16),
    ("Religion", 14),
    ("Sports", 10),
    ("Music", 10),
    ("Comics", 8),
    ("Graphic Novel", 12),
    ("Dystopian", 14),
    ("Paranormal", 14),
    ("Mythology", 12),
    ("Fairy Tale", 6),
    ("Western", 12),
    ("Crime", 15),
    ("Detective", 13),
    ("Suspense", 14),
    ("Action", 12),
    ("Comedy", 10),
    ("Short Story", 12),
    ("Essay", 15),
    ("Reference", 10),
    ("Academic", 17),
    ("Classic", 14),
    ("Literary Fiction", 15)
]

try:
    # Define the output file path
    output_file = os.path.join(os.getcwd(), "GenreTypes.csv")
    
    # Create CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write header row
        writer.writerow(['GenreID', 'GenreName', 'MinAge'])
        
        # Write data rows
        for i, (genre, min_age) in enumerate(genres_min_ages, 1):
            writer.writerow([i, genre, min_age])

    # Force flush stdout to ensure all output is displayed
    sys.stdout.flush()

except Exception as e:
    # Print error information if something goes wrong
    print(f"Error occurred: {e}")
    traceback.print_exc()

# Final flush to ensure everything is written
sys.stdout.flush()
