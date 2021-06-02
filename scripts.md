
## Create Random Raster

This script is used to generate random raster data that can be used for testing purposes. The script takes in user input for the area the user wants to find debris for. It then uses the Arcpy library to generate raster data.   
Returns:   
- raster with random values between 0 and 1, exclusive. 

## Determine Debris VOlume

Tool to determine the volume of debris in a given area

Takes in:
 - Raster layer with debris spread data - where value of a cell equates to the volume of debris in that area of the map
 - The polygon area over which the user wants to calculate the total debris volume

Returns:
 - The total volume of debris, in appropriate units, printed to the output of the script in arcGIS Pro

## Determine Clearance Time

Tool to determine the total time to clear a given area of debris.The script reads in a given raster layer to determine the debris amount, and uses user-supplied material variables to estimate the time it would take to clean a certain area.  
Takes in: 
 - Debris Raster Layer
 - The polygon area over which the user wants to clear debris
 - The distance from the debris site to the dump site
 - Specific details about number of debris loaders, number of trucks per loader, velocities, maximum loads, and times
  
Returns:
 - The total volume of debris, in appropriate units, printed to the output of the script in arcGIS Pro
 - The total time required to clear the area of debris, given the parameters
