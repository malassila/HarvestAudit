import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Constants
background_color = '#26242f'
blue_foreground_color = '#2f2d38'
white_foreground_color = '#ffffff'
highlight_color = '#bfd660'

# Define icon path and names
icon_path = "C:\\HarvestAudit\\images\\icon\\"
icon_names = ['motherboard', 'power supply', 'heatsink', 'fan', 'case component', 'backplane']

# Create main window
root = tk.Tk()
root.geometry("1200x750")
root.title("Harvest Tool")
root.configure(background=background_color)
root.state("zoomed")

# Create left navigation frame
left_frame = tk.Frame(root, bg=background_color, width=300)
left_frame.pack(side='left', fill='y')

# Create logo image
image_frame = tk.Frame(left_frame, bg=background_color)
image_frame.pack(side='top', fill='x')

pcsp_logo_path = "C:\\HarvestAudit\\images\\Logo\\PCSP_Light.png"
pcsp_logo = Image.open(pcsp_logo_path).resize((96, 64), Image.ANTIALIAS)
pcsp_logo = ImageTk.PhotoImage(pcsp_logo)

canvas = tk.Canvas(image_frame, width=96, height=64, bg=background_color, highlightthickness=0)
canvas.pack(side='left')
canvas.create_image(0, 0, anchor=tk.NW, image=pcsp_logo)

# Create button bar for server, workstation, and other buttons
button_bar1 = tk.Frame(left_frame, bg=background_color)
button_bar1.pack(side='top')
server_button = tk.Button(button_bar1, text='Server')
ws_button = tk.Button(button_bar1, text='Workstation')
other_button = tk.Button(button_bar1, text='Other')
init_button(other_button, 'server', 'left')
init_button(server_button, 'workstation', 'left')
init_button(ws_button, 'other', 'left')

# Create button bar for refresh and search buttons
button_bar_utils = tk.Frame(left_frame, bg=background_color)
button_bar_utils.pack(side='top')
refresh_button = tk.Button(button_bar_utils, text="Refresh", command=lambda: fetch_data(listbox))
search_sku_button = tk.Button(button_bar_utils, text="Search SKU", command=lambda: fetch_sku(search_box, listbox))
init_button(refresh_button, 'server', 'left')
init_button(search_sku_button, 'workstation', 'left')

# Create search box
search_var = tk.StringVar()
search_var.trace("w", lambda name, index, mode: on_search_box_change())
search_box = tk.Entry(left_frame, textvariable=search_var, borderwidth=10, relief=tk.FLAT)
search_box.pack(fill='x', padx=10, pady=10)
search_box.config(background='#5c596b', foreground='#ffffff', font=('Arial', 12, 'bold'))

# Create listbox for chassis
original_items = []
listbox = tk.Listbox(left_frame)
listbox.pack(padx=10, pady=10, fill='both', expand=True)
listbox.configure(background=background_color, foreground=white_foreground_color, bd=0, font=('Arial', 12, 'bold'), selectbackground=highlight_color, selectforeground='black', highlightcolor=background_color, borderwidth=10, relief=tk.FLAT)

# Create right frame
right_frame = tk.Frame(root, bg=background_color)
right_frame.grid(row=0, column=0, sticky="nsew")
right_frame.columnconfigure(0, weight=
