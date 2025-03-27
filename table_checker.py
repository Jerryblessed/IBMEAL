import sqlite3
from datetime import datetime, timedelta
import time

# Database path
db_path = 'database.sqlite'

# Time tracking dictionary to store prefix addition timestamps for each product ID
prefix_timestamp = {}

def monitor_and_prefix_notes():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path, timeout=10)  # Set a timeout to prevent locking issues
        cursor = conn.cursor()
        
        # Query to find notes with at least five entries and no delivery_date
        query = """
        SELECT notes
        FROM orders
        WHERE delivery_date IS NULL
        GROUP BY notes
        HAVING COUNT(*) >= 5
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()

        # Prepare a list of products to update
        products_to_update = []

        for row in rows:
            note = row[0]
            keyword = note.strip()  # Use the note as the keyword
            
            # Find corresponding products in 'products' table based on the description
            cursor.execute("SELECT id, name FROM products WHERE description = ?", (keyword,))
            product = cursor.fetchone()
            
            if product:
                product_id, original_name = product
                prefixed_name = f"ibtros{original_name}"

                # Check if 'ibtros' prefix is already present
                if not original_name.startswith("ibtros"):
                    products_to_update.append((prefixed_name, product_id, original_name))  # Track original name for reversion

        # Batch update all products in one go
        cursor.executemany("UPDATE products SET name = ? WHERE id = ?", [(name, product_id) for name, product_id, _ in products_to_update])
        conn.commit()
        
        # Log the update time for each product
        current_time = datetime.now()
        for _, product_id, original_name in products_to_update:
            prefix_timestamp[product_id] = (current_time, original_name)

        print(f"Updated {len(products_to_update)} products with the 'ibtros' prefix.")

        conn.close()

    except sqlite3.Error as e:
        print("Database error:", e)
    except Exception as e:
        print("Error:", e)

def get_credit_from_db(self):
    """Fetch the latest credit balance for the user from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT credit FROM users WHERE user_id = ?", (self.user.user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else self.user.credit


def revert_prefixed_names():
    # Check if 30 minutes have passed for each product that has the 'ibtros' prefix
    current_time = datetime.now()

    conn = sqlite3.connect(db_path, timeout=10)  # Re-open database connection for reverting
    cursor = conn.cursor()

    products_to_revert = []
    for product_id, (update_time, original_name) in list(prefix_timestamp.items()):
        # If 30 minutes have passed, revert the name
        if current_time >= update_time + timedelta(minutes=0.2):
            products_to_revert.append((original_name, product_id))
            del prefix_timestamp[product_id]  # Remove from timestamp tracking

    # Revert all product names due for reversion in one batch
    if products_to_revert:
        cursor.executemany("UPDATE products SET name = ? WHERE id = ?", products_to_revert)
        conn.commit()
        print(f"Reverted {len(products_to_revert)} products back to their original names.")

    conn.close()

# Continuously monitor the database and periodically check for reversion every 30 seconds
while True:
    monitor_and_prefix_notes()
    time.sleep(0.2)  # Wait before checking for the 30-minute reversion

    # Revert product names that have passed the 30-minute mark
    revert_prefixed_names()
    print("Monitoring and reverting...")
    time.sleep(2)  # Repeat every 30 seconds


# import sqlite3
# import time
# from datetime import datetime, timedelta

# # Database path
# db_path = 'database.sqlite'

# def monitor_and_prefix_notes():
#     try:
#         # Connect to the SQLite database
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()
        
#         # Query to find notes with five consecutive or total five entries and no delivery_date
#         query = """
#         SELECT notes
#         FROM orders
#         WHERE delivery_date IS NULL
#         GROUP BY notes
#         HAVING COUNT(*) >= 5
#         """
        
#         cursor.execute(query)
#         rows = cursor.fetchall()
        
#         # Process each found note pattern
#         for row in rows:
#             note = row[0]
#             keyword = note.strip()  # Use the note as the keyword
            
#             # Find the corresponding product with the description matching the keyword
#             cursor.execute("SELECT id, name FROM products WHERE description = ?", (keyword,))
#             product = cursor.fetchone()
            
#             if product:
#                 product_id, original_name = product
#                 prefixed_name = f"ibtros{original_name}"
                
#                 # Check if the product name already has the 'ibtros' prefix
#                 if not original_name.startswith("ibtros"):
#                     # Temporarily update the name with the prefix
#                     cursor.execute("UPDATE products SET name = ? WHERE id = ?", (prefixed_name, product_id))
#                     conn.commit()
#                     print(f"Product with description '{keyword}' updated to '{prefixed_name}'.")

#                     # Schedule reversion of the name after 30 minutes
#                     time.sleep(10)  # 1800 seconds = 30 minutes
                    
#                     # Revert the name back to the original
#                     cursor.execute("UPDATE products SET name = ? WHERE id = ?", (original_name, product_id))
#                     conn.commit()
#                     print(f"Product with description '{keyword}' name reverted to '{original_name}'.")

#             else:
#                 print(f"No product found with description '{keyword}'.")

#         conn.close()
#     except Exception as e:
#         print("Error:", e)

# # Continuously monitor the database every 30 seconds
# while True:
#     monitor_and_prefix_notes()
#     print("Monitoring...")
#     time.sleep(5)


# import sqlite3
# import time
# from datetime import datetime, timedelta

# # Database path
# db_path = 'database.sqlite'

# def monitor_and_prefix_notes():
#     try:
#         # Connect to the SQLite database
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()
        
#         # Query to find five consecutive orders with identical notes and no delivery_date
#         query = """
#         SELECT notes, COUNT(*)
#         FROM orders
#         WHERE delivery_date IS NULL
#         GROUP BY notes
#         HAVING COUNT(*) >= 5
#         """
        
#         cursor.execute(query)
#         rows = cursor.fetchall()
        
#         # Process each found note pattern
#         for row in rows:
#             note, count = row
#             keyword = note.strip()  # Extract the note as the keyword
            
#             # Find the corresponding product with the description matching the keyword
#             cursor.execute("SELECT id, name FROM products WHERE description = ?", (keyword,))
#             product = cursor.fetchone()
            
#             if product:
#                 product_id, original_name = product
#                 prefixed_name = f"ibtros{original_name}"
                
#                 # Temporarily update the name with the prefix
#                 cursor.execute("UPDATE products SET name = ? WHERE id = ?", (prefixed_name, product_id))
#                 conn.commit()
#                 print(f"Product with description '{keyword}' updated to '{prefixed_name}'.")

#                 # Wait for 30 minutes before reverting the change
#                 time.sleep(10)  # 1800 seconds = 30 minutes
                
#                 # Revert the name back to the original
#                 cursor.execute("UPDATE products SET name = ? WHERE id = ?", (original_name, product_id))
#                 conn.commit()
#                 print(f"Product with description '{keyword}' name reverted to '{original_name}'.")
#             else:
#                 print(f"No product found with description '{keyword}'.")

#         conn.close()
#     except Exception as e:
#         print("Error:", e)

# # Continuously monitor the database every 30 seconds
# while True:
#     monitor_and_prefix_notes()
#     print("Monitoring...")
#     time.sleep(30)
