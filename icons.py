import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

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

            print(f"Icon size: {icon.size}")

            self.icon = ImageTk.PhotoImage(icon)

            # Create a canvas for the image
            canvas = tk.Canvas(icon_frame, width=50, height=50, bg='#26242f', highlightthickness=0)
            canvas.pack(side='left')
            canvas.create_image(0, 0, anchor=tk.NW, image=self.icon)
        except Exception as e:
            print("Error adding icon: " + str(e))

        
def add_motherboard_icon(icon_frame): # return the canvas with the icon
    try:
        icon_path = "C:\\HarvestAudit\\images\\icon\\motherboard.png"
        motherboard_icon = Image.open(icon_path)
        icon = motherboard_icon.resize((150, 150), Image.ANTIALIAS)

        icon = ImageTk.PhotoImage(icon)
            
        # Create a canvas for the image
        canvas = tk.Canvas(icon_frame, width=50, height=50, bg='#26242f', highlightthickness=0)
        canvas.pack(side='left')
        canvas.create_image(0, 0, anchor=tk.NW, image=icon)

    except Exception as e:
        print("Error adding icon: " + str(e))

def add_power_supply_icon(icon_frame): # return the canvas with the icon
    try:
        icon_path = "C:\\HarvestAudit\\images\\icon\\power-supply.png"
        power_supply_icon = Image.open(icon_path)
        icon = power_supply_icon.resize((50, 50), Image.ANTIALIAS)

        icon = ImageTk.PhotoImage(icon)
            
        # Create a canvas for the image
        canvas = tk.Canvas(icon_frame, width=150, height=150, bg='#26242f', highlightthickness=0)
        canvas.pack(side='left')
        canvas.create_image(0, 0, anchor=tk.NW, image=icon)

    except Exception as e:
        print("Error adding icon: " + str(e))

def add_heatsink_icon(icon_frame): # return the canvas with the icon
    try:
        icon_path = "C:\\HarvestAudit\\images\\icon\\heatsink.png"
        heatsink_icon = Image.open(icon_path)
        icon = heatsink_icon.resize((50, 50), Image.ANTIALIAS)

        icon = ImageTk.PhotoImage(icon)
            
        # Create a canvas for the image
        canvas = tk.Canvas(icon_frame, width=150, height=150, bg='#26242f', highlightthickness=0)
        canvas.pack(side='left')
        canvas.create_image(0, 0, anchor=tk.NW, image=icon)

    except Exception as e:
        print("Error adding icon: " + str(e))
        
def add_fan_icon(icon_frame): # return the canvas with the icon
    try:
        icon_path = "C:\\HarvestAudit\\images\\icon\\cooling-fan.png"
        fan_icon = Image.open(icon_path)
        icon = fan_icon.resize((50, 50), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
            
        # Create a canvas for the image
        canvas = tk.Canvas(icon_frame, width=150, height=150, bg='#26242f', highlightthickness=0)
        canvas.pack(side='left')
        canvas.create_image(0, 0, anchor=tk.NW, image=icon)

    except Exception as e:
        print("Error adding icon: " + str(e))
        
def add_case_component_icon(icon_frame): # return the canvas with the icon
    try:
        icon_path = "C:\\HarvestAudit\\images\\icon\\component.png"
        case_component_icon = Image.open(icon_path)
        icon = case_component_icon.resize((50, 50), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
            
        # Create a canvas for the image
        canvas = tk.Canvas(icon_frame, width=150, height=150, bg='#26242f', highlightthickness=0)
        canvas.pack(side='left')
        canvas.create_image(0, 0, anchor=tk.NW, image=icon)

    except Exception as e:
        print("Error adding icon: " + str(e))
        
def add_backplane_icon(icon_frame): # return the canvas with the icon
    try:
        icon_path = "C:\\HarvestAudit\\images\\icon\\backplane.png"
        backplane_icon = Image.open(icon_path)
        icon = backplane_icon.resize((50, 50), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
            
        # Create a canvas for the image
        canvas = tk.Canvas(icon_frame, width=150, height=150, bg='#26242f', highlightthickness=0)
        canvas.pack(side='left')
        canvas.create_image(0, 0, anchor=tk.NW, image=icon)

    except Exception as e:
        print("Error adding icon: " + str(e))
