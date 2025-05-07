//Before running this script, please create a folder named "output" at the same level as the QuPath project files
//This script will segment the nuclei of the cells with Cellpose deep learning models, using Channel 1(DAPI). After this step, it will segment, with a threshold-based algorithm, the spots (telomeres) on Channel 3.
//Then, it will calculate Max and Min intensities for each spot. And finally, it will export all measurements as a tab-separated csv file per image. If you want a per-cell summary of the spot measurements,
//you will have to run a python script to process all the csv files that QuPath generates. Get in contact with CMU staff if you do not know how to run it.

import qupath.lib.gui.scripting.QPEx
import qupath.ext.biop.cellpose.Cellpose2D

// Get the current image data
def imageData = QPEx.getCurrentImageData()
def server = imageData.getServer()
// Get the image name
def imageName = imageData.getServer().getMetadata().getName().replaceAll("/","")
// Get the project path
def projectPath =  QPEx.getProject().getPath()
// Get the pixel size in microns
def pixelSize = server.getPixelCalibration().getPixelWidthMicrons()

//Nuclei detection using Cellpose models
createFullImageAnnotation(true)
def pathModel = 'cyto3'
def cellpose = Cellpose2D.builder( pathModel )
        .pixelSize( pixelSize )                  // Resolution for detection in um
        .channels( 'Channel 1' )	               // Select detection channel(s)
//        .tempDirectory( new File( '/tmp' ) ) // Temporary directory to export images to. defaults to 'cellpose-temp' inside the QuPath Project
//        .preprocess( ImageOps.Filters.median( 1 ) )                // List of preprocessing ImageOps to run on the images before exporting them
//        .normalizePercentilesGlobal( 0.1, 99.8, 10 ) // Convenience global percentile normalization. arguments are percentileMin, percentileMax, dowsample.
//        .tileSize( 1024 )                  // If your GPU can take it, make larger tiles to process fewer of them. Useful for Omnipose
//        .cellposeChannels( 1,2 )           // Overwrites the logic of this plugin with these two values. These will be sent directly to --chan and --chan2
//        .cellprobThreshold( 0.0 )          // Threshold for the mask detection, defaults to 0.0
//        .flowThreshold( 0.4 )              // Threshold for the flows, defaults to 0.4
        .diameter( 10/pixelSize )                    // Median object diameter. Set to 0.0 for the `bact_omni` model or for automatic computation
//        .useOmnipose()                   // Use omnipose instead
//        .addParameter( "cluster" )         // Any parameter from cellpose or omnipose not available in the builder.
//        .addParameter( "save_flows" )      // Any parameter from cellpose or omnipose not available in the builder.
//        .addParameter( "anisotropy", "3" ) // Any parameter from cellpose or omnipose not available in the builder.
        .cellExpansion( 0.000001 )              // Approximate cells based upon nucleus expansion
//        .cellConstrainScale( 1.5 )         // Constrain cell expansion using nucleus size
//        .classify( "My Detections" )       // PathClass to give newly created objects
//        .measureShape()                  // Add shape measurements
        .measureIntensity()              // Add cell measurements (in all compartments)
//        .createAnnotations()             // Make annotations instead of detections. This ignores cellExpansion
//        .simplify( 0 )                     // Simplification 1.6 by default, set to 0 to get the cellpose masks as precisely as possible
        .build()

// Run detection for the selected objects
//def imageData = getCurrentImageData() already defined erarlie in the script
def pathObjects = getSelectedObjects() // To process only selected annotations, useful while testing
// def pathObjects = getAnnotationObjects() // To process all annotations. For working in batch mode
if (pathObjects.isEmpty()) {
    Dialogs.showErrorMessage( "Cellpose", "Please select a parent object!" )
    return
}

cellpose.detectObjects( imageData, pathObjects )

// You could do some post-processing here, e.g. to remove objects that are too small, but it is usually better to
// do this in a separate script so you can see the results before deleting anything.

println 'Cellpose detection script done'

//Spot detection of telomeres using QuPath subcellular detection on Channel 3. Adapt it to your specific channel and fine-tune your particular detection settings
runPlugin('qupath.imagej.detect.cells.SubcellularDetection', '{"detection[Channel 1]":-1.0,"detection[Channel 2]":-1.0,"detection[Channel 3]":6000.0,"doSmoothing":false,"splitByIntensity":true,"splitByShape":true,"spotSizeMicrons":0.2,"minSpotSizeMicrons":0.06,"maxSpotSizeMicrons":0.5,"includeClusters":true}')
selectDetections();
//Calculate Max and Min intensities for all cells and spots
runPlugin('qupath.lib.algorithms.IntensityFeaturesPlugin', '{"pixelSizeMicrons":0.0902,"region":"ROI","tileSizeMicrons":25.0,"channel1":false,"channel2":false,"channel3":true,"doMean":false,"doStdDev":false,"doMinMax":true,"doMedian":false,"doHaralick":false,"haralickMin":NaN,"haralickMax":NaN,"haralickDistance":1,"haralickBins":32}')
//Classification of cells in positive and negative according to their number of spots. Change the number below according to your preference. Above the number, the cell is classified as positive, and below as negative
setCellIntensityClassifications("Subcellular: Channel 3: Num spots estimated", 5)
//Save detection (cells and spots) measurements. They are saved as a tab-separated csv file per image, and you need to, previously to run the script, create a folder named "output" at the same level as the QuPath project files
saveDetectionMeasurements(projectPath.toString().replaceAll("project.qpproj","output")+File.separator+imageName.toString()+'_table_resutls.csv')