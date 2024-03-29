"""
Tool:               Create random debris raster data
Source Name:        CreateRandomRaster.PY
ArcGIS Version:            2.6.0
Required Arguments: Cell Size:
                        Determines how large each data cell (each square) is inside the raster. Larger values will create larger cells/squares
                    Extent:
                        The size (coordinate values) of the space to generate the raster inside. An existing polygon or feature can be used or a new one can be drawn.
                    Clip To:
                         The shape to clip the resulting raster image to. An existing polygon or feature can be used or a new one can be drawn.
                    Name of Output File:
                        The desired name of the output .tif file
                    Environment (env) Workspace:
                        A folder from the workspace should be used for the environment workspace.

Optional Arguments: Seed Value:
                        Value to seed the generation of randomness for the raster (optional). This should be an integer or floating-point number.

Description:        This script is used to generate random raster data that can be used for testing purposes. The script takes in user input for the area the
                    user wants to find debris for. It then uses the Arcpy library to generate raster data.
"""
import arcpy
import os.path

if __name__ == '__main__':

    #arcpy.env.workspace = r'C:\Education\Capstone\CapstoneProject'
    arcpy.env.overwriteOutput = True

    if(arcpy.CheckExtension('Spatial') == 'Available'):
        arcpy.CheckOutExtension('Spatial')
        from arcpy.sa import *
    else:
        arcpy.AddError("spatial analysis is not available")

    from arcpy.sa import *

    seedValue = arcpy.GetParameter(0)
    cellSize = arcpy.GetParameter(1)
    extent = arcpy.GetParameter(2)
    clippingGeo = arcpy.GetParameter(3)
    nameOutput = arcpy.GetParameter(4)
    arcpy.env.workspace = arcpy.GetParameterAsText(5)


    arcpy.AddMessage(arcpy.GetParameterAsText(1))

    if(arcpy.GetParameterAsText(1) != ""):
        cellSizeValue = float(arcpy.GetParameterAsText(1))
        if(cellSizeValue > (extent.XMax - extent.XMin) or cellSizeValue > (extent.YMax - extent.YMin)):
            arcpy.AddError("CellSize cannot be larger than extent dimensions")
    

    outRandomRaster = CreateRandomRaster(seedValue, cellSize, extent)
    
    #create the output directory if none exists
    if os.path.exists("./output") == False:
    	#arcpy.AddError("Output dir not found")
    	os.mkdir("./output");
    filePath = "./output/" + nameOutput + ".tif"
    fileName = "./output/" + nameOutput + "Clipped"+ ".tif"
    
    #outRandomRaster.save("./output/outrandp5test.tif")
    outRandomRaster.save(filePath)

    p = arcpy.mp.ArcGISProject("CURRENT")
    map = p.listMaps()[0]
    #lyrResult = arcpy.MakeRasterLayer_management("./output/outrand.tif", "tempLyr", "", extent, "1")

    if len(arcpy.GetParameterAsText(3)) == 0:
    	lyrResult = arcpy.MakeRasterLayer_management(filePath, "tempLyr", "", extent, "1")
    else:
   		#clip the raster layer to the input clipping geometry layer
   		extentStr = "{} {} {} {}".format(extent.XMin, extent.YMin, extent.XMax, extent.YMax)
   		arcpy.Clip_management(filePath, extentStr, fileName, clippingGeo, .1, "ClippingGeometry", "MAINTAIN_EXTENT")
   		lyrResult = arcpy.MakeRasterLayer_management(fileName, "tempLyr", "", extent, "1")

    map.addLayer(lyrResult[0])

    arcpy.AddMessage("Successful!")
