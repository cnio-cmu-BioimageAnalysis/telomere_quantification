""" Script main.py """

"""
Main script for loading, processing, and saving data.

This script loads and processes raw data exported from QuPath as CSV files and makes different calculations by calling other development scripts.

Confocal Microscopy Unit - CNIO : BioImage & Data Analysis
Developer: María Calvo de Mora
Last Update April 2025
"""

import os
import pandas as pd
from browse_folders import select_folders
from data_processing import *

def main():
    """
    Main function to execute the script.
    """
    # Get input and output folder paths
    input_folder, output_folder = select_folders()

    # Process and save each CSV file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Process the CSV file
            process_csv_file(input_path, output_path)

if __name__ == "__main__":
    main()
