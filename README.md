#shop management system 

# SQL Queries to Create Database and Tables:
1. Create the Database:
```sql
CREATE DATABASE IF NOT EXISTS shop_management;
USE shop_management;
```
2. Create the products Table:
This table will store information about the products, including their name, price, and stock quantity.

```sql

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT UNSIGNED NOT NULL
);

```
- product_id is an auto-incremented primary key.
- name stores the product name.
- price stores the price of the product (decimal type to handle currency values).
- stock represents the number of items in stock.


3. Create the sales Table:
This table will store information about sales transactions, including the product sold, the quantity, total amount, and sale date.

```sql

CREATE TABLE IF NOT EXISTS sales (
    sales_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sale_date DATETIME NOT NULL,
    payment_mode ENUM('Cash', 'Card') NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
```

- sales_id is an auto-incremented primary key.
- product_id is a foreign key that references the products table.
- quantity stores the number of units sold.
- total_amount stores the total cost of the transaction.
- sale_date stores the timestamp of the sale.
- payment_mode stores the payment method (Cash or Card), enforced with an ENUM type.


5. Sales report

The Sales Report feature in code is built on data stored in the sales table. The sales table already contains all the necessary information for generating a sales report, such as:

sales_id: Unique identifier for each sale.
product_id: Foreign key to the products table, which links the sale to a specific product.
quantity: The number of units sold.
total_amount: The total amount of the sale.
sale_date: The date and time the sale occurred.

Final SQL Script
sql
Copy
-- Create Database
CREATE DATABASE IF NOT EXISTS shop_management;
USE shop_management;

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- Create Sales Table
CREATE TABLE IF NOT EXISTS sales (
    sales_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sale_date DATETIME NOT NULL,
    payment_mode ENUM('Cash', 'Card') NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
Explanation:
Database Creation:
The shop_management database is created if it doesn't exist already.
products Table:
Stores product-related data, such as product ID, name, price, and stock.
sales Table:
Stores sales transactions, including the sale date, quantity sold, total amount, and payment mode. This table also has a foreign key relationship with the products table, ensuring that sales are associated with valid products


# Summary of the Table Structure:
products Table:

product_id: A unique ID for each product (auto-incremented).
name: Name of the product.
price: Price of the product.
stock: The quantity of the product available in inventory.
sales Table:

sales_id: A unique ID for each sale (auto-incremented).
product_id: Foreign key to the products table (the product being sold).
quantity: The quantity of the product sold.
total_amount: The total cost for the sale.
sale_date: The date and time the sale occurred.
