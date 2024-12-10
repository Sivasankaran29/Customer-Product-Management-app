import pymysql

def get_db_connection():
    """Establish and return a database connection."""
    return pymysql.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="root",  # Replace with your MySQL password
        database="crpm_system",
        cursorclass=pymysql.cursors.DictCursor
    )

class Customer:
    def __init__(self, db_connection):
        self.conn = db_connection

    def add_customer(self, name, email, phone, address):
        query = "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (name, email, phone, address))
            self.conn.commit()

    def get_all_customers(self):
        query = "SELECT * FROM customers"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def update_customer(self, customer_id, name, email, phone, address):
        query = """
        UPDATE customers
        SET name = %s, email = %s, phone = %s, address = %s
        WHERE customer_id = %s
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (name, email, phone, address, customer_id))
            self.conn.commit()

    def delete_customer(self, customer_id):
        query = "DELETE FROM customers WHERE customer_id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            self.conn.commit()

class Product:
    def __init__(self, db_connection):
        self.conn = db_connection

    def add_product(self, name, category, price, stock):
        query = "INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (name, category, price, stock))
            self.conn.commit()

    def get_all_products(self):
        query = "SELECT * FROM products"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def update_product(self, product_id, name, category, price, stock):
        query = """
        UPDATE products
        SET name = %s, category = %s, price = %s, stock = %s
        WHERE product_id = %s
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (name, category, price, stock, product_id))
            self.conn.commit()

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE product_id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (product_id,))
            self.conn.commit()

class Sale:
    def __init__(self, db_connection):
        self.conn = db_connection

    def record_sale(self, customer_id, product_id, quantity):
        query = """
        INSERT INTO sales (customer_id, product_id, quantity, total_amount)
        SELECT %s, %s, %s, products.price * %s FROM products WHERE product_id = %s
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (customer_id, product_id, quantity, quantity, product_id))
            self.conn.commit()

    def get_all_sales(self):
        query = "SELECT * FROM sales"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
