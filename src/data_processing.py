""" Script data_processing.py """

"""
Functions for loading, processing, and saving data from CSV files exported by QuPath.

Confocal Microscopy Unit - CNIO : BioImage & Data Analysis
Developer: María Calvo de Mora
Last Update: April 2025
"""

import os
import pandas as pd

def process_csv_file(input_path, output_path):
    """
    Loads a CSV file, processes it, and saves the result.

    Args:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to save the processed CSV file.
    """
    # Load CSV with tab separator
    try:
        df = pd.read_csv(input_path, sep='\t', thousands=',')
    except Exception as e:
        print(f"Error loading {input_path}: {e}")
        return

    ### PROCESSING AREA
    ## Create a 'Cell Group' to assign detections to their corresponding cell
    df['Cell_Group'] = (df['Object type'] == 'Cell').cumsum() # Create a cumulative sum to assign a unique group number to each cell

    ## Calculations
    # Detect the columns for area and intensity of spots
    area_col = next((col for col in df.columns if 'Subcellular' in col and 'Area' in col), None)
    intensity_col = next((col for col in df.columns if 'Subcellular' in col and 'Mean channel intensity' in col), None)

    if not area_col or not intensity_col:
        print(f"Error: Area or Intensity columns not found in {input_path}.")
        return

    # Iterate over each unique Cell_Group (i.e., each cell)
    for cell_group in df['Cell_Group'].unique():
        # Filter rows for the current cell
        cell_data = df[df['Cell_Group'] == cell_group]
        # Filter only the 'Detection' rows for the current cell
        detection_data = cell_data[cell_data['Object type'] == 'Detection']

        # Calculations for the detections of the current cell
        if not detection_data.empty: # Only calculate if there are detections

            ## First calculation: calculate Sum intensity of each spot= mean intensity*area
            # Create the new column name based on the area column name
            base_name = area_col.rsplit(':', 1)[0]  # Get everything up to the last ':'
            new_column_name = f"{base_name}: Integrated density"  # Concatenate ": Integrated density" to the base name
            # Calculate Area * Mean Intensity for detections of the current cell
            detection_data[new_column_name] = detection_data[area_col] * detection_data[intensity_col]
            # Update the original DataFrame with the calculated values for the current cell
            df.loc[detection_data.index, new_column_name] = detection_data[new_column_name]

            ## Second calculation: Mean per nuclei of sum intensity
            # Sum all the 'Integrated density' values for the current cell and divide by the number of detections
            mean_integrated_density = detection_data[new_column_name].mean()
            # Create a new column for the mean value per cell (subcellular cluster: channel 3)
            mean_column_name = f"{base_name}: Integrated density - mean per cell"
            # Paste the mean value in the corresponding cell (only in the Cell row)
            df.loc[cell_data.index[0], mean_column_name] = mean_integrated_density

            ## Thrid calculation: Mean per nuclei of sum intensity*number of foci
            # Detect the column for number of foci
            num_spots_col = next((col for col in df.columns if 'Subcellular' in col and 'Num spots estimated' in col), None)
            if not num_spots_col:
                print(f"Error: Num spots estimated column not found in {input_path}.")
                return
            # Create the new column name for the calculation (mean per cell * number of foci)
            new_column_name_foci = f"{base_name}: Integrated density*number of foci - mean per cell"
            # Multiply the mean integrated density by the number of spots
            df.loc[cell_data.index[0], new_column_name_foci] = mean_integrated_density * cell_data[num_spots_col].iloc[0]

            ## Fourth calculation: Mean per nuclei of mean intensity 
            # Create the new column name for the mean intensity per cell
            mean_intensity_column_name = f"{base_name}: Mean intensity - mean per cell"
            # Calculate the mean intensity for the current cell
            mean_intensity = detection_data[intensity_col].mean()
            # Paste the mean value in the corresponding cell (only in the Cell row)
            df.loc[cell_data.index[0], mean_intensity_column_name] = mean_intensity

            ## Fifth calculation: Mean per nuclei of max intensity
            # Detect the column for max intensity
            max_intensity = next((col for col in df.columns if 'ROI' in col and 'Max' in col), None)
            if not max_intensity:
                print(f"Error: Max intensity column not found in {input_path}.")
                return
            # Create the new column name for the max intensity per cell
            max_intensity_column_name = f"{base_name}: Max intensity - mean per cell"
            # Calculate the mean max intensity for the current cell
            mean_max_intensity = detection_data[max_intensity].mean()
            # Paste the mean value in the corresponding cell (only in the Cell row)
            df.loc[cell_data.index[0], max_intensity_column_name] = mean_max_intensity

            ## Sixth calculation: Mean per nuclei of max intensity*number of foci
            # Create the new column name for the max intensity per cell
            max_intensity_column_name_foci = f"{base_name}: Max intensity*number of foci - mean per cell"
            # Multiply the mean max intensity by the number of spots
            df.loc[cell_data.index[0], max_intensity_column_name_foci] = mean_max_intensity * cell_data[num_spots_col].iloc[0]
   
    # Save processed CSV
    try:
        df.to_csv(output_path, sep='\t', index=False)
        print(f"Processed file saved: {output_path}")
    except Exception as e:
        print(f"Error saving {output_path}: {e}")
