import csv
import random
import os
import urllib.request
from datetime import datetime, timedelta

# URLs of the CSV files
BOOK_TO_ORDER_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/BookToOrder-GSbZR40uhKdNR4YJlcoGwErduKj0TV.csv"
BOOK_LIST_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/BookList-Y9XyEu7ykv1q4zRPMtU3Yr9bBM1ch7.csv"

# Settings
NUM_ORDERS = 800
NUM_CUSTOMERS = 400
MIN_LIBRARIAN_ID = 401
MAX_LIBRARIAN_ID = 800
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 4, 28)

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

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randint(0, days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def calculate_final_prices(book_to_order_data, book_list_data):
    """Calculate final prices for each order based on books and quantities"""
    # Convert book_list_data to a dictionary for faster lookups
    book_prices = {}
    for book in book_list_data:
        book_id = book['BookID']
        try:
            price = float(book['price'])
            book_prices[book_id] = price
        except (ValueError, KeyError):
            print(f"Warning: Invalid price for BookID {book_id}")
            book_prices[book_id] = 0.0
    
    # Calculate total price for each order
    order_prices = {}
    for record in book_to_order_data:
        try:
            order_id = record['OrderID']
            book_id = record['BookID']
            quantity = int(record['BookQuantity'])
            
            if book_id in book_prices:
                book_price = book_prices[book_id]
                item_price = book_price * quantity
                
                if order_id in order_prices:
                    order_prices[order_id] += item_price
                else:
                    order_prices[order_id] = item_price
            else:
                print(f"Warning: BookID {book_id} not found in book list")
        except (ValueError, KeyError) as e:
            print(f"Warning: Error processing record: {record}, Error: {str(e)}")
    
    # Apply random discount (0-10%) to each order
    final_prices = {}
    for order_id, total_price in order_prices.items():
        discount = random.uniform(0, 0.1)
        final_price = total_price * (1 - discount)
        final_prices[order_id] = round(final_price, 2)
    
    return final_prices

def generate_orders(final_prices):
    """Generate order data"""
    orders = []
    
    # Create orders
    for order_id in range(1, NUM_ORDERS + 1):
        # Generate random order date
        order_date = generate_random_date(START_DATE, END_DATE)
        
        # Assign to a random customer
        customer_id = random.randint(1, NUM_CUSTOMERS)
        
        # Assign to a random librarian (80% chance) or leave NULL (20% chance)
        librarian_id = random.randint(MIN_LIBRARIAN_ID, MAX_LIBRARIAN_ID) if random.random() < 0.8 else None
        
        # Get final price for this order, or generate a random one if not calculated
        if str(order_id) in final_prices:
            final_price = final_prices[str(order_id)]
        else:
            print(f"Warning: No price calculated for OrderID {order_id}, generating random price")
            final_price = round(random.uniform(50, 300), 2)
        
        # Add the order
        orders.append({
            'OrderID': order_id,
            'OrderDate': order_date.strftime('%Y-%m-%d'),
            'FinalPrice': final_price,
            'CustomerID': customer_id,
            'LibrarianID': librarian_id
        })
    
    return orders

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
        print("Starting Order_Table generation...")
        
        # Create temporary directory for downloaded files
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # Download CSV files
        book_to_order_file = os.path.join(temp_dir, 'BookToOrder.csv')
        book_list_file = os.path.join(temp_dir, 'BookList.csv')
        
        if not download_csv(BOOK_TO_ORDER_URL, book_to_order_file):
            print("Failed to download BookToOrder.csv")
            return
        
        if not download_csv(BOOK_LIST_URL, book_list_file):
            print("Failed to download BookList.csv")
            return
        
        # Load CSV data
        book_to_order_data = load_csv(book_to_order_file)
        if book_to_order_data is None:
            print("Failed to load BookToOrder data")
            return
        
        book_list_data = load_csv(book_list_file)
        if book_list_data is None:
            print("Failed to load BookList data")
            return
        
        print(f"Loaded {len(book_to_order_data)} BookToOrder records")
        print(f"Loaded {len(book_list_data)} BookList records")
        
        # Calculate final prices
        print("Calculating final prices...")
        final_prices = calculate_final_prices(book_to_order_data, book_list_data)
        print(f"Calculated prices for {len(final_prices)} orders")
        
        # Generate orders
        print("Generating orders...")
        orders = generate_orders(final_prices)
        
        # Save orders to CSV
        orders_file = save_to_csv(orders, 'Order_Table.csv')
        
        # Display 10 sample orders
        print("\n10 sample orders:")
        for order in orders[:10]:
            librarian_id = order['LibrarianID'] if order['LibrarianID'] is not None else 'NULL'
            print(f"{order['OrderID']},{order['OrderDate']},{order['FinalPrice']},{order['CustomerID']},{librarian_id}")
        
        # Statistics
        print("\nStatistics:")
        print(f"Total number of orders: {len(orders)}")
        
        # Calculate price statistics
        prices = [float(order['FinalPrice']) for order in orders]
        print(f"Minimum order price: {min(prices):.2f}")
        print(f"Maximum order price: {max(prices):.2f}")
        print(f"Average order price: {sum(prices) / len(prices):.2f}")
        
        print(f"\nData successfully saved to file: {orders_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()