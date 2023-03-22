

def toggle_parts_frame(frame, button_text, table2, btn_add, btn_remove, btn_max_qty, icon_frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        table2.pack_forget()
        icon_frame.pack_forget()
        btn_add.pack_forget()
        btn_remove.pack_forget()
        btn_max_qty.pack_forget()
        button_text.set("Show Parts")
    else:
        icon_frame.pack(side='top', fill='x')
        frame.pack(fill='x')
        table2.pack(padx=10, pady=10, fill='both', expand=True)
        btn_add.pack(side='right', padx=10, pady=10)
        btn_remove.pack(side='right', padx=10, pady=10)
        btn_max_qty.pack(side='right', padx=10, pady=10)
        button_text.set("Hide Parts")

def toggle_icon_frame(frame, button_text, table1, btn_add, btn_remove, btn_max_qty):
    if frame.winfo_ismapped():
        frame.pack_forget()
        table1.pack_forget()
        btn_add.pack_forget()
        btn_remove.pack_forget()
        btn_max_qty.pack_forget()
        button_text.set("Show Icons")
    else:
        frame.pack(fill='x')
        table1.pack(padx=10, pady=10, fill='both', expand=True)
        btn_add.pack(side='right', padx=10, pady=10)
        btn_remove.pack(side='right', padx=10, pady=10)
        btn_max_qty.pack(side='right', padx=10, pady=10)
        button_text.set("Hide Icons")