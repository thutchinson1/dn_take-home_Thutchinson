import os
import time
import tkinter
import customtkinter
import datetime
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from src.controller.pcr_testing import get_data
from src.service import read_json_data
from src.service import process_data

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("800x600")
app.title("Deleware North Take Home Assignment")


# This function will check and update the data from the cdc website
def check_and_update_data():
    # Define the path to the JSON file
    file_path = "../json/pcr_testing_data_download.json"

    # Check if the file exists
    if os.path.isfile(file_path):
        # Get the file's modification time
        mod_time = os.path.getmtime(file_path)
        mod_time = datetime.fromtimestamp(mod_time)

        # Get the current time
        current_time = datetime.now()

        # If the file is more than 7 days old, update the data
        if current_time - mod_time > timedelta(days=7):
            get_data()
    else:
        # If the file does not exist, update the data
        get_data()


# Call the function at the start of your application
check_and_update_data()


# Define a function to close the window
def on_closing():
    # Destroy the window
    app.destroy()


# Set the protocol for the window closing event
app.protocol("WM_DELETE_WINDOW", on_closing)

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


def on_submit():
    # Get the total number of tests performed up to the provided date
    total_tests = process_data.calculate_total_tests(from_date_input)

    # Get the rolling average of new results reported for the provided date
    rolling_average = process_data.calculate_rolling_average(from_date_input)

    # calculate the top ten states with the highest number of new results reported
    top_states = process_data.calculate_positivity_rate(from_date_input)

    # Print the results in a readable format
    print("\nTotal Tests Performed:")
    print(total_tests)
    print("\nRolling Average of New Results Reported:")
    print(rolling_average)
    print("\nTop Ten States with the Highest Number of New Results Reported:")
    print(top_states)


# Button for submitting the dates
submit_button = customtkinter.CTkButton(app, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Run App
app.mainloop()
