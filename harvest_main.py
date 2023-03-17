import threading
import time
import qrcode
import webbrowser
import random
import tkinter as tk
from tkinter import ttk
import pyperclip
from tkinter import *
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText
import mysql.connector
from tkinter import PhotoImage
from PIL import Image, ImageTk
from jinja2 import Template
import pdfkit
from tempfile import NamedTemporaryFile
from effects import on_enter, on_leave, on_search_box_focus_in, on_search_box_focus_out, on_listbox_enter, on_listbox_leave
from database import get_connection, query_database

# initialize the global variables
selected_button = None
server_button = None
ws_button = None
other_button = None
background_color = '#26242f'
button_background_color = '#545166'
white_foreground_color = '#ffffff'
blue_foreground_color = '#6da7d2'
highlight_color = '#bfd660'

mysql_host = 'localhost'
mysql_database = 'sellercloud'
mysql_user = 'matt'
mysql_password = 'ghXryPCSP2022!'

def fetch_data(listbox):
    global selected_button, server_button, ws_button, other_button, background_color, original_items
    # change all three buttons to default state
    server_button.config(fg='#ffffff', bg=background_color)
    ws_button.config(fg='#ffffff', bg=background_color)
    other_button.config(fg='#ffffff', bg=background_color)

    # Execute the SQL query using an inner query to sort by AggregateQty first then query the PURCHASEGROUP column
    query = """SELECT t.PURCHASEGROUP
        FROM (
            SELECT DISTINCT PURCHASEGROUP, AggregateQty
            FROM chassisproduct
            WHERE PURCHASEGROUP <> '' AND PURCHASEGROUP IS NOT NULL AND PURCHASEGROUP <> 'nan'
        ) AS t
        ORDER BY t.AggregateQty"""
        
    chassis_data = query_database(query)

    # Clear the listbox
    listbox.delete(0, tk.END)

    # Add the fetched data to the listbox and the original_items list
    for chassis_tuple in chassis_data:
        chassis = chassis_tuple[0]  # Unpack the tuple to remove the brackets
        listbox.insert(tk.END, chassis)
        original_items.append(chassis)

    
def filter_by_product_type(product_type):
    global listbox, original_items

    if product_type == 'server':
        condition = "ProductType = 'Chassis - Server'"
    elif product_type == 'workstation':
        condition = "ProductType = 'Chassis - Workstation'"
    else:
        condition = "ProductType NOT IN ('Chassis - Server', 'Chassis - Workstation')"

    query = f"SELECT DISTINCT PURCHASEGROUP FROM chassisproduct WHERE {condition} AND PURCHASEGROUP <> '' AND PURCHASEGROUP IS NOT NULL AND PURCHASEGROUP <> 'nan' ORDER BY PURCHASEGROUP ASC"
    
    chassis_data = query_database(query)
    
    listbox.delete(0, tk.END)
    # original_items.clear()

    for chassis_tuple in chassis_data:
        chassis = chassis_tuple[0]  # Unpack the tuple
        listbox.insert(tk.END, chassis)
            
        
def fetch_and_update_labels(event, listbox, value1, value2, table1):
    selected_item = listbox.get(listbox.curselection())

    connection = mysql.connector.connect(host='localhost',
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)
    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        query = "SELECT LocationNotes FROM chassisproduct WHERE PURCHASEGROUP = %s"


        result = query_database(query)

        location_notes = result[0] if result else '-'

        value1.config(text=selected_item)
        value2.config(text=location_notes)

        # Query for parts associated with the selected purchase group
        query = """SELECT ap.ProductType, ap.ProductID, ap.ProductName, SUM(be.QtyAvailable) 
                   FROM sellercloud.harvest_parts AS hp
                   LEFT JOIN sellercloud.allproducts AS ap ON hp.PartProductID = ap.ProductID
                   LEFT JOIN sellercloud.binexport AS be ON be.ProductID = ap.ProductID
                   WHERE hp.ChassisPurchaseGroup = %s
                   GROUP BY ap.ProductID, ap.ProductName, ap.ProductType"""

        cursor.execute(query, (selected_item,))
        results = cursor.fetchall()

        # Clear table1
        for row in table1.get_children():
            table1.delete(row)

        # Add the fetched parts to table1
        for result in results:
            table1.insert('', 'end', values=result)
        
        # get the number of parts in the table
        count = len(table1.get_children())
        
        value3.config(text=count)

    finally:
        cursor.close()
        connection.close()

def search_and_update_treeview(*args):
    search_keyword = parts_search_var2.get().lower()
        
    search_keyword = search_keyword.replace(" ", "%")

    connection = mysql.connector.connect(host='localhost',
                                         port=3306,
                                         database=mysql_database,
                                         user=mysql_user,
                                         password=mysql_password)
    try:
        cursor = connection.cursor()

        query = ("SELECT ap.ProductType, ap.ProductID, ap.ProductName, SUM(be.QtyAvailable) "
                 "FROM sellercloud.allproducts AS ap "
                 "LEFT JOIN sellercloud.binexport AS be ON ap.ProductID = be.ProductID "
                 "WHERE ap.ProductType LIKE %s AND ap.ProductName LIKE %s "
                 "GROUP BY ap.ProductID, ap.ProductType, ap.ProductName;")
        cursor.execute(query, ("%part%", f"%{search_keyword}%"))

        # Clear the existing items in the TreeView
        for item in table2.get_children():
            table2.delete(item)

        # Insert the new items into the TreeView
        for row in cursor.fetchall():
            treeview_values = (row[0], row[1], row[2], int(row[3]) if row[3] else 0, '-')
            table2.insert('', 'end', values=treeview_values)

    finally:
        cursor.close()
        connection.close()

def fetch_sku(search_box, listbox):
    search_keyword = search_box.get().strip().upper()
    
    search_keyword = search_keyword.replace(" ", "%")

    # Connect to the database
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database=mysql_database,
        user=mysql_user,
        password=mysql_password
    )

    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Query the sellercloud.chassisproduct table to find the PURCHASEGROUP for the given ProductID (keyword)
        query = "SELECT PURCHASEGROUP, ProductID FROM sellercloud.chassisproduct WHERE UPPER(ProductID) LIKE %s"
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
    if btn_add_to_harvest['state'] == tk.DISABLED:
        return
    
    if value1.cget('text') != '-':
        selected_items = table2.selection()
        if selected_items == ():
            flash_color('red', 500)
            messagebox.showwarning(title='Warning', message='What am I adding exactly? Select an item first')
            return
        
        count = len(table1.get_children())
        
        # Get all items in table1
        existing_items = table1.get_children()

        connection = mysql.connector.connect(host='localhost',
                                             port=3306,
                                             database=mysql_database,
                                             user=mysql_user,
                                             password=mysql_password)
        try:
            cursor = connection.cursor()

            for item in selected_items:
                item_values = table2.item(item, 'values')

                # Check for duplicates in table1
                duplicate = False
                for existing_item in existing_items:
                    existing_values = table1.item(existing_item, 'values')
                    if item_values == existing_values:
                        duplicate = True
                        break

                # Insert the item into the database and table1 if it's not a duplicate
                if not duplicate:
                    chassis_purchase_group = value1.cget('text')
                    part_product_id = item_values[1]  # Assuming SKU is the second value in item_values

                    insert_query = "INSERT INTO sellercloud.harvest_parts (ChassisPurchaseGroup, PartProductID) VALUES (%s, %s)"
                    cursor.execute(insert_query, (chassis_purchase_group, part_product_id))
                    connection.commit()

                    table1.insert('', 'end', values=item_values)
                    # flash_color('green', 500)
                    
                    count = count + 1
                    
                    value3.configure(text=count)


            table1.selection_remove(table1.selection())
            table2.selection_remove(table2.selection())

        finally:
            cursor.close()
            connection.close()

    else:
        messagebox.showwarning(title='Warning', message='Please select a chassis first.')


def remove_from_harvestable(event, table1, table2, value1):
    if btn_remove_harvest['state'] == tk.DISABLED:
        return
    
    # selected_items = table1.selection()
    if value1.cget('text') != '-':
        selected_items = table1.selection()
        if selected_items == ():
            flash_color('red', 500)
            messagebox.showwarning(title='Warning', message='Please select an item to remove.')
            return
        
        count = len(table1.get_children())

        # Add the confirmation prompt
        user_response = messagebox.askyesno(title='Confirmation',
                                            message='Are you sure you want to remove the selected items?')

        # If the user clicked 'No', do not proceed
        if not user_response:
            return

        connection = mysql.connector.connect(host='localhost',
                                            port=3306,
                                            database=mysql_database,
                                            user=mysql_user,
                                            password=mysql_password)
        try:
            cursor = connection.cursor()

            for item in selected_items:
                item_values = table1.item(item, 'values')
                chassis_purchase_group = value1.cget('text')
                part_product_id = item_values[1]  # Assuming SKU is the second value in item_values

                delete_query = "DELETE FROM sellercloud.harvest_parts WHERE ChassisPurchaseGroup = %s AND PartProductID = %s"
                cursor.execute(delete_query, (chassis_purchase_group, part_product_id))
                connection.commit()

                table1.delete(item)
                # flash_color('green', 500)
                               
                count = count - 1
                
                value3.configure(text=count)

            table1.selection_remove(table1.selection())
            table2.selection_remove(table2.selection())

        finally:
            cursor.close()
            connection.close()


def create_label(sku, description):
    html_template = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 12px;
            }}
            .label {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                width: 300px;
                height: 100px;
                border: 1px solid black;
                padding: 10px;
            }}
            .qr-code {{
                width: 80px;
                height: 80px;
            }}
            .label-content {{
                flex-grow: 1;
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="label">
            <div class="label-content">
                <div><strong>SKU:</strong> {sku}</div>
                <div><strong>Description:</strong> {description}</div>
            </div>
            <div class="qr-code">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data={sku}" />
            </div>
        </div>
    </body>
    </html>
    """

    with NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        pdfkit.from_string(html_template, pdf_file.name)
        os.startfile(pdf_file.name, "print")

def print_selected_row(event, table):
    selected_items = table.selection()

    if selected_items:
        item = table.item(selected_items[0])
        values = item['values']
        sku = values[1]
        description = values[2]

        create_label(sku, description)
    else:
        print("No row is selected")


# def get_dymo_printer_name():
#     printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
#     for printer in printers:
#         if 'DYMO LabelWriter 450 Turbo' in printer[2]:
#             return printer[2]
#     return None


       
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
        
        self.image_path = "C:\\HarvestApplication\\images\\Logo\\PCSP_Light.png"
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

        
def show_splash_and_fetch_data(root, listbox):
    try:
        # Hide the main window
        root.withdraw()

        # Show the splash screen
        splash = SplashScreen(root)

        # Schedule the data fetching and progress bar updates
        root.after(0, fetch_data, listbox)
        increment_progress(splash.progress, 8, root)

        # Destroy the splash screen and show the main window after 5 seconds
        root.after(5000, lambda: [splash.destroy(), root.deiconify()])
    except Exception as e:
        print(e)


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
    item_id = treeview.identify_row(event.y)
    column_id = treeview.identify_column(event.x)

    if item_id and column_id:
        cell_value = treeview.set(item_id, column_id)
        pyperclip.copy(cell_value)
        print(f'Copied: {cell_value}')          

def view_on_google(table2):
    selected_item = table2.selection()
    if selected_item:
        item_values = table2.item(selected_item, 'values')
        description = item_values[2]  # Assuming Description is the third value in item_values
        description = description.replace(' ', '+')
        url = f"https://www.google.com/search?q={description}&rlz=1C1ONGR_enUS975US975&sxsrf=AJOqlzXfS0bHTN8aZinRzbsZPd9M4O4h2g:1678991274668&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj-oIf0ieH9AhWRkYkEHfQvC6EQ0pQJegQIJRAE&biw=2400&bih=1321&dpr=0.8"
        webbrowser.open_new_tab(url)
    else:
        messagebox.showwarning(title='Warning', message='Please select a row first.')

def view_on_sellercloud(table2):
    selected_item = table2.selection()
    if selected_item:
        item_values = table2.item(selected_item, 'values')
        sku = item_values[1]  # Assuming SKU is the second value in item_values
        sku = sku.replace(' ', '+')
        url = f"https://pcsp.cwa.sellercloud.com/Inventory/Product_Dashboard.aspx?Id={sku}"
        webbrowser.open_new_tab(url)
    else:
        messagebox.showwarning(title='Warning', message='Please select a row first.')

def update_button_state(treeview, button):
    if treeview.selection():
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)
        

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


# create main window
root = tk.Tk()
root.geometry("1200x750")

root.title("Harvest Tool")
root.configure(background=background_color)

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

image_path = "C:\\Users\\mlassila\\OneDrive - PcServerAndParts\\Desktop\\Logo files\\Logo with tagline\\Light.png"
image = Image.open(image_path)
image = image.resize((96, 64), Image.ANTIALIAS)

logo = ImageTk.PhotoImage(image)

# Create a canvas for the image
canvas = tk.Canvas(left_frame, width=96, height=64, bg='#26242f', highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=logo)

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
other_button.bind('<Button-1>', lambda event: toggle_button(other_button, 'other'))
server_button.bind('<Button-1>', lambda event: toggle_button(server_button, 'server'))
ws_button.bind('<Button-1>', lambda event: toggle_button(ws_button, 'workstation'))

# server_button.bind('<Button-1>', lambda event: filter_by_product_type('server'))
# ws_button.bind('<Button-1>', lambda event: filter_by_product_type('workstation'))
# other_button.bind('<Button-1>', lambda event: filter_by_product_type('other'))

# create button bar
button_bar_utils = tk.Frame(left_frame)
button_bar_utils.pack(side='top')
button_bar_utils.config(background='#26242f')

refresh_button = tk.Button(button_bar_utils, text="Refresh", command=lambda: fetch_data(listbox))
refresh_button.pack(side='left' , padx=10, pady=10)
search_sku_button = tk.Button(button_bar_utils, text="Search SKU", command=lambda: fetch_sku(search_box, listbox))
search_sku_button.pack(side='left' , padx=10, pady=10)

init_button(refresh_button, 'server', 'left')
init_button(search_sku_button, 'workstation', 'left')



# create search box
search_box = tk.Entry(left_frame, textvariable=search_var, borderwidth=10, relief=tk.FLAT)
search_box.pack(fill='x', padx=10, pady=10)
search_box.config(background='#5c596b', foreground='#ffffff', font=('Arial', 12, 'bold'))
search_box.bind('<FocusIn>', lambda event: on_search_box_focus_in(event, search_box))
search_box.bind('<FocusOut>', lambda event: on_search_box_focus_out(event, search_box))
search_box.bind('<Return>', lambda event: on_search_box_enter(event, listbox, search_box))
search_var.trace("w", lambda name, index, mode: on_search_box_change())



# CHASSIS LISTBOX ************************************************************

# create listbox
listbox = tk.Listbox(left_frame)
listbox.pack(padx=10, pady=10, fill='both', expand=True)

# configure listbox padding
listbox.configure(background='#26242f', foreground='#ffffff', bd=0, font=('Arial', 12, 'bold'), selectbackground='#bfd660', selectforeground='black', highlightcolor='#26242f', borderwidth=10, relief=tk.FLAT)
listbox.bind("<Enter>", on_listbox_enter)
listbox.bind("<Leave>", on_listbox_leave)
listbox.bind("<ButtonRelease-1>", lambda event: fetch_and_update_labels(event, listbox, value1, value2, table1))

# create right frame
right_frame = tk.Frame(root, bg=background_color, padx=10, pady=10)
right_frame.pack(side='left', fill='both', expand=True)

label_frame = tk.LabelFrame(right_frame, padx=10, pady=10, height=50)
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", background=background_color, foreground=white_foreground_color, fieldbackground=background_color, font=('Arial', 12, 'bold'))



# CHASSIS LABEL FRAME ****************************************************

label_frame.pack(fill=tk.X)
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



# TABLE 1 *************************************************************

table_frame1 = tk.Frame(right_frame)
table_frame1.pack(fill='x')
table_frame1.config(background=background_color)

# create table1 label
table_label1 = tk.Label(table_frame1, text='Parts to Harvest')
table_label1.pack(side='left', padx=10, pady=5)
table_label1.config(background=background_color, foreground=blue_foreground_color, font=('Arial', 16, 'bold'))

# define table columns for both tables
table_columns = ('Type', 'SKU', 'Description', 'Qty', 'Max Qty')

# create a variable for the search box in the parts table 
parts_search_var = tk.StringVar()

# create search box for the table
parts_search_box = tk.Entry(table_frame1, textvariable=parts_search_var, borderwidth=10, relief=tk.FLAT)
parts_search_box.pack(side='right', padx=10, pady=10)
parts_search_box.config(background='#5c596b', foreground='#ffffff', font=('Arial', 12, 'bold'))
parts_search_box.bind('<FocusIn>', lambda event: on_search_box_focus_in(event, parts_search_box))
parts_search_box.bind('<FocusOut>', lambda event: on_search_box_focus_out(event, parts_search_box))
# parts_search_box.bind('<Return>', lambda event: search_parts(event, listbox, parts_search_box))
# parts_search_var.trace("w", lambda name, index, mode: search_parts())


table1 = ttk.Treeview(right_frame, columns=table_columns, show='headings')
for column in table_columns:
    table1.heading(column, text=column)
table1.pack(padx=10, pady=10, fill='both', expand=True)

table1.column("Type", width=120, anchor="center")
table1.column("SKU", width=100, anchor="center")
table1.column("Description", width=300)
table1.column("Qty", width=60, anchor="center")
table1.column("Max Qty", width=80, anchor="center")
table1.bind('<<TreeviewSelect>>', lambda event: update_button_state(table1, btn_remove_harvest))


# create button bar
button_bar2 = tk.Frame(right_frame)
button_bar2.pack(side='top', fill='x')
button_bar2.config(background='#2f2d38')

btn_print = tk.Button(button_bar2, text='Print Selected')
btn_print.pack(side='left', padx=10, pady=10)
btn_print.config(background=blue_foreground_color)
btn_print.bind('<ButtonRelease-1>', lambda event: print_selected_row(event, table1))

btn_view_on_google = tk.Button(button_bar2, text='Google')
btn_view_on_google.pack(side='right', padx=10, pady=10)
btn_view_on_google.config(background=highlight_color)
btn_view_on_google.bind('<ButtonRelease-1>', lambda event: view_on_google(table2))

btn_view_on_sellercloud = tk.Button(button_bar2, text='Sellercloud')
btn_view_on_sellercloud.pack(side='right', padx=(50, 5), pady=10)
btn_view_on_sellercloud.config(background=blue_foreground_color)
btn_view_on_sellercloud.bind('<ButtonRelease-1>', lambda event: view_on_sellercloud(table2))

btn_add_to_harvest = tk.Button(button_bar2, text='Add to Harvestable')
btn_add_to_harvest.pack(side='right', padx=10, pady=10)
btn_add_to_harvest.config(background=highlight_color, state=tk.DISABLED)
btn_add_to_harvest.bind('<ButtonRelease-1>', lambda event: add_to_harvestable(event, table2, table1, value1))

btn_remove_harvest = tk.Button(button_bar2, text='Remove from Harvestable')
btn_remove_harvest.pack(side='right', padx=10, pady=10)
btn_remove_harvest.config(background='red', state=tk.DISABLED)
btn_remove_harvest.bind('<ButtonRelease-1>', lambda event: remove_from_harvestable(event, table1, table2, value1))

btn_edit_max_qty = tk.Button(button_bar2, text='Edit Max Qty')
btn_edit_max_qty.pack(side='right', padx=10, pady=10)
btn_edit_max_qty.config(background=blue_foreground_color)
btn_edit_max_qty.bind('<ButtonRelease-1>', lambda event: edit_max_qty(event, table1))

# init_button(btn_print, "", "right")

# TABLE 2 ************************************************************

table_frame2 = tk.Frame(right_frame)
table_frame2.pack(fill='x')
table_frame2.config(background=background_color)

# create table1 label
table_label2 = tk.Label(table_frame2, text='All Parts')
table_label2.pack(side='left', padx=10, pady=5)
table_label2.config(background=background_color, foreground=blue_foreground_color, font=('Arial', 16, 'bold'))

# create a variable for the search box in the parts table 
parts_search_var2 = tk.StringVar()

# create search box for the table
parts_search_box2 = tk.Entry(table_frame2, textvariable=parts_search_var2, borderwidth=10, relief=tk.FLAT)
parts_search_box2.pack(side='right', padx=10, pady=10)
parts_search_box2.config(background='#5c596b', foreground='#ffffff', font=('Arial', 12, 'bold'))
parts_search_box2.bind('<FocusIn>', lambda event: on_search_box_focus_in(event, parts_search_box))
parts_search_box2.bind('<FocusOut>', lambda event: on_search_box_focus_out(event, parts_search_box))

# Call the search_and_update_treeview function every time the parts_search_var2 value changes
parts_search_var2.trace("w", search_and_update_treeview)

# parts_search_box.bind('<Return>', lambda event: search_all_parts(event, listbox, parts_search_box2))
# parts_search_var2.trace("w", lambda name, index, mode: search_all_parts())

table2 = ttk.Treeview(right_frame, columns=table_columns, show='headings')
for column in table_columns:
    table2.heading(column, text=column)
table2.pack(padx=10, pady=10, fill='both', expand=True)

table2.column("Type", width=120, anchor="center")
table2.column("SKU", width=100, anchor="center")
table2.column("Description", width=300)
table2.column("Qty", width=60, anchor="center")
table2.column("Max Qty", width=80, anchor="center")
table2.bind('<Double-1>', lambda event: on_double_click(event, table2))
table2.bind('<<TreeviewSelect>>', lambda event: update_button_state(table2, btn_add_to_harvest))

# # create table1 label
# table_label2 = tk.Label(right_frame, text='Search All Parts')
# table_label2.pack(side='left', padx=10, pady=5)
# table_label2.config(background=background_color, foreground=blue_foreground_color, font=('Arial', 16, 'bold'))

# # create table1
# table2 = ttk.Treeview(right_frame, columns=table_columns, show='headings')
# for column in table_columns:
#     table2.heading(column, text=column)
# table2.pack(padx=10, pady=10, fill='both', expand=True)



show_splash_and_fetch_data(root, listbox)
root.mainloop()