# Geospatial Analysis for Disaster Planning
## What This Repo Does
This repo is a geospatial analysis tool that provides emergency managers with a systems level view of the impact of disasters on their jurisdiction’s lifeline networks. The software is intended help them in creating robust response plans by identifying critical intersections of lifeline networks that may cause bottlenecks in recovery, as well as by providing estimates of time and resources required for debris clearance.

## Programs Needed to Run this Repo
* ArcGIS Pro

### How to Download ArcGIS Pro
#### For OSU Students
Follow the instructions for downloading ArcGIS Pro [here](https://oregonstate.teamdynamix.com/TDClient/1935/Portal/KB/ArticleDet?ID=89855). This repo has been tested on version 2.6.0.

### How to Download the Repo
Click on the `clone` button at the upper right hand corner. Copy the `https` link and navigate to a place in your terminal that you would like to place the repo. Type the command `git clone <https link>` and the repo will be cloned. You can now edit the repo as well as run the scripts and toolboxes.

#### How to Navigate the Repo
The repo is made up of two parts: the `scripts` folder and the `toolboxes` folder. You will need both of these in order to run them in ArcGIS Pro. The python scripts that will run to calculate the time and resources for debris clearance will be found in the `scripts` folder. ArcGIS Pro uses toolboxes to hold data and the scripts require the data to run. Read more about toolboxes [here](https://pro.arcgis.com/en/pro-app/latest/tool-reference/analysis/an-overview-of-the-analysis-toolbox.htm). The script and the pairing toolbox should have the same name.

### How to Run the Repo
Once ArcGIS Pro and the repo have been properly downloaded, navigate to the `insert` tab in ArcGIS Pro and find the `toolbox` button. Click that and select `add toolbox`. Navigate to where the repo is saved on your computer and go into the `toolboxes` folder. Select the toolbox you want to import. Once the toolbox is imported, open it in the catalog side pannel to the right and you should see a `script` there. Right click the script and select `properties`. In the `script file` section, set it to point at the appropriate script in the `scripts` folder of where this repo is saved. You should have everything set up to run properly now.

As of right now, whenever a change is made to the main branch, the toolboxes will have to be reimported and the scripts will have to be updated.

*Each script requires different things to run. Navigate to the [wiki](https://github.com/bullocgr/capstone/wiki) or look in the scripts to see what is required to run the scripts.*
