"""
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


#
if __name__ == '__main__':

    area = arcpy.GetParameter(0)      #the feature class containing the polygon area to calculate
    debris = arcpy.GetParameter(1)      #the raster feature layer containing the spread of debris
    
    areaDesc = arcpy.Describe(area)

    extentStr = "{} {} {} {}".format(areaDesc.extent.XMin, areaDesc.extent.YMin, areaDesc.extent.XMax, areaDesc.extent.YMax)
    clipPath = "./output/areaDebris.tif"

    #clip the debris just to the given area
    debrisClip = arcpy.Clip_management(debris, extentStr, clipPath, area, 0,
                      "ClippingGeometry", "MAINTAIN_EXTENT")

    #convert the cells of the clipped raster to an array
    debrisClipDesc = arcpy.Describe(debrisClip)
    lowerLeftCorner = arcpy.Point(debrisClipDesc.extent.XMin, debrisClipDesc.extent.YMin)
    array = arcpy.RasterToNumPyArray(clipPath, lowerLeftCorner)
    debrisSum = array.sum()

    #print the total calculated sum to the message field
    message = "The total value of the raw data from the raster is {sum}"
    arcpy.AddMessage(message.format(sum = debrisSum))
