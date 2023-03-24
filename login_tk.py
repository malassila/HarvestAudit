from tkinter import *

# Create the login_window window
login_window = Tk()
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

# Create login button
login_button = Button(right_frame, text="Login", font=("Helvetica", 14), bg="#26242f", fg="#ffffff", padx=20, pady=10)
login_button.pack(pady=20)
login_button.config(cursor="hand2", relief=FLAT, background="#FFFFFF", foreground="#26242f", height=1)

# Run the main loop
login_window.mainloop()
