"""
Tool:               Determine time to clear a given area of debris
Source Name:        DetermineClearanceTime.PY
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

if __name__ == '__main__':

    area = arcpy.GetParameter(0)                # the feature class containing the polygon area to calculate
    debris = arcpy.GetParameter(1)              # the raster feature layer containing the spread of debris
    numLoaders = int(arcpy.GetParameter(2))
    trucksPerLoader = int(arcpy.GetParameter(3))
    routeLength = float(arcpy.GetParameter(4)  )
    TruckVLimit = float(arcpy.GetParameter(5))
    truckWLimit = float(arcpy.GetParameter(6))
    efficiency = float(arcpy.GetParameter(7))
    truckSpeedL = float(arcpy.GetParameter(8))
    truckSpeedE = float(arcpy.GetParameter(9))
    loadTime = float(arcpy.GetParameter(10))
    dumpTime = float(arcpy.GetParameter(11))
    waitingTime = float(arcpy.GetParameter(12))

    #   Get the total volume of debris in the area
    #
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
    #TODO: add debris units parameter to function call 
    totalDebrisVolume = determineTotalVolume(debrisClip, clipPath)

    #assume an 8 hour work day
    workHourDay = 8

    # Density (lb/cy)
    ConcreteDensity = 860
    # wood/ brick density
    WnBDensity = 169

    # Formula:
    
    # Here should be a if statement to choose density type, ConcreteDensity is for temporary use
    
    # Weight of per truck(tons)
    TruckWeight = ConcreteDensity * TruckVLimit / 2000

    # Distance/Speed:
    HaulTime = routeLength / truckSpeedL * 60
    ReturnTime = routeLength / truckSpeedE * 60

    truckCycleTime = loadTime + HaulTime + dumpTime + ReturnTime + waitingTime

    # Quantity of Debris(1ton = 2000lbs)
    QuantityDebrisT = totalDebrisVolume
    QuantityDebrislb = QuantityDebrisT*2000

    # volume of debris (cy)
    VolDebris = QuantityDebrislb/WnBDensity

    # ideal number trucks/loader: the number of trucks per loader so loader can constantly be filling a truck
    ideal = 1 / (loadTime / 60)

    #come back to this later, add message mentioning an ideal allocation of resources and the time that would save
    if (int(trucksPerLoader) < ideal):
        Productivity = trucksPerLoader*TruckVLimit/(truckCycleTime*60*efficiency)
    else:
        # ideal productivity
        Productivity = ideal*TruckVLimit/(truckCycleTime*60*efficiency)

    TimeToClear = VolDebris/Productivity

    # days to clear with the given resources
    DaysToClean = TimeToClear / workHourDay
    #DaysToClean = Days1Fleet/(int(loaderFleets)*2000)

    RcleanTime = round(DaysToClean, 2)
    message1 = "The total time for cleaning the debris is {time} days"
    arcpy.AddMessage(message1.format(time=RcleanTime))