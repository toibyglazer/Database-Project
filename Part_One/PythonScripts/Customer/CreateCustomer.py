import csv
import random
from datetime import datetime
import os
import requests
from io import StringIO

# URL of the existing Person data
PERSON_DATA_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/PersonMock_data-BzmxpvC9JrPEKIMSw8R7hTC7W2XT9s.csv"

# Create output directory if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

import certifi

# Function to fetch and parse the existing Person data
def fetch_person_data():
    response = requests.get(PERSON_DATA_URL, verify=False)
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
# Function to get birth year from birth date
def get_birth_year(birth_date):
    try:
        # Handle different date formats
        if '-' in birth_date:
            parts = birth_date.split('-')
            if len(parts[2]) == 4:  # Format: DD-MM-YYYY
                return int(parts[2])
            else:  # Format: YYYY-MM-DD
                return int(parts[0])
        else:
            # Try other formats if needed
            birth_date = datetime.strptime(birth_date, "%d/%m/%Y")
            return birth_date.year
    except Exception as e:
        print(f"Error getting birth year for {birth_date}: {e}")
        # Default to a reasonable birth year if extraction fails
        return 1990


# Generate Customer data
def generate_customer_data(persons, num_customers=400):
    # Filter persons to only include IDs 1-400
    filtered_persons = [p for p in persons if 1 <= int(p['ID']) <= 400]
    
    # If we don't have enough persons after filtering, print a warning
    if len(filtered_persons) < num_customers:
        print(f"Warning: Only found {len(filtered_persons)} persons with IDs 1-400. Some customers may be missing.")
    
    customers = []
    
    # Generate customer data for each filtered person
    for i, person in enumerate(filtered_persons, 1):
        # 80% chance of being a member
        is_member = random.random() < 0.8
        
        if is_member:
            # Get birth year
            birth_year = get_birth_year(person['BirthDate'])
            
            # Start year must be after birth year + 18 (assuming membership starts at adult age)
            min_start_year = birth_year + 18
            max_start_year = 2024  # Current year
            
            if min_start_year > max_start_year:
                # Person is too young to be a member
                id_member = None
                discount = 0.00
                start_year = None
            else:
                id_member = 100 + i
                discount = random.choice([5.00, 10.00, 15.00, 20.00])
                start_year = random.randint(min_start_year, max_start_year)
        else:
            id_member = None
            discount = 0.00
            start_year = None
        
        customers.append({
            'CustomerID': person['ID'],
            'IDmember': id_member,
            'Discount': discount,
            'StartYearMember': start_year
        })
    
    return customers

# Write data to CSV file
def write_to_csv(data, filename, fieldnames):
    with open(f'output/{filename}', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Main function to generate customer data
def generate_all_customer_data():
    # Fetch existing Person data
    persons = fetch_person_data()
    
    if not persons:
        print("Failed to fetch Person data. Exiting.")
        return
    
    # Generate customer data
    customers = generate_customer_data(persons, 400)
    
    # Write data to CSV file
    write_to_csv(customers, 'Customer.csv', ['CustomerID', 'IDmember', 'Discount', 'StartYearMember'])
    
    print("Customer data generation complete. File saved in the 'output' directory.")
    print(f"Total Customer records: {len(customers)}")
    
    # Print sample data for verification
    print("\nSample Customer data:")
    for customer in customers[:5]:
        print(customer)

# Run the data generation
if __name__ == "__main__":
    generate_all_customer_data()