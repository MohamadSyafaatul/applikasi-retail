import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            database='retail_db',
            user='root',
            password=''
        )

    def close(self):
        if self.connection.is_connected():
            self.connection.close()

class Product:
    def __init__(self, db):
        self.db = db

    def add_product(self, name, price):
        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
        self.db.connection.commit()
        cursor.close()

    def update_product(self, product_id, name, price):
        cursor = self.db.connection.cursor()
        cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, product_id))
        self.db.connection.commit()
        cursor.close()

    def delete_product(self, product_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        self.db.connection.commit()
        cursor.close()

    def get_products(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT id, name, price FROM products")
        return cursor.fetchall()

class Transaction:
    def __init__(self, db):
        self.db = db

    def add_transaction(self, product_id, quantity, total_price):
        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO transactions (product_id, quantity, total_price, date) VALUES (%s, %s, %s, CURDATE())",
                       (product_id, quantity, total_price))
        self.db.connection.commit()
        cursor.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.db = Database()
        self.product_manager = Product(self.db)
        self.transaction_manager = Transaction(self.db)

        self.create_widgets()
        self.selected_product_id = None  # Initialize selected_product_id

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Retail Management System", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.product_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.product_frame.pack(pady=10, fill='x')

        tk.Label(self.product_frame, text="Product Name", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.product_name_entry = tk.Entry(self.product_frame)
        self.product_name_entry.grid(row=0, column=1)

        tk.Label(self.product_frame, text="Product Price", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.product_price_entry = tk.Entry(self.product_frame)
        self.product_price_entry.grid(row=1, column=1)

        button_style = {'padx': 10, 'pady': 5, 'bg': '#4CAF50', 'fg': 'white', 'font': ('Helvetica', 10, 'bold')}
        tk.Button(self.product_frame, text="Add Product", command=self.add_product, **button_style).grid(row=2, column=0, pady=5)
        tk.Button(self.product_frame, text="Update Product", command=self.update_product, **button_style).grid(row=2, column=1, pady=5)
        tk.Button(self.product_frame, text="Delete Product", command=self.delete_product, **button_style).grid(row=2, column=2, pady=5)

        self.product_table = ttk.Treeview(self.root, columns=("ID", "Name", "Price"), show="headings")
        self.product_table.heading("ID", text="ID")
        self.product_table.heading("Name", text="Name")
        self.product_table.heading("Price", text="Price")
        self.product_table.pack(fill='both', expand=True)
        self.product_table.bind("<Double-1>", self.on_product_select)

        self.transaction_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.transaction_frame.pack(pady=10, fill='x')

        tk.Label(self.transaction_frame, text="Select Product", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.product_combobox = ttk.Combobox(self.transaction_frame)
        self.product_combobox.grid(row=0, column=1)

        tk.Label(self.transaction_frame, text="Quantity", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.quantity_entry = tk.Entry(self.transaction_frame)
        self.quantity_entry.grid(row=1, column=1)

        tk.Button(self.transaction_frame, text="Add Transaction", command=self.add_transaction, **button_style).grid(row=2, columnspan=2, pady=5)

        self.load_products()

    def load_products(self):
        products = self.product_manager.get_products()
        self.product_combobox['values'] = [f"{name} - ${price}" for _, name, price in products]
        for row in self.product_table.get_children():
            self.product_table.delete(row)
        for product in products:
            self.product_table.insert("", tk.END, values=product)

    def on_product_select(self, event):
        selected_item = self.product_table.selection()
        if selected_item:
            product = self.product_table.item(selected_item, "values")
            self.product_name_entry.delete(0, tk.END)
            self.product_name_entry.insert(0, product[1])  # Set product name
            self.product_price_entry.delete(0, tk.END)
            self.product_price_entry.insert(0, product[2])  # Set product price
            self.selected_product_id = product[0]  # Store the selected product ID

    def add_product(self):
        name = self.product_name_entry.get()
        price = self.product_price_entry.get()
        if name and price:
            try:
                self.product_manager.add_product(name, float(price))
                messagebox.showinfo("Success", "Product added successfully!")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def update_product(self):
        if self.selected_product_id:
            name = self.product_name_entry.get()
            price = self.product_price_entry.get()
            if name and price:
                try:
                    self.product_manager.update_product(self.selected_product_id, name, float(price))
                    messagebox.showinfo("Success", "Product updated successfully!")
                    self.load_products()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select a product to update.")

    def delete_product(self):
        if self.selected_product_id:
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
            if confirm:
                try:
                    self.product_manager.delete_product(self.selected_product_id)
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    self.load_products()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")

    def add_transaction(self):
        quantity = self.quantity_entry.get()
        if self.selected_product_id and quantity:
            try:
                quantity = int(quantity)
                price = float(self.product_price_entry.get())
                total_price = quantity * price
                
                # Get the current date and time
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.transaction_manager.add_transaction(self.selected_product_id, quantity, total_price)
                
                # Fetch product name for the message
                product_name = self.product_combobox.get().split(" - ")[0]  # Get the selected product name
                
                messagebox.showinfo("Success", f"Transaction added successfully!\n"
                                                f"Product: {product_name}\n"
                                                f"Quantity: {quantity}\n"
                                                f"Total Price: ${total_price:.2f}\n"
                                                f"Date & Time: {current_time}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()