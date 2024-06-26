import os

import pandas as pd
import requests
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import tkinter
from tkinter import ttk
import customtkinter
import datetime
from tkcalendar import DateEntry
from datetime import datetime, timedelta

from src.controller.pcr_testing import get_data
from src.service import process_data
from tkinter.scrolledtext import ScrolledText


# This function will check and update the data from the cdc website
def check_and_update_data():
    # Define the directory and file name
    directory = "src/json"
    file_name = "/pcr_testing_data_download.json"

    # Join the directory and file name to get the full file path
    file_path = os.path.join(directory, file_name)

    df = None  # Initialize the DataFrame

    # Check if the file exists
    if os.path.isfile(file_path):
        # Get the file's modification time
        mod_time = os.path.getmtime(file_path)
        mod_time = datetime.fromtimestamp(mod_time)

        # Get the current time
        current_time = datetime.now()

        # If the file is more than 7 days old, update the data
        if current_time - mod_time > timedelta(days=7):
            df, status_code = get_data()

    else:
        # If the file does not exist, update the data
        df, status_code = get_data()

    return df  # Return the DataFrame


if __name__ == "__main__":
    # Call the function at the start of your application
    df = check_and_update_data()

    # System Settings
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_tests_text = None
        self.tree_title = None
        self.tree = None
        self.scrollbar = None
        self.rolling_average_text = None

    def on_submit(self):
        # Destroy existing widgets if they exist
        for widget in [self.total_tests_text, self.tree_title, self.tree, self.scrollbar, self.rolling_average_text]:
            if widget:
                widget.destroy()

        # Get the date strings from the DateEntry widgets
        from_date_str = from_date_input.get()

        # Get the total number of tests performed up to the provided date
        total_tests = process_data.calculate_total_tests(from_date_str, df)

        # Get the rolling average of new results reported for the provided date
        rolling_average = process_data.calculate_rolling_average(from_date_str, df)
        rolling_average['7_day_average'] = rolling_average['7_day_average'].round(2)

        # calculate the top ten states with the highest number of new results reported
        top_states = process_data.calculate_positivity_rate(from_date_str, df)
        top_states['positivity_rate'] = top_states['positivity_rate'] * 100
        top_states.rename(columns={'positivity_rate': 'positivity_rate (%)'}, inplace=True)

        # Convert the DataFrames to strings with columns aligned
        total_tests_str = format(total_tests, ',')
        rolling_average_str = rolling_average.to_string(justify='justify')
        top_states_str = top_states.to_string(justify='justify')

        index_list = pd.to_datetime(rolling_average.iloc[:, 2]).tolist()
        values_list = rolling_average.iloc[:, 3].tolist()

        # Create a scatter plot for the rolling_average
        plt.figure(figsize=(13, 9))
        plt.scatter(index_list, values_list)
        plt.title('Rolling Average of New Results Reported')
        plt.xlabel('Date')
        plt.ylabel('Rolling Average')
        date_format = mdates.DateFormatter('%d-%m')
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.grid(True)
        plt.savefig('rolling_average_scatter_plot.png')

        # Create a markdown file and write the data to it
        with open('Metric and Documentation Output.md', 'w') as f:
            f.write("## Metric Documentation\n\n")
            f.write("### Total Tests Performed\n\n")
            f.write("This metric represents the total number of tests performed up to the provided date.\n\n")
            f.write("### Rolling Average of New Results Reported\n\n")
            f.write("This metric represents the 7-day rolling average of new results reported for the provided date. "
                    "It calculates the average number of new cases reported per day for the last 7 days, for each day in the last 30 days.\n\n")
            f.write("### Top Ten States with the Highest Number of New Results Reported\n\n")
            f.write(
                "This metric represents the top ten states with the highest number of new results reported for the provided date. The positivity rate is displayed as a percentage.\n\n")
            f.write(f"# Total Tests Performed as of yesterday - Date(2024-06-13): \n\n{total_tests_str}\n\n")
            f.write(
                f"# Rolling Average of New Results Reported - Date(2024-06-13):\n\n```\n{rolling_average_str}\n```\n\n")
            f.write("![Rolling Average of New Results Reported](rolling_average_scatter_plot.png)\n\n")
            f.write(f"# Top Ten States with the Highest Number of New Results Reported - Date(2024-06-13):\n\n```\n{top_states_str}\n```\n\n")

        # Create CTkText widgets to display the results
        self.total_tests_text = customtkinter.CTkTextbox(self, height=30, width=550)
        self.total_tests_text.insert('end', f"Total Tests Performed as of yesterday: {total_tests_str}")
        self.total_tests_text.pack(pady=10)

        # Convert the DataFrame to a list of lists
        top_states_list = top_states.values.tolist()

        # Create a label for the Treeview widget
        self.tree_title = tkinter.Label(self, text="Top Ten States with the Highest Number of New Results Reported:",
                                        font=("Arial", 10))
        self.tree_title.pack(pady=10)

        # Create a Treeview widget
        self.tree = ttk.Treeview(self)

        # Define the columns
        self.tree["columns"] = top_states.columns.tolist()

        # Format the columns
        for column in self.tree["columns"]:
            self.tree.column(column, anchor="center")
            self.tree.heading(column, text=column, anchor="center")

        # Insert data into the Treeview widget
        for state_data in top_states_list:
            self.tree.insert("", "end", values=state_data)

        # Pack the Treeview widget into the window
        self.tree.pack(pady=10)

        # Create a Scrollbar widget
        self.scrollbar = tkinter.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')

        # Convert the DataFrame to a string with columns centered
        rolling_average_str = rolling_average.to_string(justify='center')
        self.rolling_average_text = tkinter.Text(self, height=150, width=350, yscrollcommand=self.scrollbar.set)
        self.rolling_average_text.tag_configure('center', justify='center')
        self.rolling_average_text.insert('end', f"Rolling Average of New Results Reported:\n\n{rolling_average_str}",
                                         'center')
        self.rolling_average_text.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        self.scrollbar.config(command=self.rolling_average_text.yview)




# Our app frame
app = App()
app.geometry("1200x800")
app.title("Deleware North Take Home Assignment")


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
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = from_date + timedelta(days=7)
    to_date_var.set(to_date.strftime('%Y-%m-%d'))


# Trace changes to from_date_var
from_date_var.trace("w", update_to_date)

# Create a label for the DateEntry widget
date_label = tkinter.Label(date_frame, text="Select the date for the report results: ")
date_label.grid(row=0, column=0, padx=20, sticky='w')

# Adding a date from input
from_date_input = DateEntry(date_frame, date_pattern='y-mm-dd', textvariable=from_date_var)
from_date_input.grid(row=0, column=1, padx=20, sticky='w')

# # Adding a date to input
# to_date_input = DateEntry(date_frame, date_pattern='y-mm-dd', textvariable=to_date_var, state='disabled')
# to_date_input.grid(row=0, column=1, padx=20, sticky='w')


# Button for submitting the dates
submit_button = customtkinter.CTkButton(app, text="Submit", command=app.on_submit)
submit_button.pack(pady=10)

# Run App
app.mainloop()
