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

    # ScriptTool parameters
    roads = arcpy.GetParameter(0)
    debris = arcpy.GetParameter(1)
    debrisExtent = arcpy.GetParameter(2)

    #get intersection
    rectangleStr = "{} {} {} {}".format(debrisExtent.XMin, debrisExtent.YMin, debrisExtent.XMax, debrisExtent.YMax)
    arcpy.Clip_management(debris, rectangleStr, "./output/debrisRoadsIntersection.tif", roads, .1, "ClippingGeometry", "MAINTAIN_EXTENT")

    #add to map as layer
    lyrResult = arcpy.MakeRasterLayer_management("./output/debrisRoadsIntersection.tif", "debrisRoadsIntersectionLyr", "", debrisExtent, "1")

    p = arcpy.mp.ArcGISProject("CURRENT")
    map = p.listMaps()[0]

    map.addLayer(lyrResult[0])

    arcpy.AddMessage("Successful!")


