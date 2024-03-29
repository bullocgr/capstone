"""
Tool:               Determine debris volume of a given area
Source Name:        DetermineDebrisVolume.PY
ArcGIS Version:     2.6.0
Required Arguments: Area Polygon to Clear:
                        The area polygon to clear is the polygon the user drew in ArcGIS Pro. This area should represent the area the user wants to clear of debris
                    Debris Raster:
                        The debris raster is the file generated by the CreateRandomRaster script for this example. It should be a rasterized dataset as a .tif file. The data should represent debris spread.
                    Number of Loaders:
                        This is the number of loaders the user will have to clean up the given area.
                    Number of Trucker per Loader:
                        This is how many trucks the user will have assigned to each loader.
                    Distance to Dump Site:
                        This is the distance to the dump site from the main loading point within the polygon.

Optional Arguments: Volume Per Truck (cubic yards): Default set to 30 cubic yards. This is how much debris each truck can carry.
                    Weight Per Truck (tons): Default set to 20 tons. This is how much weight each truck can carry.
                    Efficiency Factor (decimal): Default set to 83%. This is how effecient the loaders are. 
                    Work Day Length (hours): Default set to 8 hours. This is how long each work day is.
                    Truck Speed Loaded (miles per hour): Default is set to 25 mph. This is how quickly each truck is loaded with debris.
                    Truck Speed Empty (miles per hour): Default is set to 30 mph. This is how quickly each truck can be unloaded.
                    Truck Load Time (minutes): Default is set to 10 minutes. This is how long it takes to load each truck with debris.
                    Truck Dump Time (minutes): Default is set to 5 minutes. This is how long it takes to unload each truck with debris.
                    Other Waiting Time (minutes): Default is set to 5 mintes. This is just to account any extra time that the script might not take into account.
                    
Description:        Tool to determine the volume of debris in a given area
                        Takes in:
                            Raster layer with debris spread data - where value of a cell equates to the volume of debris in that area of the map
                            The extent over which the user wants to calculate the total debris volume
                        Returns:
                            The total volume of debris, in appropriate units(?), printed to the output of the script in arcGIS Pro
"""
import arcpy
import numpy
import math
import os


def increase_suffix(suff):
    fileName = "areaDebris" + str(suff) + ".tif"
    if arcpy.Exists(fileName):
        # arcpy.AddMessage(fileName + " alread exists!")
        suff += 1
        # errorMe = "suff number is {num}"
        # arcpy.AddMessage(errorMe.format(num = suff))
        return increase_suffix(suff)
    else:
        return int(suff)



# total debris volume of area
# sums debris volume over all clipped cells
def determineTotalVolume(debris, debrisPath, debrisUnits="Cubic Yards"):

	# convert the cells of the clipped raster to an array
    debrisClipDesc = arcpy.Describe(debris)
    lowerLeftCorner = arcpy.Point(debrisClipDesc.extent.XMin, debrisClipDesc.extent.YMin)
    array = arcpy.RasterToNumPyArray(debrisPath, lowerLeftCorner)
    arcpy.AddMessage("debris: {}".format(debris))

    debrisSum = array.sum()

    # print the total calculated sum to the message field
    message = "The total volume of debris in the area is {sum} {unit}"
    arcpy.AddMessage(message.format(sum=debrisSum, unit=debrisUnits))

    return debrisSum


#
if __name__ == '__main__':

    area = arcpy.GetParameter(0)  # the feature class containing the polygon area to calculate
    debris = arcpy.GetParameter(1)  # the raster feature layer containing the spread of debris
    # Testing removing environement to see if it has any effect
    # arcpy.env.workspace = arcpy.GetParameterAsText(4)
    fileName = arcpy.GetParameterAsText(2)  # name the output, optional choice
    if fileName == None:
        fileName = "areaDebris"

    debrisUnits = arcpy.GetParameterAsText(3)

    areaDesc = arcpy.Describe(area)

    extentStr = "{} {} {} {}".format(areaDesc.extent.XMin, areaDesc.extent.YMin, areaDesc.extent.XMax,
                                     areaDesc.extent.YMax)
    # clipPath = "./output/areaDebris.tif"
    suff = 0
    # fileName = "areaDebris" + str(suff) + ".tif"
    suff = increase_suffix(suff)

    if os.path.exists("./output") == False:
    	#arcpy.AddError("Output dir not found")
    	os.mkdir("./output");
    clipPath = "./output/" + fileName + str(suff) + ".tif"

    # clip the debris just to the given area
    debrisClip = arcpy.Clip_management(debris, extentStr, clipPath, area, 0,
                                       "ClippingGeometry", "MAINTAIN_EXTENT")


    totalDebrisVolume = determineTotalVolume(debrisClip, clipPath, debrisUnits)



