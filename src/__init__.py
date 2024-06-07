import tkinter
import customtkinter
from tkcalendar import DateEntry
import datetime

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("800x600")
app.title("Deleware North Take Home Assignment")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Deleware North Take Home Assignment", font=("Arial", 24))
title.pack(pady=10)

# Create a new frame for the DateEntry widgets
date_frame = tkinter.Frame(app)
date_frame.pack(pady=10)

# Create StringVar variables for the DateEntry widgets
from_date_var = tkinter.StringVar()
to_date_var = tkinter.StringVar()

# Function to update to_date_input when from_date_input changes
def update_to_date(*args):
    from_date_str = from_date_var.get()
    if not from_date_str:  # If from_date_str is an empty string, return immediately
        return
    from_date = datetime.datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = from_date + datetime.timedelta(days=7)
    to_date_var.set(to_date.strftime('%Y-%m-%d'))

# Trace changes to from_date_var
from_date_var.trace("w", update_to_date)

# Adding a date from input
from_date_input = DateEntry(date_frame, date_pattern='y-mm-dd', textvariable=from_date_var)
from_date_input.grid(row=0, column=0, padx=20, sticky='w')

# Adding a date to input
to_date_input = DateEntry(date_frame, date_pattern='y-mm-dd', textvariable=to_date_var, state='disabled')
to_date_input.grid(row=0, column=1, padx=20, sticky='w')

# Run App
app.mainloop()
