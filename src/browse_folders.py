""" Script browse_folders.py """

"""
Utility functions for selecting input and output directories using a GUI window.

Confocal Microscopy Unit - CNIO : BioImage & Data Analysis
Developer: María Calvo de Mora
Last Update April 2025
"""

import tkinter as tk
from tkinter import filedialog

def select_folders():
    """
    Opens a window for the user to select input and output folders.

    Returns:
        tuple: (input_folder_path, output_folder_path)
    """
    def browse_input():
        path = filedialog.askdirectory(title="Select Input Folder")
        if path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, path)

    def browse_output():
        path = filedialog.askdirectory(title="Select Output Folder")
        if path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, path)

    def submit():
        nonlocal input_path, output_path
        input_path = input_entry.get()
        output_path = output_entry.get()
        window.destroy()

    # Create the main window
    window = tk.Tk()
    window.title("Select Input and Output Folders")

    # Input directory
    input_label = tk.Label(window, text="Input Directory:")
    input_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    input_entry = tk.Entry(window, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=10)

    input_browse_button = tk.Button(window, text="Browse", command=browse_input)
    input_browse_button.grid(row=0, column=2, padx=10, pady=10)

    # Output directory
    output_label = tk.Label(window, text="Output Directory:")
    output_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    output_entry = tk.Entry(window, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=10)

    output_browse_button = tk.Button(window, text="Browse", command=browse_output)
    output_browse_button.grid(row=1, column=2, padx=10, pady=10)

    # Submit button
    submit_button = tk.Button(window, text="Continue", command=submit)
    submit_button.grid(row=2, column=1, pady=20)

    # Run the window
    input_path = ""
    output_path = ""
    window.mainloop()

    return input_path, output_path
