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
def getRouteToDump(roads, debrisCenter, dump):
    #arcpy.CreateRoutes_lr(roads, "ALIAS_NAME", "Routes", "LENGTH", "#", "#", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    #arcpy.mp.ArcGISProject().defaultGeodatabase
    networkDataset = "C:/Education/Capstone/CapstoneProject/Default.gdb/Feature_Dataset/Network_Dataset"

    result_object = arcpy.na.MakeRouteAnalysisLayer(networkDataset, "SimpleRoute", "Driving Time")
    layer_object = result_object.getOutput(0)
    arcpy.AddMessage(layer_object)

    #Get the names of all the sublayers within the route layer.
    sublayer_names = arcpy.na.GetNAClassNames(layer_object)
    arcpy.AddMessage(sublayer_names)

    #Stores the layer names that we will use later
    stops_layer_name = sublayer_names["Stops"]
    arcpy.AddMessage(stops_layer_name)
    
    
    """
        Stopping point: need to make sure that the stops feature class has the right type of data
    """
    hardCodedStops = "C:/Education/Capstone/CapstoneProject/Default.gdb/Feature_Dataset/stops"
    arcpy.na.AddLocations(layer_object, "Stops", hardCodedStops, "", "")

    arcpy.na.Solve(layer_object)

    outputLayer = "C:/Education/Capstone/CapstoneProject/Default.gdb/Feature_Dataset/route.lyrx"
    layer_object.saveACopy(output_layer_file)

if __name__ == '__main__':

    
    area = arcpy.GetParameter(0)                # the feature class containing the polygon area to calculate
    debris = arcpy.GetParameter(1)              # the raster feature layer containing the spread of debris
    roads = arcpy.GetParameter(2)               # the feature class containing the road lines and points
    dumpLoc = arcpy.GetParameter(3)             # the point (coordinate) of the dump site

    # the rest of the variables to follow
    #loaderFleets = arcpy.GetParameter(4)        # Loader fleet refers to 1 loader and the trucks that it hauls.
    


    areaDesc = arcpy.Describe(area)
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

    centerPoint = arcpy.Point((areaDesc.extent.XMin + areaDesc.extent.XMax) / 2, (areaDesc.extent.YMin + areaDesc.extent.YMax) / 2)
    route = getRouteToDump(roads, centerPoint, dumpLoc)

    # routeLength = route.


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
