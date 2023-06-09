import threading
import time
import socket
import json
import traceback
import os
import win32print
from win32print import JOB_INFO_1
from win32com.client import Dispatch
import webbrowser
import random
import tkinter as tk
from tkinter import ttk
import pyperclip
from datetime import datetime
from tkinter import *
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText
import mysql.connector
from tkinter import PhotoImage
from PIL import Image, ImageTk
from jinja2 import Template
from tempfile import NamedTemporaryFile
from effects import *
from browser import *
from database import *
from ui_toggle import *
from icons import *
from print import *
from log_events import *
import hashlib
import re

# initialize the global variables
selected_table = None
selected_button = None
server_button = None
ws_button = None
other_button = None
background_color = '#26242f'
button_background_color = '#545166'
white_foreground_color = '#ffffff'
blue_foreground_color = '#6da7d2'
highlight_color = '#bfd660'

mysql_host = '192.168.1.156'
mysql_database = 'sellercloud'
mysql_user = 'python'
mysql_password = 'ghXryPCSP2022!'

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

log_path = "C:\\HarvestAudit\\log.txt"

# Define a function to log messages
def log_message(message, log_type="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_path, "a") as log_file:
        log_file.write(f"{timestamp} [{log_type.upper()}] {message}\n")
        
def save_data():
    data = {
        "search_box_value": search_var.get(),
        "listbox_selection": listbox.get(listbox.curselection()) if listbox.curselection() else None,
        "value1": value1.cget("text"),
        "value2": value2.cget("text"),
        "value3": value3.cget("text"),
        "parts_search_box2_value": parts_search_var2.get(),
        "table2_selection": table2.item(table2.selection())["values"] if table2.selection() else None,
    }
    with open("C:\\HarvestAudit\\data\\ui_state.json", "w") as f:
        json.dump(data, f)
        
    threading.Timer(20.0, save_data).start() # call this function again after 20 seconds
        
def unlock_admin_features():

    pass

def login_as_admin():
    global user_label
    print(f"User label: {user_label.cget('text')}")
    if user_label.cget("text") == "Admin":
        messagebox.showinfo("Admin Logout", "You have successfully logged out as an administrator.")
    
        return
    # Create the login window
    login_window = tk.Toplevel()
    login_window.title("Unlock Admin Features")
    login_window.geometry("400x200")
    
    login_frame = tk.Frame(login_window)
    login_frame.pack()
    
    # Create the username label and entry widget
    username_label = tk.Label(login_frame, text="Username")
    username_label.pack()
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    # Create the password label and entry widget
    password_label = tk.Label(login_frame, text="Password")
    password_label.pack()
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.pack()
    
    username = username_entry.get()
    password = password_entry.get()

    # Create the login button
    login_button = tk.Button(login_frame, text="Login", command=lambda: check_login(username, password))
    login_button.pack()

    def check_login(username, password):
        # Connect to the database
        connection = mysql.connector.connect(host=mysql_host,
                                             port=3306,
                                             database=mysql_database,
                                             user=mysql_user,
                                             password=mysql_password)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the entered username and password are valid
        cursor.execute('SELECT is_admin FROM sellercloud.users WHERE username=%s AND password=%s', (username, hashed_password))
        result = cursor.fetchone()

        if result is None:
            tk.messagebox.showerror("Error", "Invalid username or password")
        else:
            is_admin = result[0]
            if is_admin:
                # Unlock the advanced features
                load_admin_user(username)
                login_window.destroy()
            else:
                tk.messagebox.showerror("Error", "You do not have admin privileges")

def format_username(username):
    return username.upper()

def create_user():
    def insert_user():
            # Call the validate_form function before inserting data into the database
        if not validate_form():
            return
        
        # Get the username and password
        username = username_entry.get()
        password = password_entry.get()
        initials = initials_entry.get()

            
        # Get the is_admin value
        is_admin = is_admin_var.get()

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        connection = mysql.connector.connect(host=mysql_host,
                                             port=3306,
                                             database=mysql_database,
                                             user=mysql_user,
                                             password=mysql_password)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert the username, hashed password, and is_admin value into the database
        cursor.execute("INSERT INTO sellercloud.users (username, password, is_admin, initials) VALUES (%s, %s, %s, %s)", (username, hashed_password, is_admin, initials))
        connection.commit()

        # Close the create user window
        create_user_window.destroy()
        
        messagebox.showinfo("User Created", f"The user {username} has been created successfully.")
        
    # def validate_initials(initials):
    #     # Allow only alphabetical characters
    #     return re.match("^[a-zA-Z]+$", initials) is not None
    def validate_form():
        # Get the values from the form
        username = username_entry.get()
        password = password_entry.get()
        initials = initials_entry.get()
        # Validate the form
        not_valid = False
        error_message = "Error: Please enter a valid "
        if len(username) == 0:
            error_message += "username"
            not_valid = True
        else:
            # Check if the username is already in the database
            connection = mysql.connector.connect(host=mysql_host,
                                                 port=3306,
                                                 database=mysql_database,
                                                 user=mysql_user,
                                                 password=mysql_password)
            cursor = connection.cursor()
            cursor.execute("SELECT username FROM sellercloud.users WHERE username=%s", (username,))
            result = cursor.fetchone()
            if result is not None:
                messagebox.showerror("ERROR", "Error: The username already exists!")
                return False
                
        if len(password) == 0:
            if error_message != "Error: Please enter a valid ":
                error_message += ", password"
            else:
                error_message += "password"
            not_valid = True
        if len(initials) < 2 or not re.match("^[a-zA-Z]+$", initials):
            if error_message != "Error: Please enter a valid ":
                error_message += ", initials (2 alphabetical characters)"
            else:
                error_message += "initials (2 alphabetical characters)"
            not_valid = True
        error_message += "!"
        if not_valid:
            messagebox.showerror("Error", error_message)
            create_user_window.lift()
            return False
        return True



        
    create_user_window = tk.Toplevel()
    create_user_window.geometry("800x650")
    create_user_window.resizable(False, False)

    # Create left frame
    left_frame = Frame(create_user_window, bg="#1b1923")
    left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    # Set logo image in the center of the left frame
    logo_image = PhotoImage(file="C:\\HarvestAudit\\images\\logo\\PCSP_Original_website_header_tight_crop_250px.png")
    logo_label = Label(left_frame, image=logo_image, bg="#1b1923")
    logo_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Create right frame
    right_frame = Frame(create_user_window, bg="#26242f")
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=2)

    blank_frame = Frame(right_frame, bg="#26242f")
    blank_frame.pack(pady=60)

    # Create "Create User" label in the right frame
    create_user_label = Label(right_frame, text="Create User", font=("Helvetica", 32), fg="#bfd660", bg="#26242f")
    create_user_label.pack(pady=10)
    
    
    # Bind the function to the variable of username_entry
    username_entry_var = StringVar()
    
    # Create username label and entry widget
    username_label = Label(right_frame, text="Username", font=("Helvetica", 13, "bold"), fg="#315954", bg="#26242f")
    username_label.pack(pady=10)
    username_availability = StringVar()

    username_entry = Entry(right_frame, textvariable=username_entry_var, font=("Helvetica", 14))
    username_entry.pack()

    # Create username availability label
    username_availability_label = Label(right_frame, textvariable=username_availability)

    username_availability_label.pack()
    
    username_entry_var.trace("w", lambda name, index, mode: check_username_availability(username_entry))

    # username_entry_var.trace("w", check_username_availability)
    # username_entry_var.trace("w", lambda name, index, mode, username_entry=username_entry: check_username_availability(username_entry))
    # username_entry_var.trace("w", lambda name, index, mode, entry=username_entry: check_username_availability(entry))

    
    # Create password label and entry widget
    password_label = Label(right_frame, text="Password", font=("Helvetica", 13, "bold"), fg="#315954", bg="#26242f")
    password_label.pack(pady=10)
    password_entry = Entry(right_frame, show="*", font=("Helvetica", 14))
    password_entry.pack()
    
    # Create initials label and entry widget
    initials_label = tk.Label(right_frame, text="Initials", font=("Helvetica", 13, "bold"), fg="#315954", bg="#26242f")
    initials_label.pack(pady=10)

    def validate_initials(initials):
        # Allow only alphabetical characters and maximum length of 2
        if re.match("^[a-zA-Z]{0,2}$", initials):
            return True
        else:
            messagebox.showerror("Invalid Initials", "Initials must contain only alphabetical characters and be two characters.")
            create_user_window.lift()
            return False
        
    def check_username_availability():
        # Get the entered username
        username = username_entry.get()
        print(username)
        
        # Connect to the database
        connection = mysql.connector.connect(host=mysql_host,
                                            port=3306,
                                            database=mysql_database,
                                            user=mysql_user,
                                            password=mysql_password)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        # Query the database to check if the username already exists
        cursor.execute("SELECT COUNT(*) FROM sellercloud.users WHERE username = %s", (username,))
        result = cursor.fetchone()

        # Update the availability label
        if result[0] > 0:
            username_availability_label.config(text="Username is already taken!", fg="red")
            username_availability.set("Username is already taken!")
            # username_availability_label.config(fg="red")
        else:
            username_availability.set("Username is available")
            username_availability_label.config(fg="green")
        

    initials_var = tk.StringVar()
    initials_entry = tk.Entry(right_frame, font=("Helvetica", 14), textvariable=initials_var)
    initials_entry.pack()
    initials_entry.config(validate='key', validatecommand=(initials_entry.register(validate_initials), '%P'))
    
    # Create is_admin checkbox
    is_admin_var = BooleanVar()
    is_admin_checkbox = Checkbutton(right_frame, text="Is Admin", variable=is_admin_var, font=("Helvetica", 13), bg="#26242f", fg="#ffffff", activebackground="#26242f", selectcolor="#26242f")
    is_admin_checkbox.pack(pady=10)
    
    # Create create user button
    create_button = Button(right_frame, text="Create", font=("Helvetica", 14), bg="#26242f", fg="#ffffff", padx=20, pady=10, command=insert_user)
    create_button.pack(pady=20)
    create_button.config(cursor="hand2", relief=FLAT, background="#FFFFFF", foreground="#26242f", height=1)

# def add_admin_confirm(is_admin_checkbox, is_admin):
#     # check if the checkbox was selected or deselected
#     if is_admin.get() == 1:
#         # if the checkbox was selected, show a confirmation message
#         response = messagebox.askquestion("Admin Confirmation", "Are you sure you want to make this user an admin?")
#         if response == "no":
#             is_admin_checkbox.deselect()
#             is_admin_checkbox.config(fg="red")
#         else:
#             is_admin_checkbox.config(fg="#bfd660")
        
    
def fetch_data(listbox):
    global selected_button, server_button, ws_button, other_button, background_color, original_items
    # change all three buttons to default state
    server_button.config(fg='#ffffff', bg=background_color)
    ws_button.config(fg='#ffffff', bg=background_color)
    other_button.config(fg='#ffffff', bg=background_color)
    # Connect to the MySQL database
    connection = mysql.connector.connect(host=mysql_host,
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)

    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute the SQL query using an inner query to sort by AggregateQty first then query the PURCHASEGROUP column
        query = """SELECT t.PURCHASEGROUP
           FROM (
               SELECT DISTINCT PURCHASEGROUP, AggregateQty
               FROM ChassisProduct
               WHERE PURCHASEGROUP <> '' AND PURCHASEGROUP IS NOT NULL AND PURCHASEGROUP <> 'nan'
           ) AS t
           ORDER BY t.AggregateQty"""


        cursor.execute(query)

        # Fetch the results
        chassis_data = cursor.fetchall()

        # Clear the listbox
        listbox.delete(0, tk.END)

        # Add the fetched data to the listbox and the original_items list
        for chassis_tuple in chassis_data:
            chassis = chassis_tuple[0]  # Unpack the tuple to remove the brackets
            listbox.insert(tk.END, chassis)
            original_items.append(chassis)

    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()

def fetch_chassis_with_harvest_parts(listbox):
    # Connect to the MySQL database
    connection = mysql.connector.connect(host=mysql_host,
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)

    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute the SQL query to fetch the distinct ChassisPurchaseGroups
        query = "SELECT DISTINCT ChassisPurchaseGroup FROM sellercloud.harvest_parts"

        cursor.execute(query)

        # Fetch the results
        chassis_data = cursor.fetchall()

        # Clear the listbox
        listbox.delete(0, tk.END)
        original_items = []

        # Add the fetched data to the listbox and the original_items list
        for chassis_tuple in chassis_data:
            chassis = chassis_tuple[0]  # Unpack the tuple to remove the brackets
            listbox.insert(tk.END, chassis)
            original_items.append(chassis)

    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()

def fetch_chassis_without_harvest_parts(listbox):
    # Connect to the MySQL database
    connection = mysql.connector.connect(host=mysql_host,
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)

    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute the SQL query to fetch the distinct PURCHASEGROUP values
        # from ChassisProduct that are not in the ChassisPurchaseGroup column
        # of the harvest_parts table
        query = """
            SELECT DISTINCT cp.PURCHASEGROUP
            FROM sellercloud.ChassisProduct cp
            LEFT JOIN sellercloud.harvest_parts hp
                ON cp.PURCHASEGROUP = hp.ChassisPurchaseGroup
            WHERE hp.ChassisPurchaseGroup IS NULL
                AND cp.PURCHASEGROUP <> '' AND cp.PURCHASEGROUP IS NOT NULL AND cp.PURCHASEGROUP <> 'nan'
            ORDER BY cp.PURCHASEGROUP
        """

        cursor.execute(query)

        # Fetch the results
        chassis_data = cursor.fetchall()

        # Clear the listbox
        listbox.delete(0, tk.END)
        original_items = []
        
        # Add the fetched data to the listbox and the original_items list
        for chassis_tuple in chassis_data:
            chassis = chassis_tuple[0]  # Unpack the tuple to remove the brackets
            listbox.insert(tk.END, chassis)
            original_items.append(chassis)

    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()
        
def fetch_and_update_labels(event, listbox, value1, value2, table1):
    if event.state == 4:  # check if Control key is held down
        return  # exit the function if Control key is pressed
    selected_item = listbox.get(listbox.curselection())

    connection = mysql.connector.connect(host=mysql_host,
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        query = "SELECT LocationNotes FROM ChassisProduct WHERE PURCHASEGROUP = %s LIMIT 1"

        cursor.execute(query, (selected_item,))
        
        result = cursor.fetchall()
        
        print(result)
        
        count = len(result)
        
        log_message(f"Location notes results: {count}")

        location_notes = result[0] if result else '-'
        # location_notes = location_notes.replace('nan', '-').replace('{', '').replace('}', '')

        value1.config(text=selected_item)
        value2.config(text=location_notes)

        # Query for parts associated with the selected purchase group
        query = """
            SELECT ap.ProductType, ap.ProductID, ap.ProductName, SUM(be.QtyAvailable), ap.InventoryHighStockNotice
            FROM sellercloud.harvest_parts AS hp
            LEFT JOIN sellercloud.AllProducts AS ap ON hp.PartProductID = ap.ProductID
            LEFT JOIN sellercloud.BinExport AS be ON be.ProductID = ap.ProductID
            WHERE hp.ChassisPurchaseGroup = %s AND ap.ProductID IS NOT NULL
            GROUP BY ap.ProductID, ap.ProductName, ap.ProductType, ap.InventoryHighStockNotice

            UNION ALL

            SELECT 'CASE COMPONENT', hp.PartProductID, hp.PartProductID, NULL, NULL
            FROM sellercloud.harvest_parts AS hp
            LEFT JOIN sellercloud.AllProducts AS ap ON hp.PartProductID = ap.ProductID
            WHERE hp.ChassisPurchaseGroup = %s AND ap.ProductID IS NULL
        """
        cursor.execute(query, (selected_item, selected_item))
        results = cursor.fetchall()
        
        # print(results)
        
        count = len(results)
        
        log_message(f"Parts results: {count}")

        # Clear table1
        for row in table1.get_children():
            table1.delete(row)
        
        # Create a dictionary to store the unique part types and their descriptions
        unique_type = {}
        
        # Add the fetched parts to table1
        for result in results:
            type = result[0].lower().replace('parts - ', '')
            keywords = {"motherboard", "psu", "power supply", "heatsink", "backplane", "control panel"}
            
            if type in ['part', 'parts']:
                # print("UNIQUE", unique_type)
                for keyword in keywords:
                    # print("KEYWORD: ", keyword)
                    if keyword in result[2].lower():
                        unique_type[keyword] = result[2]
                        break
                # print("part")
            else:
                if type not in unique_type:
                    unique_type[type] = result[2]
            # if result[1] not in unique_type:

            if result[4] is not None:
                high_stock_notice = str(result[4])
                if high_stock_notice == "nan":
                    high_stock_notice = "-"
                else:
                    # convert to int
                    high_stock_notice = int(float(high_stock_notice))
            else:
                high_stock_notice = "-"
            table1.insert('', 'end', values=(result[0], result[1], result[2], result[3], high_stock_notice))
        print("__________________________")
        hide_icons()
        for part in unique_type:
            # add_icon(part, icon_frame)
            show_icon(part)
            icon_frame.update()
            
        # get the number of parts in the table
        count = len(table1.get_children())
        print("COUNT: ", count)
        value3.config(text=count)

    finally:
        cursor.close()
        connection.close()

# Unhide a canvas based on the name of the icon
def show_icon(icon_name):
    for i, icon_canvas in enumerate(icon_canvas_list):
        if icon_canvas.icon_name == icon_name:
            icon_canvas.create_image(0, 0, anchor=tk.NW, image=icon_photo_list[i]) 
            
def create_icons(icon_frame):
    for name in icon_names:
        path = icon_path
        if name == 'motherboard':
            path += "motherboard.png"
        elif name == 'power supply':
            path += "power-supply.png"
        elif name == 'heatsink':
            path += "heatsink.png"
        elif name == 'fan':
            path += "cooling-fan.png"
        elif name == 'case component':
            path += "component.png"
        elif name == 'backplane':
            path += "backplane.png"
        icon = Image.open(path)
        icon = icon.resize((50, 50), Image.ANTIALIAS)
        icon_image = ImageTk.PhotoImage(icon)
        canvas = tk.Canvas(icon_frame, width=50, height=50, bg='#26242f', highlightthickness=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=icon_image)
        canvas.pack(side='left')
        canvas.icon_name = name
        icon_photo_list.append(icon_image)
        icon_canvas_list.append(canvas)

# Define function to show icons
def show_icons():
    for icon_canvas in icon_canvas_list:
        icon_canvas.pack()

# Define function to hide icons
def hide_icons():
    for icon_canvas in icon_canvas_list:
        icon_canvas.pack_forget()
         
class MyApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.icon = None
        # ... rest of your code ...

    def add_icon(self, type, icon_frame):
        try:
            print(f"Adding icon for {type}")
            icon_path = "C:\\HarvestAudit\\images\\icon\\"
            if type == 'motherboard':
                icon_path += "motherboard.png"
            elif type == 'power supply':
                icon_path += "power-supply.png"
            elif type == 'heatsink':
                icon_path += "heatsink.png"
            elif type == 'fan':
                icon_path += "cooling-fan.png"
            elif type == 'case component':
                icon_path += "component.png"
            elif type == 'backplane':
                icon_path += "backplane.png"
            print(f"Icon path: {icon_path}")

            icon = Image.open(icon_path)
            icon = icon.resize((50, 50), Image.ANTIALIAS)

            self.icon = ImageTk.PhotoImage(icon)

            # Create a canvas for the image
            canvas = tk.Canvas(icon_frame, width=50, height=50, bg='#26242f', highlightthickness=0)
            canvas.pack(side='left')
            canvas.create_image(0, 0, anchor=tk.NW, image=self.icon)
        except Exception as e:
            print("Error adding icon: " + str(e))
            
def search_and_update_treeview(*args):
    search_keyword = parts_search_var2.get().lower()
    # only search if the search keyword is at least 2 characters long
    if len(search_keyword) < 3:
        return
        
    search_keyword = search_keyword.replace(" ", "%")

    connection = mysql.connector.connect(host=mysql_host,
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)
    try:
        cursor = connection.cursor()

        query = ("SELECT ap.ProductType, ap.ProductID, ap.ProductName, SUM(be.QtyAvailable), ap.InventoryHighStockNotice "
                 "FROM sellercloud.AllProducts AS ap "
                 "LEFT JOIN sellercloud.BinExport AS be ON ap.ProductID = be.ProductID "
                 "WHERE ap.ProductType LIKE %s AND ap.ProductName LIKE %s "
                 "GROUP BY ap.ProductID, ap.ProductType, ap.ProductName, ap.InventoryHighStockNotice;")
        cursor.execute(query, ("%part%", f"%{search_keyword}%"))

        # Clear the existing items in the TreeView
        for item in table2.get_children():
            table2.delete(item)

        # Insert the new items into the TreeView
        for row in cursor.fetchall():
            treeview_values = (row[0], row[1], row[2], int(row[3]) if row[3] else 0, '-')
            if treeview_values[3] != '-':
                high_stock_notice = str(treeview_values[3])
                if high_stock_notice == "nan":
                    high_stock_notice = "-"
                if high_stock_notice != "-":
                    high_stock_notice = int(high_stock_notice)
                treeview_values = (treeview_values[0], treeview_values[1], treeview_values[2],  treeview_values[2], high_stock_notice)
            table2.insert('', 'end', values=treeview_values)


    except Exception as err:
        log_message(f"Error: {err}")
        log_message(f"Query: {query}")
        
    finally:
        cursor.close()
        connection.close()

def fetch_sku(search_box, listbox):
    search_keyword = search_box.get().strip().upper()
    
    search_keyword = search_keyword.replace(" ", "%")

    # Connect to the database
    connection = get_connection()

    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Query the sellercloud.chassisproduct table to find the PURCHASEGROUP for the given ProductID (keyword)
        query = "SELECT PURCHASEGROUP, ProductID FROM sellercloud.ChassisProduct WHERE UPPER(ProductID) LIKE %s"
        cursor.execute(query, (f"%{search_keyword}%",))

        results = cursor.fetchall()

        if results:
            # Clear the list widget
            listbox.delete(0, tk.END)

            for result in results:
                purchase_group = result[0]  # Get the PURCHASEGROUP value from the result

                # Find the corresponding PURCHASEGROUP in the original_items array
                found_items = [item for item in original_items if purchase_group == item]

                # Add the found PURCHASEGROUP to the list widget without duplicates
                for item in found_items:
                    if item not in listbox.get(0, tk.END):  # Check if the item is not already in the listbox
                        listbox.insert(tk.END, item)
        else:
            messagebox.showwarning(title='Warning', message='No PURCHASEGROUP found for the given SKU.')
    except Exception as err:
        log_message(f"Error: {err}")
        log_message(f"Query: {query}")

    finally:
        cursor.close()
        connection.close()

def flash_color(color, duration):
    print("flash_color function called")
    # Create the popup window
    popup = tk.Toplevel(root)

    # popup.title("Popup Window")
    popup.configure(background=color)
    popup.wm_attributes("-alpha", 0.0)

    # Get the main window position
    x = root.winfo_x()
    y = root.winfo_y()

    # Set the new window's position to the same as the main window
    popup.geometry("20000x20000")
    # popup.attributes("-fullscreen", True)
    

    # Define a function to gradually increase the popup window transparency
    def fade_in(alpha):
        if alpha < 1.0:
            popup.wm_attributes("-alpha", alpha)
            alpha += 0.05
            popup.after(15, lambda: fade_in(alpha))

    # Define a function to gradually decrease the popup window transparency
    def fade_out(alpha):
        if alpha > 0.0:
            popup.wm_attributes("-alpha", alpha)
            alpha -= 0.05
            popup.after(15, lambda: fade_out(alpha))
        else:
            popup.destroy()

    # Show the popup window and start the transparency fade-in and fade-out animations
    popup.attributes("-topmost", True)
    popup.lift()
    fade_in(0.0)
    popup.after(duration, lambda: fade_out(1.0))
    
def add_to_harvestable(event, table2, table1, value1):
    user = user_label.cget('text')
    chassis = value1.cget('text')
    if btn_add_to_harvest['state'] == tk.DISABLED:
        return
    
    if value1.cget('text') != '-':
        selected_items = list(table2.selection())
        selected_items.append(combo_box.get())
        selected_items = tuple(selected_items)
        print(f"Selected items: -{selected_items}-")
        if selected_items == () or selected_items == ('',):
            # flash_color('red', 500)
            messagebox.showwarning(title='Warning', message='What am I adding exactly? Select an item first')
            return
        
        count = len(table1.get_children())
        
        # Get all items in table1
        existing_items = table1.get_children()

        connection = mysql.connector.connect(host=mysql_host,
                                             port=3306,
                                             database=mysql_database,
                                             user=mysql_user,
                                             password=mysql_password)
        try:
            cursor = connection.cursor()
            
            logs = []
            
            for item in selected_items:
                if isinstance(item, str):
                    item_values = (item,)
                    is_combo_box = True
                    print("Item is a string", item)
                    print("Item values", item_values)
                else:
                    item_values = table2.item(item, 'values')
                    is_combo_box = False

                # Check for duplicates in table1
                duplicate = False
                for existing_item in existing_items:
                    existing_values = table1.item(existing_item, 'values')
                    if item_values == existing_values:
                        duplicate = True
                        break
                    if is_combo_box and item == existing_values[1]:
                        # Check if a row with same PartProductID exists when adding a CASE COMPONENT from combo box
                        print("Duplicate found", item, existing_values[1])
                        duplicate = True
                        break



                # Insert the item into the database and table1 if it's not a duplicate
                if not duplicate:
                    chassis_purchase_group = value1.cget('text')
                    if is_combo_box:
                        part_product_id = combo_box.get()                     
                        insert_query = "INSERT INTO sellercloud.harvest_parts (ChassisPurchaseGroup, PartProductID) VALUES (%s, %s)"
                        cursor.execute(insert_query, (chassis_purchase_group, part_product_id))
                        connection.commit()
                        item_values = ('CASE COMPONENT',part_product_id, part_product_id, None, '-')
                    else:
                        part_product_id = item_values[1]  # Assuming SKU is the second value in item_values
                        insert_query = "INSERT INTO sellercloud.harvest_parts (ChassisPurchaseGroup, PartProductID) VALUES (%s, %s)"
                        cursor.execute(insert_query, (chassis_purchase_group, part_product_id))
                        connection.commit()
                        
                    logs.append((user, part_product_id, chassis, "add")) # Add log to the list
                    
                    table1.insert('', 'end', values=item_values)
                    count = count + 1
                    value3.configure(text=count)

            log_add_remove_event(logs)
            table1.selection_remove(table1.selection())
            table2.selection_remove(table2.selection())

        finally:
            cursor.close()
            connection.close()

    else:
        messagebox.showwarning(title='Warning', message='Please select a chassis first.')

def remove_from_harvestable(event, table1, table2, value1):
    user = user_label.cget('text')
    chassis = value1.cget('text')
    if btn_remove_harvest['state'] == tk.DISABLED:
        return
    
    # selected_items = table1.selection()
    if value1.cget('text') != '-':
        selected_items = table1.selection()
        if selected_items == ():
            # flash_color('red', 500)
            messagebox.showwarning(title='Warning', message='Please select an item to remove.')
            return
        
        count = len(table1.get_children())

        # Add the confirmation prompt
        user_response = messagebox.askyesno(title='Confirmation',
                                            message='Are you sure you want to remove the selected items?')

        # If the user clicked 'No', do not proceed
        if not user_response:
            return

        connection = mysql.connector.connect(host=mysql_host,
                                            port=3306,
                                            database=mysql_database,
                                            user=mysql_user,
                                            password=mysql_password)
        try:
            cursor = connection.cursor()
            logs = []
            for item in selected_items:
                item_values = table1.item(item, 'values')
                chassis_purchase_group = value1.cget('text')
                part_product_id = item_values[1]  # Assuming SKU is the second value in item_values
                logs.append((user, part_product_id, chassis, "remove")) # Add log to the list
                delete_query = "DELETE FROM sellercloud.harvest_parts WHERE ChassisPurchaseGroup = %s AND PartProductID = %s"
                cursor.execute(delete_query, (chassis_purchase_group, part_product_id))
                connection.commit()

                table1.delete(item)
                # flash_color('green', 500)
                               
                count = count - 1
                
                value3.configure(text=count)
                
            log_add_remove_event(logs)
            table1.selection_remove(table1.selection())
            table2.selection_remove(table2.selection())

        finally:
            cursor.close()
            connection.close()

import win32print

def print_selected_row(event, table, selected_printer, qty_var, initials):
    table = get_selected_table(table1, table2)
    printer_name = selected_printer.get()
    user = user_label.cget('text')
    chassis = value1.cget('text')
    # initials = initials_entry.get()
    # printer_name = "ZDesigner GX420d"
    # initials = "ML"

    if printer_name == "Select a printer":
        messagebox.showwarning(title='Warning', message='Please select a printer before printing.')
        return

    qty = qty_var.get()

    if not qty or not qty.isdigit() or int(qty) < 1:
        messagebox.showwarning(title='Warning', message='Please enter a valid quantity.')
        return

    # if initials == "-" or initials == "":
    #     messagebox.showwarning(title='Warning', message='Please enter your initials.')
    #     return

    # Get the selected row from the table
    qty = int(qty)
    initials = initials.upper()
    
    selected_rows = table.selection()
    # Create an empty list to store logs
    logs = []

    # Loop through selected rows
    for selected_row in selected_rows:
        sku = table.item(selected_row, "values")[1]
        description = table.item(selected_row, "values")[2]
        try:
            if "dymo" in printer_name.lower():
                print("Printing to DYMO")
                print_dymo_label(printer_name, qty, sku, description, initials)
                logs.append((user, sku, chassis)) # Add log to the list
            else:
                print("Printing to Zebra")
                print_zebra_label(printer_name, qty, sku, description, initials)
                logs.append((user, sku, chassis)) # Add log to the list
            qty_var.set(1)
            # print("Printing")
        except Exception as e:
            # There was an error starting the print job, so close the printer handle and return
            print("Error printing")
            print(traceback.format_exc())
            return

    # Insert the logs into the database
    log_print(logs)

def get_selected_table(table1, table2):
    print("Selected table", selected_table)
    if selected_table is table1:
        print("Table 1 selected")
        return table1
    elif selected_table is table2:
        print("Table 2 selected")
        return table2
    else:
        return None

def get_printer_list():
    # Get a list of all printers installed on the system
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS | win32print.PRINTER_INFO_1)
    printer_list = []
    for printer in printers:
        printer_list.append(printer[2])
    return printer_list
       
class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        background_color = '#26242f'

        self.geometry("500x350")
        self.title("Loading Sellercloud Data...")
        self.configure(background=background_color)

        # Create a label for the splash screen
        splash_label = tk.Label(self, text="Please wait while we load the necessary data...", bg=background_color, fg='#ffffff', font=('Arial', 16, 'bold'))
        splash_label.pack(pady=20)
        

        
        # Create a progress bar for the splash screen
        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=20)
        
        self.image_path = "C:\\HarvestAudit\\images\\Logo\\PCSP_Light.png"
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((288, 192), Image.ANTIALIAS)
        
        self.logo = ImageTk.PhotoImage(self.image)
        
        # Create a canvas for the image
        self.canvas = tk.Canvas(self, width=288, height=192, bg=background_color, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.logo)

        # Center the splash screen on the screen
        self.center_on_screen()

        # Center the splash screen on the screen
        self.center_on_screen()
        

    def center_on_screen(self):
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"+{x}+{y}")

def increment_progress(progress, seconds, root):
    try:
        if seconds > 0:
            progress['value'] += random.randint(1, 5)
            root.after(100, increment_progress, progress, seconds - 0.1, root)
    except Exception as e:
        print(e)

def switch_user():
    login_window = tk.Toplevel()
    login_window.title("Switch User Form")
    login_window.geometry("800x550")
    login_window.resizable(False, False)

    # Create left frame
    left_frame = Frame(login_window, bg="#1b1923")
    left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    # Set logo image in the center of the left frame
    logo_image = PhotoImage(file="C:\\HarvestAudit\\images\\logo\\PCSP_Original_website_header_tight_crop_250px.png")
    logo_label = Label(left_frame, image=logo_image, bg="#1b1923")
    logo_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Create right frame
    right_frame = Frame(login_window, bg="#26242f")
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    blank_frame = Frame(right_frame, bg="#26242f")
    blank_frame.pack(pady=60)

    # Create "Switch User" label in the right frame
    welcome_label = Label(right_frame, text="Switch User", font=("Helvetica", 32), fg="#bfd660", bg="#26242f")
    welcome_label.pack(pady=10)

    # Create username label and entry widget
    username_label = Label(right_frame, text="Username", font=("Helvetica", 13, "bold"), fg="#315954", bg="#26242f")
    username_label.pack(pady=10)
    username_entry = Entry(right_frame, font=("Helvetica", 14))
    username_entry.pack()

    # Create password label and entry widget
    password_label = Label(right_frame, text="Password", font=("Helvetica", 13, "bold"), fg="#315954", bg="#26242f")
    password_label.pack(pady=10)
    password_entry = Entry(right_frame, show="*", font=("Helvetica", 14))
    password_entry.pack()

    # Create login button
    def check_login():
        # Get the entered username and password
        username = username_entry.get()
        password = password_entry.get()

        # Connect to the database
        connection = mysql.connector.connect(host=mysql_host,
                                             port=3306,
                                             database=mysql_database,
                                             user=mysql_user,
                                             password=mysql_password)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the entered username and password are valid
        cursor.execute('SELECT is_admin, initials FROM sellercloud.users WHERE username=%s AND password=%s', (username, hashed_password))
        result = cursor.fetchone()

        if result is None:
            tk.messagebox.showerror("Error", "Invalid username or password")
        else:
            is_admin = result[0]
            initials = result[1]
            login_window.destroy()
            if is_admin:
                load_admin_user(username, initials)
            else:
                load_general_user(username, initials)
            
    login_button = tk.Button(right_frame, text="Login", font=("Helvetica", 14), bg="#26242f", fg="#ffffff", padx=20, pady=10, command=check_login)
    login_button.pack(pady=20)
    login_button.config(cursor="hand2", relief=tk.FLAT, background="#FFFFFF", foreground="#26242f", height=1)

def show_login_screen():
    root.withdraw()
    # Create the login window
    login_window = tk.Toplevel()
    login_window.title("Login Form")
    login_window.geometry("800x550")
    login_window.resizable(False, False)

    # Create left frame
    left_frame = Frame(login_window, bg="#1b1923")
    left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    # Set logo image in the center of the left frame
    logo_image = PhotoImage(file="C:\\HarvestAudit\\images\\logo\\PCSP_Original_website_header_tight_crop_250px.png")
    logo_label = Label(left_frame, image=logo_image, bg="#1b1923")
    logo_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Create right frame
    right_frame = Frame(login_window, bg="#26242f")
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    blank_frame = Frame(right_frame, bg="#26242f")
    blank_frame.pack(pady=60)

    # Create "Welcome!" label in the right frame
    welcome_label = Label(right_frame, text="Harvest Audit", font=("Helvetica", 32), fg="#bfd660", bg="#26242f")
    welcome_label.pack(pady=10)

    # Create username label and entry widget
    username_label = Label(right_frame, text="Username", font=("Helvetica", 13, "bold"), fg="#315954", bg="#26242f")
    username_label.pack(pady=10)
    username_entry = Entry(right_frame, font=("Helvetica", 14))
    username_entry.pack()

    # Create password label and entry widget
    password_label = Label(right_frame, text="Password", font=("Helvetica", 13, "bold"), fg="#315954", bg="#26242f")
    password_label.pack(pady=10)
    password_entry = Entry(right_frame, show="*", font=("Helvetica", 14))
    password_entry.pack()

    def on_close():
        # Close the entire application when the login screen is closed
        root.quit()

    login_window.protocol("WM_DELETE_WINDOW", on_close)


    # Create login button
    def check_login():
        # Get the entered username and password
        username = username_entry.get()
        password = password_entry.get()

        # Connect to the database
        connection = mysql.connector.connect(host=mysql_host,
                                             port=3306,
                                             database=mysql_database,
                                             user=mysql_user,
                                             password=mysql_password)

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the entered username and password are valid
        cursor.execute('SELECT is_admin, initials FROM sellercloud.users WHERE username=%s AND password=%s', (username, hashed_password))
        result = cursor.fetchone()

        if result is None:
            tk.messagebox.showerror("Error", "Invalid username or password")
        else:
            is_admin = result[0]
            initials = result[1]
            login_window.destroy()
            show_splash_and_fetch_data(root, listbox, is_admin, username, initials)
            

    login_button = tk.Button(right_frame, text="Login", font=("Helvetica", 14), bg="#26242f", fg="#ffffff", padx=20, pady=10, command=check_login)
    login_button.pack(pady=20)
    login_button.config(cursor="hand2", relief=tk.FLAT, background="#FFFFFF", foreground="#26242f", height=1)

def show_splash_and_fetch_data(root, listbox, is_admin, username, initials):
    try:
               
        # Check the login status
        if is_admin:
            # Unlock advanced features
            load_user("admin", username, initials)
        else:
            # Lock advanced features
            load_user("user", username, initials)
            
        # Show the splash screen
        splash = SplashScreen(root)
                
        # Schedule the data fetching and progress bar updates
        root.after(0, fetch_data, listbox)
        increment_progress(splash.progress, 8, root)

        # Destroy the splash screen and show the main window after 5 seconds
        root.after(5000, lambda: [splash.destroy(), root.deiconify()])
    except Exception as e:
        print(e)

def load_user(user_type, username, initials):
    
    if user_type == "admin":
        # Unlock advanced features
        load_admin_user(username, initials)
        pass
    else:
        # Lock advanced features
        load_general_user(username, initials)
    
def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)

        search_var.set(data['search_box_value'])
        parts_search_var2.set(data['parts_search_box2_value'])
        listbox_selection = data['listbox_selection']
        if listbox_selection:
            index = listbox.get(0, tk.END).index(listbox_selection)
            listbox.selection_set(index)

        value1.config(text=data['value1'])
        value2.config(text=data['value2'])
        value3.config(text=data['value3'])

        # set the Treeview values
        table2.delete(*table2.get_children())
        for row in data['table2_values']:
            table2.insert('', tk.END, values=row)

        root.state('zoomed')
        
    except FileNotFoundError:
        messagebox.showwarning(title='No Data', message='No saved data found.')
        
    except Exception as e:
        messagebox.showerror(title='Error', message='Error loading saved data.')
        print(f"Error loading saved data: {e}")

def load_general_user(username, init):
    log_login_event(username)
    global btn_add_to_harvest, btn_remove_harvest, btn_edit_max_qty, user_label, create_user_btn, initials
    user_label.config(text=username.upper(), fg=highlight_color)
    initials.config(text=init.upper())
    btn_add_to_harvest.pack_forget()
    btn_remove_harvest.pack_forget()
    btn_edit_max_qty.pack_forget()
    create_user_btn.pack_forget()
    
def load_admin_user(username, init):
    log_login_event(username)
    if len(init) != 2:
        init = "XX"
    global btn_add_to_harvest, btn_remove_harvest, btn_edit_max_qty, user_label, button_bar2, create_user_btn, initials
    messagebox.showinfo("Admin Login", "Welcome, administrator! Please be aware that with great power comes great responsibility. As an admin, you have access to sensitive features and information that should be used with care. Please ensure that you are authorized to perform any actions you take.")
    user_label.config(text=username.upper(), fg='red')
    initials.config(text=init.upper())
    btn_add_to_harvest.pack(side='right', padx=10, pady=10)
    btn_remove_harvest.pack(side='right', padx=10, pady=10)
    btn_edit_max_qty.pack(side='right', padx=10, pady=10)
    create_user_btn.pack(padx=10, pady=10)
    init_button(create_user_btn, "", "left")
    
def on_closing():
    # stop all running threads
    for thread in threading.enumerate():
        if thread.is_alive():
            thread.stop()
    # destroy the main window
    root.destroy()

def toggle_button(button, product_type):
    global selected_button, server_button, ws_button, other_button, background_color
    # change all three buttons to default state
    server_button.config(fg='#ffffff', bg=background_color)
    ws_button.config(fg='#ffffff', bg=background_color)
    other_button.config(fg='#ffffff', bg=background_color)
    
    # filter the listbox items based on the product type
    filter_by_product_type(product_type)

    # if button is already selected, deselect it
    if selected_button == button:
        selected_button = None
        return
    
    # change selected button to selected state
    button.config(fg=background_color, bg='#bfd660')
    selected_button = button
    
def update_listbox(listbox, search_term):
    # Clear the listbox
    listbox.delete(0, tk.END)
    
    # Filter the listbox items based on the search term
    for item in original_items:
        if search_term in item.lower():
            # Check if the item is not already in the listbox
            if item not in listbox.get(0, tk.END):
                listbox.insert(tk.END, item)
      
def on_double_click(event, treeview):
    global table2
    item_id = treeview.identify_row(event.y)
    column_id = treeview.identify_column(event.x)
    
    if treeview is table2:
        if item_id and column_id:
            cell_value = treeview.set(item_id, column_id)
            pyperclip.copy(cell_value)
            print(f'Copied: {cell_value}')
        else:
            selected_item = treeview.selection()
            if selected_item:
                values = treeview.item(selected_item, 'values')
                if len(values) > 1 and values[1].lower() == "1100w clear handle":
                  # set the value of parts_search_box2 which uses parts_search_var2 to "1100W Clear Handle"
                  parts_search_var2.set("1100W Clear Handle")   

def update_max_qty_database(sku: str, max_qty: int):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            port=3306,
            database=mysql_database,
            user=mysql_user,
            password=mysql_password
        )
        cursor = connection.cursor()

        # Update the high stock notice value in the database
        query = "UPDATE sellercloud.AllProducts SET InventoryHighStockNotice = %s WHERE ProductID = %s"
        cursor.execute(query, (max_qty, sku))
        connection.commit()
        
    except Exception as e:
        print(f"Error updating max qty for SKU {sku}: {e}")
        
    finally:
        cursor.close()
        connection.close()

def display_max_qty_window(event, table1, table2):
    selection1 = table1.selection()
    selection2 = table2.selection()
    # if selection1 or selection2:
    #     top = tk.Toplevel()
    #     top.title("Edit Max Qty")
    #     top.geometry("1000x400")
    #     top.resizable(False, False)

    #     # Get selected values from Table1
    #     table1_values = table1.item(selection1, 'values') if selection1 else None

    #     # Get selected values from Table2
    #     table2_values = table2.item(selection2, 'values') if selection2 else None

    #     # Display selected values from Table1
    #     if table1_values:
    #         frame1 = tk.Frame(top)
    #         frame1.pack(side=tk.TOP, pady=10)
    #         label1 = tk.Label(frame1, text=f"{table1_values[1]} - {table1_values[2]}", font=("Helvetica", 14))
    #         label1.pack(side=tk.LEFT, padx=10)
    #         entry1 = tk.Entry(frame1, width=10, font=("Helvetica", 14))
    #         entry1.pack(side=tk.LEFT)
    #         button1 = tk.Button(frame1, text="Update", font=("Helvetica", 14), command=lambda: asyncio.run(edit_max_qty(table1_values[1], int(entry1.get()))))
    #         button1.pack(side=tk.LEFT, padx=10)
    #         update_max_qty_database(table1_values[1], int(entry1.get()))

    #     # Display selected values from Table2
    #     if table2_values:
    #         frame2 = tk.Frame(top)
    #         frame2.pack(side=tk.TOP, pady=10)
    #         label2 = tk.Label(frame2, text=f"{table2_values[1]} - {table2_values[2]}", font=("Helvetica", 14))
    #         label2.pack(side=tk.LEFT, padx=10)
    #         entry2 = tk.Entry(frame2, width=10, font=("Helvetica", 14))
    #         entry2.pack(side=tk.LEFT)
    #         button2 = tk.Button(frame2, text="Update", font=("Helvetica", 14), command=lambda: asyncio.run(edit_max_qty(table2_values[1], int(entry2.get()))))
    #         button2.pack(side=tk.LEFT, padx=10)
    #         update_max_qty_database(table2_values[1], int(entry2.get()))

    # else:
    #     messagebox.showwarning(title='Warning', message='Please select a row first.')
    
def update_button_state(treeview, button):
    # if treeview.selection() and combo_box.get() != '':
    button.config(state=tk.NORMAL)
    # else:
    #     button.config(state=tk.DISABLED)

def table_select(treeview, button):
    global selected_table
    selected_table = treeview
    try:
        update_button_state(treeview, button)
        if treeview == table1 and table2.selection():
            print('table1 selected')
            table2.selection_remove(table2.selection())
            table1.focus()
        elif treeview == table2 and table1.selection():
            print('table2 selected')
            table1.selection_remove(table1.selection())
            table2.focus()

    except Exception as e:
        print(f"Error selecting row: {e}")

def select_case_component(event):
    update_button_state(table1, btn_add_to_harvest)

def on_search_box_change():
    search_list(listbox, search_box)
    
def on_search_box_enter(event, listbox, search_box):
    # Get the search term
    search_term = search_box.get().lower()

    # Update the listbox
    update_listbox(listbox, search_term)
        
def search_list(listbox, search_box):
    # Get the search term
    search_term = search_box.get().lower()

    # Update the listbox
    update_listbox(listbox, search_term)
        
def init_button(btn, product_type, side):
    global server_button, ws_button, other_button, selected_button
    btn.pack(side=side, padx=10, pady=10)
    btn.config(background=background_color, foreground='#ffffff', bd=0, highlightthickness=0, font=('Arial', 12, 'bold'))
    btn.bind('<Enter>', lambda event: on_enter(event, btn, selected_button))
    btn.bind('<Leave>', lambda event: on_leave(event, btn, selected_button))

def init_frame(frame):
    frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)
    frame.configure(height=150, bd=0, highlightthickness=0, background=background_color)

def init_label(label):
    label.pack(side='top')
    label.config(background=background_color, foreground=white_foreground_color, font=('Arial', 12, 'bold', 'underline'))

def init_value(value):
    value.pack(side='top')
    value.config(background=background_color, foreground=highlight_color, font=('Arial', 30))

def scroll_listbox(event):
    if event.keysym == "Up":
        if not listbox.curselection():
            listbox.selection_set(0)
            listbox.activate(0)
            listbox.yview_scroll(-1, "units")
        else:
            index = int(listbox.curselection()[0])
            if index == 0:
                return
            listbox.selection_clear(0, END)
            listbox.selection_set(index - 1)
            listbox.activate(index - 1)
            listbox.yview_scroll(-1, "units")
    elif event.keysym == "Down":
        if not listbox.curselection() and listbox.size() > 0:
            listbox.selection_set(0)
            listbox.activate(0)
            listbox.yview_scroll(1, "units")
        else:
            index = int(listbox.curselection()[0])
            if index == listbox.size() - 1:
                return
            listbox.selection_clear(0, END)
            listbox.selection_set(index + 1)
            listbox.activate(index + 1)
            listbox.yview_scroll(1, "units")

def scroll_treeview(event):
    try:
        if event.keysym == "Up":
            if not table2.selection():
                first_item = table2.get_children()[0]
                table2.focus(first_item)
                table2.selection_set(first_item)
                table2.see(first_item)
            else:
                cur_item = table2.focus()
                prev_item = table2.prev(cur_item)
                if prev_item:
                    table2.focus(prev_item)
                    table2.selection_set(prev_item)
                    table2.see(prev_item)
        elif event.keysym == "Down":
            if not table2.selection() and len(table2.get_children()) > 0:
                first_item = table2.get_children()[0]
                table2.focus(first_item)
                table2.selection_set(first_item)
                table2.see(first_item)
            else:
                cur_item = table2.focus()
                next_item = table2.next(cur_item)
                if next_item:
                    table2.focus(next_item)
                    table2.selection_set(next_item)
                    table2.see(next_item)
    except Exception as e:
        print("No items in table2")

# bind key events to increment/decrement quantity
def on_key(event):
    if event.keysym == "Prior":
        qty_var.set(str(int(qty_var.get()) + 1))
    elif event.keysym == "Next":
        qty_var.set(str(max(int(qty_var.get()) - 1, 1)))
    elif event.keysym == "P" and event.state == 16:  # alt+p
        parts_search_box2.focus_set()
    elif event.keysym == "Tab":
        if event.widget == search_box:
            parts_search_box2.focus_set()
            return "break"
        else:
            search_box.focus_set()
            return "break"

def fetch_and_update_labels(event, listbox, value1, value2, table1):
    selected_item = listbox.get(listbox.curselection())

    connection = mysql.connector.connect(host=mysql_host,
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        query = "SELECT LocationNotes FROM ChassisProduct WHERE PURCHASEGROUP = %s LIMIT 1"

        cursor.execute(query, (selected_item,))
        
        result = cursor.fetchall()
        
        print(result)
        
        count = len(result)
        
        log_message(f"Location notes results: {count}")

        location_notes = result[0] if result else '-'
        # location_notes = location_notes.replace('nan', '-').replace('{', '').replace('}', '')

        value1.config(text=selected_item)
        value2.config(text=location_notes)

        # Query for parts associated with the selected purchase group
        query = """
            SELECT ap.ProductType, ap.ProductID, ap.ProductName, SUM(be.QtyAvailable), ap.InventoryHighStockNotice
            FROM sellercloud.harvest_parts AS hp
            LEFT JOIN sellercloud.AllProducts AS ap ON hp.PartProductID = ap.ProductID
            LEFT JOIN sellercloud.BinExport AS be ON be.ProductID = ap.ProductID
            WHERE hp.ChassisPurchaseGroup = %s AND ap.ProductID IS NOT NULL
            GROUP BY ap.ProductID, ap.ProductName, ap.ProductType, ap.InventoryHighStockNotice

            UNION ALL

            SELECT 'CASE COMPONENT', hp.PartProductID, hp.PartProductID, NULL, NULL
            FROM sellercloud.harvest_parts AS hp
            LEFT JOIN sellercloud.AllProducts AS ap ON hp.PartProductID = ap.ProductID
            WHERE hp.ChassisPurchaseGroup = %s AND ap.ProductID IS NULL
        """
        cursor.execute(query, (selected_item, selected_item))
        results = cursor.fetchall()
        
        # print(results)
        
        count = len(results)
        
        log_message(f"Parts results: {count}")

        # Clear table1
        for row in table1.get_children():
            table1.delete(row)
        
        # Create a dictionary to store the unique part types and their descriptions
        unique_type = {}
        
        # Add the fetched parts to table1
        for result in results:
            type = result[0].lower().replace('parts - ', '')
            keywords = {"motherboard", "psu", "power supply", "heatsink", "backplane", "control panel"}
            
            if type in ['part', 'parts']:
                # print("UNIQUE", unique_type)
                for keyword in keywords:
                    # print("KEYWORD: ", keyword)
                    if keyword in result[2].lower():
                        unique_type[keyword] = result[2]
                        break
                # print("part")
            else:
                if type not in unique_type:
                    unique_type[type] = result[2]
            # if result[1] not in unique_type:

            if result[4] is not None:
                high_stock_notice = str(result[4])
                if high_stock_notice == "nan":
                    high_stock_notice = "-"
                else:
                    # convert to int
                    high_stock_notice = int(float(high_stock_notice))
            else:
                high_stock_notice = "-"
            table1.insert('', 'end', values=(result[0], result[1], result[2], result[3], high_stock_notice))
        print("__________________________")
        # if table2.winfo_ismapped():
        #     pass
        # else:
        if icon_frame.winfo_ismapped():
            pass
        else:
            # table_frame1.pack_forget()
            icon_frame.pack(side='top', fill='x', before=table_frame1)
            # icon_frame.place(x=0, y=0)
            # table_frame1.pack(fill='x')
            
        hide_icons()
        for part in unique_type:
            # add_icon(part, icon_frame)
            show_icon(part)
            icon_frame.update()
            
        # get the number of parts in the table
        count = len(table1.get_children())
        print("COUNT: ", count)
        value3.config(text=count)

    finally:
        cursor.close()
        connection.close()

# Unhide a canvas based on the name of the icon
def show_icon(icon_name):
    for i, icon_canvas in enumerate(icon_canvas_list):
        if icon_canvas.icon_name == icon_name:
            icon_canvas.pack(side='left', padx=50)
            
def create_icons(icon_frame):
    global icon_canvas_list, icon_photo_list
    
    for name in icon_names:
        path = icon_path
        if name == 'motherboard':
            path += "motherboard.png"
        elif name == 'power supply':
            path += "power-supply.png"
        elif name == 'heatsink':
            path += "heatsink.png"
        elif name == 'fan':
            path += "cooling-fan.png"
        elif name == 'case component':
            path += "component.png"
        elif name == 'backplane':
            path += "backplane.png"
        icon = Image.open(path)
        icon = icon.resize((150, 150), Image.ANTIALIAS)
        icon_image = ImageTk.PhotoImage(icon)
        canvas = tk.Canvas(icon_frame, width=150, height=150, highlightthickness=0, background=background_color)
        canvas.create_image(0, 0, anchor=tk.NW, image=icon_image)
        canvas.pack()
        canvas.icon_name = name
        icon_photo_list.append(icon_image)
        icon_canvas_list.append(canvas)

# Define function to show icons
def show_icons():
    for icon_canvas in icon_canvas_list:
        icon_canvas.pack()

# Define function to hide icons
def hide_icons():
    for icon_canvas in icon_canvas_list:
        icon_canvas.pack_forget()
         
# create main window
root = tk.Tk()
root.geometry("1300x750")

root.title("Harvest Tool")
root.configure(background=background_color)

# Define icon path and names
icon_path = "C:\\HarvestAudit\\images\\icon\\"
icon_names = ['motherboard', 'power supply', 'heatsink', 'fan', 'case component', 'backplane']

# Create list of canvas widgets for icons
icon_canvas_list = []
icon_photo_list = []
# set window to full screen
# root.attributes("-fullscreen", True)

# # remove maximize button
# root.state("zoomed")

# add exit button to top bar
# root.protocol("WM_DELETE_WINDOW", on_closing)

# List of all the original items in the listbox
original_items = []
# variable to store the search term
search_var = tk.StringVar()

# dymo_printer_name = get_dymo_printer_name()

# if dymo_printer_name:
    # print(f"Found DYMO printer: {dymo_printer_name}")
# else:
    # print("DYMO printer not found")

# create left navigation frame
left_frame = tk.Frame(root, bg='#26242f', width=300)
left_frame.pack(side='left', fill='y')

image_frame = tk.Frame(left_frame, bg='#26242f')
image_frame.pack(side='top', fill='x')

pcsp_logo_path = "C:\\HarvestAudit\\images\\Logo\\PCSP_Light.png"
pcsp_logo = Image.open(pcsp_logo_path)
pcsp_logo = pcsp_logo.resize((96, 64), Image.ANTIALIAS)

pcsp_logo = ImageTk.PhotoImage(pcsp_logo)

# Create a canvas for the image
canvas = tk.Canvas(image_frame, width=96, height=64, bg='#26242f', highlightthickness=0)
canvas.pack(side='left')
canvas.create_image(0, 0, anchor=tk.NW, image=pcsp_logo)


user_frame = tk.Frame(image_frame, bg='#26242f')
user_frame.pack(side='right')
user_icon_path = "C:\\HarvestAudit\\images\\icon\\user.png"
user_icon = Image.open(user_icon_path)
user_icon = user_icon.resize((35, 35), Image.ANTIALIAS)

user_icon = ImageTk.PhotoImage(user_icon)

# Create a canvas for the image
canvas2 = tk.Canvas(user_frame, width=35, height=35, bg='#26242f', highlightthickness=0)
canvas2.pack(side='left', padx=(10, 0))
canvas2.create_image(0, 0, anchor=tk.NW, image=user_icon)

user_label = tk.Button(user_frame, text="Unlock Admin", command=switch_user)
user_label.pack(fill='both', expand=True, side='left')
user_label.config(background='#26242f', fg='white', font=("Helvetica", 22, "bold"), borderwidth=0)
user_frame.bind("<Enter>", lambda event: on_widget_enter(event, user_label))
user_frame.bind("<Leave>", lambda event: on_widget_leave(event, user_label))

create_user_btn = tk.Button(image_frame, text="Create User", command=create_user)


# sc_logo_path = "C:\HarvestAudit\images\logo\SC_Original.png"
# sc_logo = Image.open(sc_logo_path)
# sc_logo = sc_logo.resize((200, 15), Image.ANTIALIAS)

# sc_logo = ImageTk.PhotoImage(sc_logo)

# # Create a canvas for the image
# canvas = tk.Canvas(image_frame, width=96, height=64, bg='#26242f', highlightthickness=0)
# canvas.pack(side='left')
# canvas.create_image(0, 0, anchor=tk.NW, image=sc_logo)

# create button bar
button_bar1 = tk.Frame(left_frame)
button_bar1.pack(side='top')
button_bar1.config(background='#26242f')

# create buttons
server_button = tk.Button(button_bar1, text='Server')
ws_button = tk.Button(button_bar1, text='Workstation')
other_button = tk.Button(button_bar1, text='Other')

init_button(other_button, 'server', 'left')
init_button(server_button, 'workstation', 'left')
init_button(ws_button, 'other', 'left')

# create button bar
button_bar_utils = tk.Frame(left_frame)
button_bar_utils.pack(side='top')
button_bar_utils.config(background='#26242f')

refresh_button = tk.Button(button_bar_utils, text="Refresh", command=lambda: fetch_data(listbox))
refresh_button.pack(side='left' , padx=5, pady=10)
search_sku_button = tk.Button(button_bar_utils, text="Search SKU", command=lambda: fetch_sku(search_box, listbox))
search_sku_button.pack(side='left' , padx=5, pady=10)
with_button = tk.Button(button_bar_utils, text="With", command=lambda: fetch_chassis_with_harvest_parts(listbox))
with_button.pack(side='left' , padx=5, pady=10)
without_button = tk.Button(button_bar_utils, text="Without", command=lambda: fetch_chassis_without_harvest_parts(listbox))
without_button.pack(side='left' , padx=5, pady=10)


init_button(refresh_button, 'server', 'left')
init_button(search_sku_button, 'workstation', 'left')



# create search box
search_box = tk.Entry(left_frame, textvariable=search_var, borderwidth=10, relief=tk.FLAT)
search_box.pack(fill='x', padx=10, pady=10)
search_box.config(background='#5c596b', foreground='#ffffff', font=('Arial', 12, 'bold'))

search_var.trace("w", lambda name, index, mode: on_search_box_change())



# CHASSIS LISTBOX ************************************************************

# create listbox
listbox = tk.Listbox(left_frame, selectmode="extended")
listbox.pack(padx=10, pady=10, fill='both', expand=True)

# configure listbox padding
listbox.configure(background='#26242f', foreground='#ffffff', bd=0, font=('Arial', 12, 'bold'), selectbackground='#bfd660', selectforeground='black', highlightcolor='#26242f', borderwidth=10, relief=tk.FLAT)

# create right frame
right_frame = tk.Frame(root, bg=background_color, padx=10, pady=10)
right_frame.pack(side='left', fill='both', expand=True)

label_frame = tk.LabelFrame(right_frame, height=50)
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", background=background_color, foreground=white_foreground_color, fieldbackground=background_color, font=('Arial', 12, 'bold'))



# CHASSIS LABEL FRAME ****************************************************

label_frame.pack(fill=tk.X, side='top', expand=True)
# label_frame.place(relx=0.5, rely=2, anchor='n')
label_frame.configure(height=150, bd=0, highlightthickness=0, background=background_color, foreground=white_foreground_color)
label_frame.pack_propagate(0)

# create four frames
frame1 = tk.Frame(label_frame)
init_frame(frame1)
label1 = tk.Label(frame1, text='Chassis Purchase Group', font=('Arial', 12))
init_label(label1)
value1 = tk.Label(frame1, text='-')
init_value(value1)


frame2 = tk.Frame(label_frame)
init_frame(frame2)
label2 = tk.Label(frame2, text='Notes', font=('Arial', 12))
init_label(label2)
value2 = tk.Label(frame2, text='-')
init_value(value2)

frame3 = tk.Frame(label_frame)
init_frame(frame3)

# create labels and values


label3 = tk.Label(frame3, text='# of Harvestable', font=('Arial', 12))
init_label(label3)

value3 = tk.Label(frame3, text='-')
init_value(value3)

icon_frame = tk.Frame(right_frame)
icon_frame.configure(height=150, bd=0, highlightthickness=0, background=background_color)

# Create icons and store canvas in list
create_icons(icon_frame)

# Initially hide the icons
hide_icons()
# icon_frame.pack_forget()

# TABLE 1 *************************************************************

table_frame1 = tk.Frame(right_frame)
table_frame1.pack(fill='both', expand=True)
icon_frame.pack(side='top', fill='x', before=table_frame1)
# table_frame1.place(relx=0.5, rely=2, anchor='s')
table_frame1.config(background=background_color, height=700)

# create table1 label
table_label1 = tk.Label(table_frame1, text='Parts to Harvest')
table_label1.pack(side='left')
table_label1.config(background=background_color, foreground=white_foreground_color, font=('Arial', 16, 'bold'))

# define table columns for both tables
table_columns = ('Type', 'SKU', 'Description', 'Qty', 'Max Qty')

# create a variable for the search box in the parts table 
parts_search_var = tk.StringVar()

table1 = ttk.Treeview(right_frame, columns=table_columns, show='headings')
for column in table_columns:
    table1.heading(column, text=column)
table1.pack(fill='both', expand=True)

table1.column("Type", width=120, anchor="center")
table1.column("SKU", width=100, anchor="center")
table1.column("Description", width=300)
table1.column("Qty", width=60, anchor="center")
table1.column("Max Qty", width=80, anchor="center")

# table1.config(height=700)

# create button bar
button_bar2 = tk.Frame(right_frame)
button_bar2.pack(side='top', fill='x')
button_bar2.config(background='#2f2d38', height=50)

btn_print = tk.Button(button_bar2, text='Print Selected')
btn_print.pack(side='left', padx=10, pady=10)
btn_print.config(background=background_color)
init_button(btn_print, "", 'left')

qty_label = tk.Label(button_bar2, text="Qty:")
qty_var = tk.StringVar(value="1")
qty_entry = tk.Entry(button_bar2, textvariable=qty_var, width=5)
qty_label.pack(side='left')
qty_entry.pack(side='left')
qty_label.config(background=background_color, foreground=white_foreground_color, font=('Arial', 12, 'bold'))
qty_entry.config(background=background_color, foreground=white_foreground_color, font=('Arial', 12, 'bold'))

initials_label = tk.Label(button_bar2, text="Initials:")
initials_label.config(background=background_color, foreground=white_foreground_color, font=('Arial', 12, 'bold'))
initials_label.pack(side='left')

initials = tk.Label(button_bar2, text="")
initials.config(background=background_color, foreground=white_foreground_color, font=('Arial', 12, 'bold'))
initials.pack(side='left')

printers = get_printer_list()

# Create a dropdown list widget
menu = tk.StringVar()
menu.set('Select a printer')
dropdown = tk.OptionMenu(button_bar2, menu, *printers)

# dropdown["menu"].bind(label=printers[2], command=lambda printer_name=printers[2]: print("Selected printer: " + printer_name))
dropdown.pack(side='left', padx=10, pady=10)
dropdown.config(background=background_color, foreground=white_foreground_color, font=('Arial', 12, 'bold'), width=25)

# Create a button that toggles the frame
hide_button_text = tk.StringVar()
hide_button_text.set("Hide Parts")
hide_button = tk.Button(button_bar2, textvariable=hide_button_text, command=lambda: toggle_parts_frame(table_frame2, hide_button_text, table2, btn_add_to_harvest, btn_remove_harvest, btn_edit_max_qty, icon_frame, table1))
hide_button.pack(side='left', pady=10)
init_button(hide_button, "", 'left')
    
btn_view_on_google = tk.Button(button_bar2, text='Google')
btn_view_on_google.pack(side='right', padx=10, pady=10)
btn_view_on_google.config(background=highlight_color)

btn_view_on_sellercloud = tk.Button(button_bar2, text='Sellercloud')
btn_view_on_sellercloud.pack(side='right', padx=(50, 5), pady=10)
btn_view_on_sellercloud.config(background=blue_foreground_color)

btn_add_to_harvest = tk.Button(button_bar2, text='Add to Harvestable')

btn_remove_harvest = tk.Button(button_bar2, text='Remove from Harvestable')

btn_edit_max_qty = tk.Button(button_bar2, text='Edit Max Qty')


# init_button(btn_print, "", "right")

# TABLE 2 ************************************************************

table_frame2 = tk.Frame(right_frame)
table_frame2.pack(fill='x')
table_frame2.config(background=background_color)

# create table1 label
table_label2 = tk.Label(table_frame2, text='All Parts')
table_label2.pack(side='left', padx=10, pady=5)
table_label2.config(background=background_color, foreground=blue_foreground_color, font=('Arial', 16, 'bold'))

# create list with options
case_components = ['EARS', 'FEET', 'PCI BLANKS', 'PCI CLIPS', 'FACEPLATE', 'M.2 SCREWS', 'HARD DRIVE SCREWS', 'DVD BRACKET', 'CACHE MODULE', 'RAID BATTERY', 'SATA CABLE(S)']

# create combobox
combo_box = ttk.Combobox(table_frame2, values=case_components)
combo_box.pack(side='left', padx=10, pady=10)
combo_box.config(background=background_color, foreground=white_foreground_color, font=('Arial', 12, 'bold'), width=25)

# create a variable for the search box in the parts table 
parts_search_var2 = tk.StringVar()

# create search box for the table
parts_search_box2 = tk.Entry(table_frame2, textvariable=parts_search_var2, borderwidth=10, relief=tk.FLAT)
parts_search_box2.pack(side='right', padx=10, pady=10)
parts_search_box2.config(background='#5c596b', foreground='#ffffff', font=('Arial', 12, 'bold'))


# Call the search_and_update_treeview function every time the parts_search_var2 value changes
parts_search_var2.trace("w", search_and_update_treeview)


table2 = ttk.Treeview(right_frame, columns=table_columns, show='headings')
for column in table_columns:
    table2.heading(column, text=column)
table2.pack(padx=10, pady=10, fill='both', expand=True)

table2.column("Type", width=120, anchor="center")
table2.column("SKU", width=100, anchor="center")
table2.column("Description", width=300)
table2.column("Qty", width=60, anchor="center")
table2.column("Max Qty", width=80, anchor="center")


# WIDGET BINDINGS ************************************************************
root.bind("<KeyPress>", on_key)
root.bind("<Control-p>", lambda event: print_selected_row(event, selected_table, menu, qty_var, initials.cget('text')))

canvas.bind("<Enter>", on_widget_enter)
canvas.bind("<Leave>", on_widget_leave)
canvas.bind('<ButtonRelease-1>', lambda event: open_pcsp())

other_button.bind('<Button-1>', lambda event: toggle_button(other_button, 'other'))
server_button.bind('<Button-1>', lambda event: toggle_button(server_button, 'server'))
ws_button.bind('<Button-1>', lambda event: toggle_button(ws_button, 'workstation'))


listbox.bind("<Enter>", on_widget_enter)
listbox.bind("<Leave>", on_widget_leave)
listbox.bind("<ButtonRelease-1>", lambda event: fetch_and_update_labels(event, listbox, value1, value2, table1))

btn_view_on_google.bind('<Enter>', lambda event: on_widget_enter)
btn_view_on_google.bind('<Leave>', lambda event: on_widget_leave)
btn_view_on_google.bind('<ButtonRelease-1>', lambda event: view_on_google(selected_table, value1))
btn_print.bind('<ButtonRelease-1>', lambda event: print_selected_row(event, selected_table, menu, qty_var, initials.cget('text')))
btn_view_on_sellercloud.bind('<Enter>', lambda event: on_widget_enter)
btn_view_on_sellercloud.bind('<Leave>', lambda event: on_widget_leave)
btn_view_on_sellercloud.bind('<ButtonRelease-1>', lambda event: view_on_sellercloud(selected_table))
btn_add_to_harvest.bind('<Enter>', lambda event: on_widget_enter)
btn_add_to_harvest.bind('<Leave>', lambda event: on_widget_leave)
btn_add_to_harvest.bind('<ButtonRelease-1>', lambda event: add_to_harvestable(event, table2, table1, value1))
btn_remove_harvest.bind('<Enter>', lambda event: on_widget_enter)
btn_remove_harvest.bind('<Leave>', lambda event: on_widget_leave)
btn_remove_harvest.bind('<ButtonRelease-1>', lambda event: remove_from_harvestable(event, table1, table2, value1))
btn_edit_max_qty.bind('<Enter>', lambda event: on_widget_enter)
btn_edit_max_qty.bind('<Leave>', lambda event: on_widget_leave)
btn_edit_max_qty.bind('<ButtonRelease-1>', lambda event: display_max_qty_window(event, table1, table2))

search_box.bind('<FocusIn>', lambda event: on_search_box_focus_in(event, search_box))
search_box.bind('<FocusOut>', lambda event: on_search_box_focus_out(event, search_box))
search_box.bind('<Return>', lambda event: on_search_box_enter(event, listbox, search_box))
search_box.bind("<Up>", scroll_listbox)
search_box.bind("<Down>", scroll_listbox)
parts_search_box2.bind('<FocusIn>', lambda event: on_search_box_focus_in(event, parts_search_box2))
parts_search_box2.bind('<FocusOut>', lambda event: on_search_box_focus_out(event, parts_search_box2))
parts_search_box2.bind("<Up>", scroll_treeview)
parts_search_box2.bind("<Down>", scroll_treeview)
parts_search_box2.bind("<Return>", lambda event: print_selected_row(event, selected_table, menu, qty_var, initials_entry))

table1.bind('<ButtonRelease-1>', lambda event: table_select(table1, btn_add_to_harvest))
table1.bind('<Double-1>', lambda event: on_double_click(event, table1))
table2.bind('<Double-1>', lambda event: on_double_click(event, table2))

table2.bind('<ButtonRelease-1>', lambda event: table_select(table2, btn_add_to_harvest))

combo_box.bind("<<ComboboxSelected>>", select_case_component)

show_login_screen()
btn_add_to_harvest.config(background=highlight_color, state=tk.NORMAL)
btn_remove_harvest.config(background='red', state=tk.NORMAL)
btn_edit_max_qty.config(background=blue_foreground_color)
root.mainloop()
