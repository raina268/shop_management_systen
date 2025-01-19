#shop management system 

# SQL Queries to Create Database and Tables:
1. Create the Database:
```sql
CREATE DATABASE IF NOT EXISTS shop_management;
```
2. Create the products Table:
This table will store information about the products, including their name, price, and stock quantity.

```sql

USE shop_management;

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0
);
```
3. Create the sales Table:
This table will store information about sales transactions, including the product sold, the quantity, total amount, and sale date.

```sql

CREATE TABLE IF NOT EXISTS sales (
    sales_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sale_date DATETIME NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```
4. Sales report

The Sales Report feature in code is built on data stored in the sales table. The sales table already contains all the necessary information for generating a sales report, such as:

sales_id: Unique identifier for each sale.
product_id: Foreign key to the products table, which links the sale to a specific product.
quantity: The number of units sold.
total_amount: The total amount of the sale.
sale_date: The date and time the sale occurred.

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
