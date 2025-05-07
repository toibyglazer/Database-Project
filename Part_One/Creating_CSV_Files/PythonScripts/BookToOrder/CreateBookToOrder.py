import csv
import random
import os

# Settings
NUM_ORDERS = 800
NUM_BOOKS = 400
NUM_BOOK_TO_ORDER_RECORDS = 900
MIN_QUANTITY = 1
MAX_QUANTITY = 5

def generate_book_to_order():
    """Generate relationships between books and orders"""
    book_to_order_records = []
    
    # Track which combinations we've already created to avoid duplicates
    # (since OrderID, BookID is a primary key)
    combinations = set()
    
    # First, ensure each order has at least one book
    for order_id in range(1, NUM_ORDERS + 1):
        book_id = random.randint(1, NUM_BOOKS)
        
        # Make sure we don't create duplicate combinations
        while (order_id, book_id) in combinations:
            book_id = random.randint(1, NUM_BOOKS)
        
        quantity = random.randint(MIN_QUANTITY, MAX_QUANTITY)
        
        book_to_order_records.append({
            'OrderID': order_id,
            'BookID': book_id,
            'BookQuantity': quantity
        })
        
        combinations.add((order_id, book_id))
    
    # Then add additional records to reach NUM_BOOK_TO_ORDER_RECORDS
    additional_records = NUM_BOOK_TO_ORDER_RECORDS - NUM_ORDERS
    
    for _ in range(additional_records):
        order_id = random.randint(1, NUM_ORDERS)
        book_id = random.randint(1, NUM_BOOKS)
        
        # Make sure we don't create duplicate combinations
        while (order_id, book_id) in combinations:
            order_id = random.randint(1, NUM_ORDERS)
            book_id = random.randint(1, NUM_BOOKS)
        
        quantity = random.randint(MIN_QUANTITY, MAX_QUANTITY)
        
        book_to_order_records.append({
            'OrderID': order_id,
            'BookID': book_id,
            'BookQuantity': quantity
        })
        
        combinations.add((order_id, book_id))
    
    return book_to_order_records

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
        print("Generating BookToOrder data...")
        book_to_order_records = generate_book_to_order()
        
        # Save book to order relationships to CSV
        book_to_order_file = save_to_csv(book_to_order_records, 'BookToOrder.csv')
        
        print(f"\nData successfully saved to file: {book_to_order_file}")
        print(f"Generated {len(book_to_order_records)} BookToOrder records")
        
        # Count orders per book
        order_counts = {}
        for record in book_to_order_records:
            order_id = record['OrderID']
            order_counts[order_id] = order_counts.get(order_id, 0) + 1
        
        print(f"Orders with multiple books: {sum(1 for count in order_counts.values() if count > 1)}")
        print(f"Maximum books per order: {max(order_counts.values())}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()