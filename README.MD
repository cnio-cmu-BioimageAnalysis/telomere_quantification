# processTelomereSegmentation

This Python script processes the output CSV files from QuPath telomere segmentation. It calculates several new features related to telomere intensity per nucleus and saves the results into a specified output directory.

## Download processTelomereSegmentation code

1. Go to the GitHub repository `processTelomereSegmentation`
2. Click on `<> Code` > `Download ZIP`
   
<p align="center">
    <img width="700" height="350" src="images/code.png">
</p>

3. The downloaded repo will be found in the Downloads directory of your computer.

## Setting up the environment

1. Open a terminal or Anaconda Prompt.

    **TIP**: In the Microscopy Unit, we usually work with Miniforge. There is already a preconfigured environment to run this code. Most workstations have a shortcut to open the Miniforge Prompt directly.
    Make sure that the window title says something like:

    <p align="center">
    <img width="50" height="50" src="images/miniforge_simbol.png">
    </p>

    <p align="center">
    <img width="700" height="350" src="images/miniforge.png">
    </p>

   **TELOMERES AND TELOMERASE GROUP**: In the analysis computer of your Group there is already an specific environment created. In order to use it open the Ubuntu terminal (type on the search bar: Ubuntu).

2. Activate the conda environment (or the environment where your required packages are installed).  
If you used Anaconda to install Cellpose, you can activate it by typing:

```bash
conda activate cellpose
```

**Note**: If you installed the dependencies in a different environment, make sure to activate the correct one.

**TELOMERES AND TELOMERASE GROUP**: On the Ubuntu terminal type:
```bash
conda activate telomere_quantification
```

## Running the script

1. Navigate to the location where you downloaded the repository and **inside the src folder in the repository**:

```bash
cd path/to/telomere_quantification/src
```
**TELOMERES AND TELOMERASE GROUP**: After downlowing the code and if you have in the Downloads folder of your computer type:
```bash
cd /mnt/c/Users/analysisuser/Downloads/telomere_quantification-main/telomere_quantification-main/src
```

2. Run the main Python script:

```bash
python main.py
```

3. A GUI will pop up asking you to select:
   - **Input directory**: The folder where your QuPath telomere segmentation CSV files are stored.

        **CAUTION**: The **input directory must contain only the .csv files you want to process**.Do **not** include any other files in that folder, as the script assumes all files ending in .csv are valid inputs and will attempt to process them. 

        **TELOMERES AND TELOMERASE GROUP**: Do not have blank spaces in the paths/folders. For the input path you should always put at the beginning: /mnt/c/Users/analysisuser/. After that you should put the Windows path where you have created the QuPath output folder. It is recommended to put it always on the desktop for            simplicity. If so, you would put:/mnt/c/Users/analysisuser/Desktop/QuPath_project/output
   
   - **Output directory**: The folder where the processed CSV files with the new calculated features will be saved.

      **TELOMERES AND TELOMERASE GROUP**: Do not have blank spaces in the paths/folders. As for the input path you should always put at the beginning: /mnt/c/Users/analysisuser/. After that you should put the Windows path where you have created the Python output folder. It is recommended to put it always on the desktop               for simplicity. If so, you would put:/mnt/c/Users/analysisuser/Desktop/output_python

4. After selecting the directories, the script will start processing each file.
When the processing finishes, you will see a message in the terminal for each file like:
    ```bash
    Processed file saved at: [path_to_file]_processed.csv
    ```
    This confirms that the file was successfully processed and saved.
    Each processed file keeps its original name with the suffix _processed added.

5. Once the script finishes, you will find the processed CSV files in your selected output directory.  
Each output CSV will include the following new calculated columns:

| Column name | Description |
| :---------- | :----------- |
| `Integrated density` | Sum intensity of each spot = mean intensity × area |
| `Integrated density - mean per cell` | Mean per nucleus of sum intensity |
| `Integrated density*number of foci - mean per cell` | Mean per nucleus of sum intensity × number of foci |
| `Mean intensity - mean per cell` | Mean per nucleus of mean intensity |
| `Max intensity - mean per cell` | Mean per nucleus of max intensity |
| `Max intensity*number of foci - mean per cell` | Mean per nucleus of max intensity × number of foci |

6. You can now use the processed data for further analysis!

# QuPath analysis script

This script is located inside the `src/qupath_analysis_script` folder in the repository. It will segment the nuclei of the cells with Cellpose deep learning models, using Channel 1(DAPI). After this step, it will segment, with a threshold-based algorithm, the spots (telomeres). If you have 2 channels and telomeres are in Channel 2, choose `2D_nuclei_trf1_spots_2_channels.groovy` script. If you have 3 channels and telomeres are in Channel 3, choose `2D_nuclei_intensity_green_trf1_spots_3_channels.groovy` script. Then, it will calculate Max and Min intensities for each spot. And finally, it will export all measurements as a tab-separated csv file per image. You must create previously a folder named `output` inside QuPath project's folder so that data can be exported. If you want a per-cell summary of the spot measurements, you will have to run the python script mentioned above, to process all the csv files that QuPath generates. Before running this script, please create a folder named "output" at the same level as the QuPath project files.

