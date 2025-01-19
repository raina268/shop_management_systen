import mysql.connector
from datetime import datetime

# Database connection with context manager
def connect_db():
    """
    Connects to the MySQL database and returns the connection object.
    """
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Update your MySQL username if needed
        password='python3',  # Update your MySQL password if needed
        database='shop_management'  # Your database name
    )

def print_receipt(cart, payment_mode):
    """
    Prints a formatted receipt for the items in the cart and the payment mode.

    Parameters:
    - cart: A list of tuples, where each tuple contains a product and its quantity.
    - payment_mode: The payment method used for the purchase (Cash/Card).
    """
    print("\n--------------------------------------------------")
    print("                     Receipt")
    print("--------------------------------------------------")
    print("Date:                " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("--------------------------------------------------")
    print("Product Name          Quantity    Price (₹)    Total (₹)")
    print("--------------------------------------------------")
    
    total_amount = 0
    for item in cart:
        product, quantity = item
        total_cost = product[2] * quantity
        total_amount += total_cost
        print(f" {product[1]:<20} {quantity:<12} ₹{product[2]:<8} ₹{total_cost:<8}")
    
    print("--------------------------------------------------")
    print(f"Total Amount:                                ₹{total_amount}")
    print(f"Payment Mode:                                {payment_mode}")
    print("--------------------------------------------------")
    print("           Thank you for your purchase!")
    print("--------------------------------------------------")


# Handle adding a product to the inventory
def add_product(name, price, stock):
    """
    Adds a new product to the inventory.

    Parameters:
    - name: The name of the product.
    - price: The price of the product.
    - stock: The initial stock quantity of the product.
    """
    try:
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", (name, price, stock))
            db.commit()
        print("\nProduct '" + name + "' added successfully!\n")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Handle selling products (making a sale)
def sell_to_customer(cart, payment_mode):
    """
    Processes a sale and updates the stock in the inventory.

    Parameters:
    - cart: A list of tuples where each tuple contains a product and its quantity.
    - payment_mode: The payment method used for the purchase (Cash/Card).
    """
    try:
        with connect_db() as db:
            cursor = db.cursor()
    
            # Process the sale and update stock
            total_amount = 0
            for item in cart:
                product, quantity = item
                total_cost = product[2] * quantity
                total_amount += total_cost
                new_stock = product[3] - quantity
                cursor.execute("UPDATE products SET stock = %s WHERE product_id = %s", (new_stock, product[0]))
                
                # Record the sale
                sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO sales (product_id, quantity, total_amount, sale_date, payment_mode) VALUES (%s, %s, %s, %s, %s)",
                            (product[0], quantity, total_cost, sale_date, payment_mode))

            db.commit()
        
        # Print receipt
        print_receipt(cart, payment_mode)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Generate a bill manually (no cart, user inputs products directly)
def generate_bill_manually():
    """
    Allows the user to generate a bill manually by entering product details.
    """
    cart = []
    while True:
        product_id = int(input("\nEnter product ID (0 to stop): "))
        if product_id == 0:
            break
        
        quantity = int(input("Enter quantity to sell: "))
        
        try:
            with connect_db() as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
                product = cursor.fetchone()
            if product:
                cart.append((product, quantity))
            else:
                print("\nError: Product not found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    if not cart:
        print("\nNo products selected for purchase.")
        return

    # Ask for payment mode and generate the bill
    payment_mode = input("Enter payment mode (Cash/Card): ").capitalize()
    sell_to_customer(cart, payment_mode)

# View inventory (list all products and their stock)
def view_inventory():
    """
    Displays all the products in the inventory, along with their stock levels.
    """
    try:
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT product_id, name, price, stock FROM products")
            products = cursor.fetchall()

            print("\n--- Inventory ---")
            if products:
                for product in products:
                    print("ID: " + str(product[0]) + " | Name: " + product[1] + " | Price: ₹" + str(product[2]) + " | Stock: " + str(product[3]))
            else:
                print("No products in inventory.")
            print("----------------")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def sales_report():
    """
    Displays a report of all sales transactions.
    """
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT sales_id, product_id, quantity, total_amount, sale_date, payment_mode FROM sales")
    sales = cursor.fetchall()
    
    print("\n--- Sales Report ---")
    if sales:
        for sale in sales:
            cursor.execute("SELECT name FROM products WHERE product_id = %s", (sale[1],))
            product_name = cursor.fetchone()[0]
            payment_mode = sale[5] if sale[5] else "Not Available"  # Handle None
            print(f"Sale ID: {sale[0]} | Product: {product_name} | Quantity: {sale[2]} | Total: ₹{sale[3]} | Date: {sale[4]} | Payment Mode: {payment_mode}")
    else:
        print("No sales recorded.")
    print("----------------")
    
# Function to search a product by name
def search_product_by_name(name):
    """
    Searches for a product in the inventory by its name.

    Parameters:
    - name: The name (or partial name) of the product to search for.
    """
    try:
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + name + '%',))
            products = cursor.fetchall()

            print("\n--- Product Search Result ---")
            if products:
                for product in products:
                    print("ID: " + str(product[0]) + " | Name: " + product[1] + " | Price: ₹" + str(product[2]) + " | Stock: " + str(product[3]))
            else:
                print("No product found with that name.")
            print("----------------")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Restock a product
def restock_product(product_id, quantity):
    """
    Restocks a product by increasing its stock.

    Parameters:
    - product_id: The ID of the product to restock.
    - quantity: The number of items to add to the stock.
    """
    try:
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()

            if product:
                new_stock = product[3] + quantity
                cursor.execute("UPDATE products SET stock = %s WHERE product_id = %s", (new_stock, product_id))
                db.commit()
                print(f"\nProduct '{product[1]}' restocked successfully! New stock: {new_stock}")
            else:
                print("\nError: Product not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Remove a product from inventory
def remove_product(product_id):
    """
    Removes a product from the inventory.

    Parameters:
    - product_id: The ID of the product to be removed.
    """
    try:
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()

            if product:
                cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                db.commit()
                print(f"\nProduct '{product[1]}' removed successfully!")
            else:
                print("\nError: Product not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Regenerate a bill by sales ID
def regenerate_bill():
    """
    Regenerates a bill for a specific sale transaction using the sales ID.
    """
    sales_id = int(input("\nEnter sales ID to regenerate bill: "))

    try:
        # Connect to the database
        db = connect_db()
        cursor = db.cursor()

        # Get sales details using sales_id, including the payment_mode
        cursor.execute("SELECT sales_id, product_id, quantity, total_amount, sale_date, payment_mode FROM sales WHERE sales_id = %s", (sales_id,))
        sale = cursor.fetchone()

        if sale:
            # Get product details
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (sale[1],))
            product = cursor.fetchone()

            # Display regenerated receipt
            print("\n--------------------------------------------------")
            print("                     Regenerated Receipt")
            print("--------------------------------------------------")
            print("Date:                ", sale[4])
            print("--------------------------------------------------")
            print("Product Name           Quantity   Price (₹)    Total (₹)")
            print("--------------------------------------------------")
            print(f"{product[1]}                {sale[2]}        ₹{product[2]:.2f}    ₹{sale[3]:.2f}")
            print("--------------------------------------------------")
            print(f"Total Amount:                            ₹{sale[3]:.2f}")
            print(f"Payment Mode:                            {sale[5]}")
            print("--------------------------------------------------")
            print("           Thank you for your purchase!")
            print("--------------------------------------------------")
        else:
            print("\nError: Sale not found for the given sales ID.")
        
        cursor.close()
        db.close()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def product_management():
    """
    Handles the product management section, allowing the user to add, search, view, restock, or remove products.
    """
    while True:
        print("\n--- Product Management ---")
        print("1. Add Product")
        print("2. Search Product")
        print("3. View Inventory")
        print("4. Restock Product")
        print("5. Remove Product")
        print("6. Back to Main Menu")
        
        sub_choice = input("\nEnter your choice (1-6): ")
        
        if sub_choice == '1':
            name = input("\nEnter product name: ")
            price = float(input("Enter product price: ₹"))
            stock = int(input("Enter initial stock: "))
            add_product(name, price, stock)
        elif sub_choice == '2':
            name = input("\nEnter product name to search: ")
            search_product_by_name(name)
        elif sub_choice == '3':
            view_inventory()
        elif sub_choice == '4':
            product_id = int(input("\nEnter product ID to restock: "))
            quantity = int(input("Enter quantity to restock: "))
            restock_product(product_id, quantity)
        elif sub_choice == '5':
            product_id = int(input("\nEnter product ID to remove: "))
            remove_product(product_id)
        elif sub_choice == '6':
            break
        else:
            print("\nInvalid choice. Please try again.")

# Purchase Section
def purchase_section():
    """
    Handles the purchase flow: adding products to the cart, finalizing the bill, and generating the receipt.
    """
    cart = []
    while True:
        print("\n--- Purchase Section ---")
        print("1. Add Product to Cart")
        print("2. Finalize Bill and Generate Receipt")
        print("3. Generate Bill Manually")
        print("4. Regenerate Bill")
        print("5. Back to Main Menu")
        
        sub_choice = input("\nEnter your choice (1-4): ")
        
        if sub_choice == '1':
            product_id = int(input("\nEnter product ID: "))
            quantity = int(input("Enter quantity to sell: "))
            
            try:
                with connect_db() as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
                    product = cursor.fetchone()
                if product:
                    cart.append((product, quantity))
                else:
                    print("\nError: Product not found.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            
        elif sub_choice == '2':
            if not cart:
                print("\nCart is empty. Cannot finalize bill.")
            else:
                payment_mode = input("Enter payment mode (Cash/Card): ").capitalize()
                sell_to_customer(cart, payment_mode)
                break
        elif sub_choice == '3':
            generate_bill_manually()  # Allow manual bill generation
            break
        elif sub_choice == '4':
            regenerate_bill()  # Allow regeneration of the bill by sales ID
        elif sub_choice == '5':
            break
        else:
            print("\nInvalid choice. Please try again.")


# Main Menu
def main_menu():
    """
    The main menu of the system, where the user can choose between different functionalities.
    """
    while True:
        print("\n--- Main Menu ---")
        print("1. Product Management")
        print("2. Purchase")
        print("3. Sales Report")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            product_management()
        elif choice == '2':
            purchase_section()
        elif choice == '3':
            sales_report()
        elif choice == '4':
            print("\nExiting... Thank you for using the system!")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
