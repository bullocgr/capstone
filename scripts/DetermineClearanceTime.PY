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


Description:        Tool to determine the total time to clear a given area of debris
    


"""
import arcpy
import numpy
import os
import math
from DetermineDebrisVolume import determineTotalVolume, increase_suffix


"""
    How I think routing has to work in arcpy:
        To route, a network dataset is required
            A network dataset must live within a feature dataset
            And share the feature dataset with the network (edges and junctions)
            As well as any stops (I think)
        Use the network dataset in the process of making a network analysis layer
        set the layer to read the stops and the edges and junctions, as well as to optimize for shortest distance between stops
        Finally, use the solve function on the layer
        Then do something with the result??
"""
def getRouteToDump(featureDataset, roads, debrisCenter, dump):

    if arcpy.CheckExtension("network") == "Available":
        arcpy.CheckOutExtension("network")
    else:
        raise arcpy.ExecuteError("Network Analyst Extension license is not available.")


    stopsFC = createStops(featureDataset, debrisCenter, dump)          # first create the feature class for the stops (debris site and dump site)


    networkDataset = arcpy.na.CreateNetworkDataset(featureDataset, "Road_Network" , [roads, "Stops"], "NO_ELEVATION" ) # create new network dataset 
    arcpy.na.BuildNetwork(networkDataset)


    result_object = arcpy.na.MakeRouteAnalysisLayer(networkDataset, "SimpleRoute")
    layer_object = result_object.getOutput(0)
    sublayer_names = arcpy.na.GetNAClassNames(layer_object) #Get the names of all the sublayers within the route layer.
    stops_layer_name = sublayer_names["Stops"]              #Stores the layer names that we will use later
    arcpy.na.AddLocations(layer_object, stops_layer_name, stopsFC, "", "")

    arcpy.na.Solve(layer_object)

    outputLayer = "C:/Education/Capstone/CapstoneProject/Default.gdb/Feature_Dataset/route.lyrx"
    layer_object.saveACopy(output_layer_file)



def createStops(featureDataset, startPoint, endPoint):

    featureClass = arcpy.management.CreateFeatureclass(featureDataset, "Stops", "POINT")

    cursor = arcpy.da.InsertCursor(featureClass, ["SHAPE@XY"])


    arcpy.AddMessage(startPoint.Y)
    arcpy.AddMessage(endPoint.Y)
    metersPerDegreeX = 111319.9
    metersPerDegreeY = 125802.7         #????? Using the extent of other points in the area to derive this one, the other wasn't even close
    coordsToMeters = [(startPoint.X * metersPerDegreeX,  startPoint.Y * metersPerDegreeY),
                    (endPoint.X * metersPerDegreeX, endPoint.Y *  metersPerDegreeY)]

    cursor.insertRow([coordsToMeters[0]])
    cursor.insertRow([coordsToMeters[1]])


    return featureClass



if __name__ == '__main__':

    
    area = arcpy.GetParameter(0)                # the feature class containing the polygon area to calculate
    debris = arcpy.GetParameter(1)              # the raster feature layer containing the spread of debris
    featureDataset = arcpy.GetParameter(2)      # the feature dataset containing the roads
    roadsFC = arcpy.GetParameter(3)             # the name of the road feature class
    dumpArg = arcpy.GetParameterAsText(4).split()       # the point (coordinate) of the dump site - no idea why it won't import as a point (??)
    dumpPoint = arcpy.Point(float(dumpArg[0]), float(dumpArg[1]))

    # the rest of the variables to follow
    #loaderFleets = arcpy.GetParameter(4)        # Loader fleet refers to 1 loader and the trucks that it hauls.
    

    
    #   Get the total volume of debris in the area
    #
    areaDesc = arcpy.Describe(area)
    
    """
    extentStr = "{} {} {} {}".format(
        areaDesc.extent.XMin, areaDesc.extent.YMin, areaDesc.extent.XMax, areaDesc.extent.YMax)
    
    suff = 0
    suff = increase_suffix(suff)
    clipPath = "./output/clip" + str(suff) + ".tif"

    # clip the debris just to the given area
    debrisClip = arcpy.Clip_management(debris, extentStr, clipPath, area, 0,
                                       "ClippingGeometry", "MAINTAIN_EXTENT")

    # debrisSum = array.sum()
    totalDebrisVolume = determineTotalVolume(debrisClip, clipPath)

    
    """

    #       Get the route to the dump and its distance:
    #
    centerPoint = arcpy.Point((areaDesc.extent.XMin + areaDesc.extent.XMax) / 2, (areaDesc.extent.YMin + areaDesc.extent.YMax) / 2)
    getRouteToDump(featureDataset, roadsFC, centerPoint, dumpPoint)

    # routeLength = route.

    """
    # default values:
    # Volume / Truck = 30cy
    TruckVLimit = 30
    # Weight / Truck = 20tons
    TruckWLimit = 20
    # Loader Cycle Time = 10 mins
    LoadCTime = 10
    # Efficiency of site = 0.83
    Efficiency = 0.83
    # Truck Speed Loaded = 25mph
    TruckSpeedL = 25
    # Truck Speed empty = 30mph
    TruckSpeedE = 30
    # Load Time = 10 mins
    LoadTime = 10
    # Dump Time = 5 mins
    DumpTime = 5
    WaitingTime = 5
    # Assume work for 8 hours per day
    workHourDay = 8

    # Formula:
    # Truck Cycle Time = 52 mins
    TruckCTime = 52
    # Density (lb/cy)
    ConcreteDensity = 860
    # wood/ brick density
    WnBDensity = 169
    # Here should be a if statement to choose density type, ConcreteDensity is for temporary use
    # Weight of per truck(tons)
    TruckWeight = ConcreteDensity * TruckVLimit / 2000

    # Value from GIS map
    # Distance/Speed:
    # Unable to find distance for now, requires traffic dataset
    HaulTime = 24  # temporary
    ReturnTime = 8  # temporary
    # Quantity of Debris(1ton = 2000lbs)
    QuantityDebrisT = totalDebrisVolume
    QuantityDebrislb = QuantityDebrisT*2000
    # volume of debris (cy)
    VolDebris = QuantityDebrislb/ConcreteDensity
    # ideal number trucks/loader = 6
    ideal = 6

    if (int(nTracks) < ideal):
        Productivity = nTracks*TruckVLimit/(LoadCTime*60*Efficiency)
    else:
        # ideal productivity
        Productivity = TruckVLimit/(TruckCTime*60*Efficiency)

    TimeToClear = VolDebris/Productivity

    # days to clear or 1 loader fleet
    Days1Fleet = TimeToClear / workHourDay
    DaysToClean = Days1Fleet/(int(loaderFleets)*2000)

    RcleanTime = round(DaysToClean, 2)
    message1 = "Hi! The total time for cleaning the debris is {time} days"
    arcpy.AddMessage(message1.format(time=RcleanTime))
    """
