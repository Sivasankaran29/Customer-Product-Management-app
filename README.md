# Customer & Product Management Application

A Streamlit-based application for managing customers, products, and sales in a database. This app provides a user-friendly interface to add, edit, delete, and view customers, products, and sales data, as well as visualize business insights.

---

## **Features**

- **Customer Management**: Add, view, edit, and delete customers.
- **Product Management**: Add, view, edit, and delete products.
- **Sales Management**: Record and view sales.
- **Business Insights**:
  - Total sales overview.
  - Visualization of customer purchase frequency.
  - Analysis of top-selling products.

---

## **Setup and Installation**

### Prerequisites

- Python 3.8 or higher
- Streamlit
- SQLite (or other compatible database)
- Required Python libraries (listed in `requirements.txt`)

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/customer-product-management.git
   cd customer-product-management
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Configure the database connection:

The app uses a database connection from backend.py. Ensure the database exists and is properly set up.
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open your browser at http://localhost:8501 to view the app.

Usage
Navigation
Use the sidebar to navigate between the following pages:

Customers: Manage customer records.
Products: Manage product records.
Sales: Record and view sales transactions.
Summary: View business insights through charts and visualizations.
Customer Management
Add a customer using the form provided under the "Add Customer" section.
View all customers in a table.
Edit or delete a customer using their unique ID.
Product Management
Add a new product, specifying name, category, price, and stock.
View all products in a table.
Edit or delete a product using its unique ID.
Sales Management
Record a sale by selecting customer ID, product ID, and quantity sold.
View all sales transactions in a table.
Summary and Insights
Total sales overview.
Visualizations of:
Sales by product.
Customer purchase frequency.
Top-selling products.
Folder Structure
bash
Copy code
customer-product-management/
│
├── app.py                  # Main Streamlit app file
├── backend.py              # Contains database connection and management classes
├── requirements.txt        # Required Python libraries
└── README.md               # Documentation
Contributing
Feel free to fork this repository, make changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
