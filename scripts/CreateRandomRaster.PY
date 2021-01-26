"""
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

if __name__ == '__main__':

    arcpy.env.workspace = r'C:\Users\Josiah\Documents\ArcGIS\Projects\Geospatial Analysis For Disaster Planning'
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

    arcpy.AddMessage(arcpy.GetParameterAsText(1))

    if(arcpy.GetParameterAsText(1) != ""):
        cellSizeValue = float(arcpy.GetParameterAsText(1))
        if(cellSizeValue > (extent.XMax - extent.XMin) or cellSizeValue > (extent.YMax - extent.YMin)):
            arcpy.AddError("CellSize cannot be larger than extent dimensions")
    

    outRandomRaster = CreateRandomRaster(seedValue, cellSize, extent)
    outRandomRaster.save("./output/outrand.tif")

    p = arcpy.mp.ArcGISProject("CURRENT")
    map = p.listMaps()[0]

    lyrResult = arcpy.MakeRasterLayer_management("./output/outrand.tif", "tempLyr", "", "", "1")
    map.addLayer(lyrResult[0])

    arcpy.AddMessage("Successful!")
