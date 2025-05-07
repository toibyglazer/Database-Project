import csv
import random
import os
import urllib.request
from datetime import datetime, timedelta
import calendar

# URLs of the CSV files
BOOK_TO_ORDER_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/BookToOrder-GSbZR40uhKdNR4YJlcoGwErduKj0TV.csv"
BOOK_LIST_URL = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/BookList-Y9XyEu7ykv1q4zRPMtU3Yr9bBM1ch7.csv"

# Settings
NUM_ORDERS = 800
NUM_CUSTOMERS = 400
MIN_LIBRARIAN_ID = 401
MAX_LIBRARIAN_ID = 800
START_DATE = datetime(2014, 1, 1)
END_DATE = datetime(2025, 5, 5)  # Current date mentioned by user

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

def generate_date_for_month(year, month):
    """Generate a random date within a specific year and month"""
    _, last_day = calendar.monthrange(year, month)
    day = random.randint(1, last_day)
    return datetime(year, month, day)

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

def generate_orders_by_month(final_prices):
    """Generate order data ensuring each month in the date range has orders"""
    orders = []
    
    # Calculate total number of months in the range
    start_year, start_month = START_DATE.year, START_DATE.month
    end_year, end_month = END_DATE.year, END_DATE.month
    
    # Create a list of all year-month combinations in the range
    all_months = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # Skip months before start_month in start_year
            if year == start_year and month < start_month:
                continue
            # Skip months after end_month in end_year
            if year == end_year and month > end_month:
                continue
            all_months.append((year, month))
    
    # Calculate minimum orders per month to ensure coverage
    min_orders_per_month = NUM_ORDERS // len(all_months)
    remaining_orders = NUM_ORDERS % len(all_months)
    
    print(f"Total months in range: {len(all_months)}")
    print(f"Minimum orders per month: {min_orders_per_month}")
    print(f"Remaining orders to distribute: {remaining_orders}")
    
    # Distribute orders across months
    order_id = 1
    for year, month in all_months:
        # Determine how many orders for this month
        orders_this_month = min_orders_per_month
        if remaining_orders > 0:
            orders_this_month += 1
            remaining_orders -= 1
        
        # Generate orders for this month
        for _ in range(orders_this_month):
            if order_id > NUM_ORDERS:
                break
                
            # Generate date within this month
            order_date = generate_date_for_month(year, month)
            
            # Assign to a random customer
            customer_id = random.randint(1, NUM_CUSTOMERS)
            
            # Always assign a librarian (no NULL values)
            librarian_id = random.randint(MIN_LIBRARIAN_ID, MAX_LIBRARIAN_ID)
            
            # Get final price for this order, or generate a random one if not calculated
            if str(order_id) in final_prices:
                final_price = final_prices[str(order_id)]
            else:
                final_price = round(random.uniform(30, 1300), 2)
            
            # Add the order
            orders.append({
                'OrderID': order_id,
                'OrderDate': order_date.strftime('%Y-%m-%d'),
                'FinalPrice': final_price,
                'CustomerID': customer_id,
                'LibrarianID': librarian_id
            })
            
            order_id += 1
    
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
        print("Starting Orders generation...")
        
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
        
        # Generate orders ensuring each month has orders
        print("Generating orders for each month in the date range...")
        orders = generate_orders_by_month(final_prices)
        
        # Save orders to CSV
        orders_file = save_to_csv(orders, 'Orders.csv')
        
        # Display 10 sample orders
        print("\n10 sample orders:")
        for order in orders[:10]:
            print(f"{order['OrderID']},{order['OrderDate']},{order['FinalPrice']},{order['CustomerID']},{order['LibrarianID']}")
        
        # Statistics
        print("\nStatistics:")
        print(f"Total number of orders: {len(orders)}")
        
        # Calculate price statistics
        prices = [float(order['FinalPrice']) for order in orders]
        print(f"Minimum order price: {min(prices):.2f}")
        print(f"Maximum order price: {max(prices):.2f}")
        print(f"Average order price: {sum(prices) / len(prices):.2f}")
        
        # Count orders by year and month
        orders_by_month = {}
        for order in orders:
            date = datetime.strptime(order['OrderDate'], '%Y-%m-%d')
            year_month = f"{date.year}-{date.month:02d}"
            if year_month in orders_by_month:
                orders_by_month[year_month] += 1
            else:
                orders_by_month[year_month] = 1
        
        print("\nOrders by month:")
        for year_month, count in sorted(orders_by_month.items()):
            print(f"{year_month}: {count} orders")
        
        print(f"\nData successfully saved to file: {orders_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()