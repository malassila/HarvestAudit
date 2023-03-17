import tkinter as tk

background_color = '#26242f'
button_background_color = '#545166'
white_foreground_color = '#ffffff'
blue_foreground_color = '#6da7d2'
highlight_color = '#bfd660'

def on_enter(event, button, selected_button):
    # if button is not selected_button
    if button != selected_button:
        button.config(relief=tk.RAISED, cursor='hand2', fg='#413f4a', bg=highlight_color)

def on_leave(event, button, selected_button):
    # if button is not selected_button
    if button != selected_button:
        button.config(relief=tk.SUNKEN, cursor='hand2', fg=white_foreground_color, bg=background_color)


def on_search_box_focus_in(event, search_box):
    search_box.config(bg='#ffffff', fg='black')

def on_search_box_focus_out(event, search_box):
    search_box.config(bg='#5c596b', fg=white_foreground_color)
    
def on_widget_enter(event):
    event.widget.config(cursor="hand2")

def on_widget_leave(event):
    event.widget.config(cursor="")

def on_hover(event, widget):
    event.widget.config()