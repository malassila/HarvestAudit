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
    
def on_widget_enter(event, widget2=None, widget3=None, widget4=None):
    try:
        event.widget.config(cursor="hand2")
        event.widget.config(relief=tk.RAISED)
        event.widget.config(bg="#3c3a43")
        widget2.config(bg="#3c3a43")
        widget3.config(bg="#3c3a43")
        widget4.config(bg="#3c3a43")
    except Exception as e:
        print(e)

def on_widget_leave(event, widget2=None, widget3=None, widget4=None):
    try:
        event.widget.config(cursor="")
        event.widget.config(relief=tk.SUNKEN)
        event.widget.config(bg=background_color)
        widget2.config(bg=background_color)
        widget3.config(bg=background_color)
        widget4.config(bg=background_color)
    except Exception as e:
        print(e)

def on_hover(event, widget):
    event.widget.config()