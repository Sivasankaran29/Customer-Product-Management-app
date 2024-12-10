import streamlit as st
import pandas as pd
from backend import get_db_connection, Customer, Product, Sale
import matplotlib.pyplot as plt

# Initialize DB connection
conn = get_db_connection()

# Create objects for managing customers, products, and sales
customer_manager = Customer(conn)
product_manager = Product(conn)
sale_manager = Sale(conn)

# Streamlit page configuration
st.set_page_config(page_title="Customer & Product Management", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Customers", "Products", "Sales", "Summary"])

# **Customers Management**
if page == "Customers":
    st.title("Customer Management")
    
    # Add Customer Section
    with st.expander("Add Customer"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        address = st.text_area("Address")
        if st.button("Add Customer"):
            customer_manager.add_customer(name, email, phone, address)
            st.success("Customer added successfully!")

    # View All Customers Section
    st.subheader("All Customers")
    customers = customer_manager.get_all_customers()
    customer_df = pd.DataFrame(customers)
    st.write(customer_df)
    
    # Edit/Delete Customer Section
    with st.expander("Edit/Delete Customer"):
        customer_id = st.number_input("Customer ID", min_value=1)
        customer = next((x for x in customers if x['customer_id'] == customer_id), None)
        if customer:
            new_name = st.text_input("New Name", value=customer['name'])
            new_email = st.text_input("New Email", value=customer['email'])
            new_phone = st.text_input("New Phone", value=customer['phone'])
            new_address = st.text_area("New Address", value=customer['address'])
            if st.button("Update Customer"):
                customer_manager.update_customer(customer_id, new_name, new_email, new_phone, new_address)
                st.success("Customer updated successfully!")
            if st.button("Delete Customer"):
                customer_manager.delete_customer(customer_id)
                st.success("Customer deleted successfully!")
        else:
            st.error("Customer not found.")

# **Products Management**
elif page == "Products":
    st.title("Product Management")

    # Add Product Section
    with st.expander("Add Product"):
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock", min_value=0)
        if st.button("Add Product"):
            product_manager.add_product(name, category, price, stock)
            st.success("Product added successfully!")

    # View All Products Section
    st.subheader("All Products")
    products = product_manager.get_all_products()
    product_df = pd.DataFrame(products)
    st.write(product_df)

    # Edit/Delete Product Section
    with st.expander("Edit/Delete Product"):
        product_id = st.number_input("Product ID", min_value=1)
        product = next((x for x in products if x['product_id'] == product_id), None)
        if product:
            new_name = st.text_input("New Name", value=product['name'])
            new_category = st.text_input("New Category", value=product['category'])
        
            # Convert Decimal price to float for st.number_input
            new_price = st.number_input("New Price", value=float(product['price']), format="%.2f")
        
            new_stock = st.number_input("New Stock", value=product['stock'])
        
            if st.button("Update Product"):
                product_manager.update_product(product_id, new_name, new_category, new_price, new_stock)
                st.success("Product updated successfully!")
            if st.button("Delete Product"):
                product_manager.delete_product(product_id)
                st.success("Product deleted successfully!")
        else:
            st.error("Product not found.")

# **Sales Management**
elif page == "Sales":
    st.title("Sales Management")

    # Record Sale Section
    with st.expander("Record Sale"):
        customer_id = st.number_input("Customer ID", min_value=1)
        product_id = st.number_input("Product ID", min_value=1)
        quantity = st.number_input("Quantity", min_value=1)
        if st.button("Record Sale"):
            sale_manager.record_sale(customer_id, product_id, quantity)
            st.success("Sale recorded successfully!")

    # View All Sales Section
    st.subheader("All Sales")
    sales = sale_manager.get_all_sales()
    sales_df = pd.DataFrame(sales)
    st.write(sales_df)

# **Summary and Business Insights**
elif page == "Summary":
    st.title("Business Summary and Insights")

    # Fetch customer data for the customer purchase frequency visualization
    customers = customer_manager.get_all_customers()  # Add this line to fetch customers

    # Business Insights (Example: Total Sales Visualization)
    sales = sale_manager.get_all_sales()
    sales_df = pd.DataFrame(sales)

    if not sales_df.empty:
        sales_df['TotalAmount'] = sales_df['quantity'] * sales_df['total_amount']
        total_sales = sales_df['TotalAmount'].sum()

        st.subheader(f"Total Sales: ${total_sales:,.2f}")

        # Visualization: Total Sales by Product
        sales_by_product = sales_df.groupby('product_id')['TotalAmount'].sum().reset_index()
        product_sales = product_manager.get_all_products()
        product_sales_dict = {p['product_id']: p['name'] for p in product_sales}
        sales_by_product['Product Name'] = sales_by_product['product_id'].map(product_sales_dict)

        # **Customer Purchase Frequency** Visualization
        customer_purchase_frequency = sales_df.groupby('customer_id').size().reset_index(name='Purchase Count')

        # Ensure customers data is available before using it
        customers_dict = {c['customer_id']: c['name'] for c in customers}
        customer_purchase_frequency['Customer Name'] = customer_purchase_frequency['customer_id'].map(customers_dict)

        # **Top-Selling Products (Count of Product Sales)** Visualization
        product_sales_count = sales_df.groupby('product_id').size().reset_index(name='Sales Count')
        product_sales_count['Product Name'] = product_sales_count['product_id'].map(product_sales_dict)

        # Create a single figure with 3 subplots side by side
        fig, axes = plt.subplots(1, 3, figsize=(18, 8))  # 1 row, 3 columns

        # Plot Total Sales by Product
        axes[0].bar(sales_by_product['Product Name'], sales_by_product['TotalAmount'])
        axes[0].set_xlabel('Product Name')
        axes[0].set_ylabel('Total Sales')
        axes[0].set_title('Total Sales by Product')
        axes[0].tick_params(axis='x', rotation=45)

        # Plot Customer Purchase Frequency
        axes[1].bar(customer_purchase_frequency['Customer Name'], customer_purchase_frequency['Purchase Count'])
        axes[1].set_xlabel('Customer Name')
        axes[1].set_ylabel('Purchase Frequency')
        axes[1].set_title('Customer Purchase Frequency')
        axes[1].tick_params(axis='x', rotation=45)

        # Plot Top-Selling Products as Pie Chart
        top_selling_products = product_sales_count.sort_values(by='Sales Count', ascending=False).head(10)
        axes[2].pie(top_selling_products['Sales Count'], labels=top_selling_products['Product Name'], autopct='%1.1f%%', startangle=90)
        axes[2].set_title('Top-Selling Products')

        # Adjust layout for better spacing
        plt.tight_layout()
        st.pyplot(fig)

    else:
        st.warning("No sales data available.")


