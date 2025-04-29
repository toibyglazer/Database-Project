import csv
import random
from datetime import datetime, timedelta
import os
import requests
from io import StringIO

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL of the existing Person data
PERSON_DATA_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/PersonMock_data-BzmxpvC9JrPEKIMSw8R7hTC7W2XT9s.csv"

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define output directory path
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created output directory at: {OUTPUT_DIR}")
else:
    print(f"Output directory already exists at: {OUTPUT_DIR}")

# Function to fetch and parse the existing Person data
def fetch_person_data():
    response = requests.get(PERSON_DATA_URL, verify=False)  # Changed to verify=False to bypass SSL verification
    if response.status_code == 200:
        # Parse CSV data
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        persons = list(reader)
        print(f"Successfully fetched {len(persons)} person records")
        return persons
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

# Function to calculate age from birth date
def calculate_age(birth_date):
    try:
        # Handle different date formats
        if '-' in birth_date:
            parts = birth_date.split('-')
            if len(parts[2]) == 4:  # Format: DD-MM-YYYY
                birth_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
            else:  # Format: YYYY-MM-DD
                birth_date = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        elif '/' in birth_date:
            parts = birth_date.split('/')
            birth_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
        else:
            # Try other formats if needed
            birth_date = datetime.strptime(birth_date, "%d/%m/%Y")
            
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except Exception as e:
        print(f"Error calculating age for {birth_date}: {e}")
        # Default to a reasonable age if calculation fails
        return random.randint(20, 60)

# Generate Librarian data
def generate_librarian_data(persons, num_librarians=400):
    librarians = []
    
    # Filter persons to only include IDs 401-800
    filtered_persons = [p for p in persons if 401 <= int(p['ID']) <= 800]
    
    # If we don't have enough persons after filtering, print a warning
    if len(filtered_persons) < num_librarians:
        print(f"Warning: Only found {len(filtered_persons)} persons with IDs 401-800. Some librarians may be missing.")
    
    # Generate librarian data for each filtered person
    for person in filtered_persons:
        try:
            # Calculate age
            age = calculate_age(person['BirthDate'])
            
            # Parse birth date
            birth_date = None
            if '-' in person['BirthDate']:
                parts = person['BirthDate'].split('-')
                if len(parts[2]) == 4:  # Format: DD-MM-YYYY
                    birth_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
                else:  # Format: YYYY-MM-DD
                    birth_date = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
            elif '/' in person['BirthDate']:
                parts = person['BirthDate'].split('/')
                birth_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
            else:
                # Try other formats if needed
                birth_date = datetime.strptime(person['BirthDate'], "%d/%m/%Y")
            
            # Calculate minimum work start date (person must be at least 18 years old)
            min_start_date = birth_date + timedelta(days=365.25 * 18)
            
            # Ensure min_start_date is not in the future
            if min_start_date > datetime.now():
                # If person is too young, use a reasonable default
                start_work_date = datetime.now() - timedelta(days=365 * random.randint(1, 5))
            else:
                # Generate a random start date between min_start_date and now
                days_since_min = (datetime.now() - min_start_date).days
                if days_since_min <= 0:
                    # If person is too young, use a reasonable default
                    start_work_date = datetime.now() - timedelta(days=365 * random.randint(1, 5))
                else:
                    random_days = random.randint(0, days_since_min)
                    start_work_date = min_start_date + timedelta(days=random_days)
            
            # Format the date as YYYY-MM-DD for PostgreSQL
            start_work_date_str = start_work_date.strftime("%Y-%m-%d")
            
            # Calculate years of experience (could be more than years worked at this library)
            years_worked = (datetime.now() - start_work_date).days / 365.25
            experience_years = round(random.uniform(years_worked, years_worked + 5))
            
            # Calculate salary based on experience (base 8000 + 500 per year of experience)
            salary = 8000 + (experience_years * 500) + random.randint(-500, 500)
            
            librarians.append({
                'LibrarianID': person['ID'],
                'StartWorkDate': start_work_date_str,  # Now in YYYY-MM-DD format
                'ExperienceYears': experience_years,
                'age': age,
                'Salary': round(salary, 2)
            })
        except Exception as e:
            print(f"Error processing librarian for person {person['ID']}: {e}")
    
    return librarians

# Write data to CSV file
def write_to_csv(data, filename, fieldnames):
    output_file = os.path.join(OUTPUT_DIR, filename)
    
    # מחיקת הקובץ הקודם אם הוא קיים
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"Deleted previous file: {output_file}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"File created at: {output_file}")

# Main function to generate librarian data
def generate_all_librarian_data():
    # Fetch existing Person data
    persons = fetch_person_data()
    
    if not persons:
        print("Failed to fetch Person data. Exiting.")
        return
    
    # Generate librarian data
    librarians = generate_librarian_data(persons, 400)
    
    # Write data to CSV file
    write_to_csv(librarians, 'Librarian.csv', ['LibrarianID', 'StartWorkDate', 'ExperienceYears', 'age', 'Salary'])
    
    print("Librarian data generation complete.")
    print(f"Total Librarian records: {len(librarians)}")
    
    # Print sample data for verification
    print("\nSample Librarian data:")
    for librarian in librarians[:5]:
        print(librarian)
    
    # Print confirmation of date format
    print("\nDate format verification:")
    for librarian in librarians[:5]:
        print(f"StartWorkDate: {librarian['StartWorkDate']} (Format: YYYY-MM-DD)")
    
    # בדיקה שהקובץ אכן נוצר
    output_file = os.path.join(OUTPUT_DIR, 'Librarian.csv')
    if os.path.exists(output_file):
        print(f"\nSUCCESS: File exists at: {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
    else:
        print(f"\nERROR: File was not created at: {output_file}")

# Run the data generation
if __name__ == "__main__":
    generate_all_librarian_data()