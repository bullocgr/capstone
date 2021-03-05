"""
update the script
Tool:               Determine debris volume of a given area
Source Name:        DetermineDebrisVolume.PY
Version:            <ArcGIS Version>
Author:             <Author>
Usage:              <Command syntax>
Required Arguments: <parameter0>
                    <parameter1>
Optional Arguments: <parameter2>
                    <parameter3>


Description:        Tool to determine the volume of debris in a given area
                        Takes in:
                            Raster layer with debris spread data - where value of a cell equates to the volume of debris in that area of the map
                            The extent over which the user wants to calculate the total debris volume
                        Returns:
                            The total volume of debris, in appropriate units(?), printed to the output of the script in arcGIS Pro

                    Details/To-Do:
                        Find method to poll the raster data at a specific x,y position

                        Two general approaches:
                            Iterate over the raster image, from the lower x,y to the upper x,y polling the values of the raster layer and adding all the values together
                                We need to be careful here, because the units of the bounds will be in latitude and longitude and we will need to be able to use either meters or feet to multiply
                                a particulr value from the raster layer by the area of our unit (ex: if we subdivide and sample at 1000 points along x and y, each sample value needs to be multiplied by the actual area of each cell,
                                which would be (maxX - minx)/1000 *  (maxY - minY)/1000) )

                            Or use some other arcPy functionality to automatically add all the values of the raster layer where it intersects with the extent
                                I have hope for this approach, but don't even know what to google yet
                                Maybe clip the raster to just the extent, then use a sum function to sum all of that?





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
# = density of debris for each individual cell
# * the area that a cell covers
# summed over all clipped cells
def determineTotalVolume(debris, debrisPath):

	# convert the cells of the clipped raster to an array
    debrisClipDesc = arcpy.Describe(debris)
    lowerLeftCorner = arcpy.Point(debrisClipDesc.extent.XMin, debrisClipDesc.extent.YMin)
    array = arcpy.RasterToNumPyArray(debrisPath, lowerLeftCorner)
    arcpy.AddMessage("debris: {}".format(debris))

    #get info from the clipped raster
    xResult = arcpy.GetRasterProperties_management(debris, "CELLSIZEX")
    yResult = arcpy.GetRasterProperties_management(debris, "CELLSIZEY")
    maxYResult = arcpy.GetRasterProperties_management(debris, "TOP")
    cellSizeX = float(xResult.getOutput(0))
    cellSizeY = float(yResult.getOutput(0))
    maxY = float(maxYResult.getOutput(0))

    # 1 degree latitude = 364000 feet
    #                   / 3 = yards
    latDegreeLen = 364000 / 3

    debrisSum = 0
    rowCount = 0
    for row in array:
        # 1 degree of longitude is the cosine of the latitude y
        # times the longitude at the equator (equivalent to any latitude)
        longDegreeLen = math.cos(math.radians(maxY - (rowCount * cellSizeY))) * latDegreeLen
        for cell in row:
            cellArea = (cellSizeX * longDegreeLen) * \
                       (cellSizeY * latDegreeLen)
            msg = "Value of cell: {val}, area of cell: {area} square yards"
            arcpy.AddMessage(msg.format(val=cell, area=cellArea))
            msg = "This cell contains {val} tons of debris"
            arcpy.AddMessage(msg.format(val=cell * cellArea))
            debrisSum += cell * cellArea
        rowCount += 1

    # print the total calculated sum to the message field
    message = "The total volume of debris in the area is {sum}"
    arcpy.AddMessage(message.format(sum=debrisSum))

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


    totalDebrisVolume = determineTotalVolume(debrisClip, clipPath)



