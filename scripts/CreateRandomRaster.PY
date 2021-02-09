"""
Update for error 999999
Tool:               <Tool label>
Source Name:        <File name>
Version:            <ArcGIS Version>
Author:             <Author>
Usage:              <Command syntax>
Required Arguments: <parameter0>
                    <parameter1>
Optional Arguments: <parameter2>
                    <parameter3>
Description:        <Description>
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
