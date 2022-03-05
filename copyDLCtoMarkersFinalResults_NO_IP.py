# For the import of sci_file_tools to work you must add the following directory to your python path. do
# nano ~/.bashrc
# down the bottom of the file, add:
# export PYTHONPATH=/home/spencelab/spencelab/code/python/KinematicsSoftware_Dreadds:$PYTHONPATH
import pandas as pd
#import cv2
import numpy as np
from shutil import copyfile
import os, sys
import csv
from os import path
from glob import glob
import fileinput
from termcolor import colored, cprint
import math
import pdb
import datetime
import re
from sci_file_tools import *

# TODO:
# THis only works when data are inside a subfolder of the dump folder called
# analyze_videos!
# We need to update it to work with dump folders that do not have those subfolders!
# It should find all data folders, then figure out which belong to the same dump,
# then use either the newest analze_videos subfolder OR the outer dump folder.

print("""
This program finds deeplabcut output files (csv) and converts them to files that can be
input into Omid Haji-Maghsoudi (former Spence Lab phd student) code for 3D reconstruction.

IMPORTANT
The code finds files in sub directories of the current directory in the following manner.
It uses code within sci_file_tools.py to do this.
1. It finds all dump folders in all subdirectories of the current one.
2. The folders matching the above criteries must be in a set of nest subfolders with the 
following properties:
a) There must be at least 5 directories above this one. E.g. at least
/sb4/week1/cam3/rat155/2020-07-23_15_58_30 and potentially more before sb4...
b) The folder above the current one must begin with 'rat' case sensitive
c) The folder two above the current one must begin with 'cam' case sensitive
3. Each dump folder for cam3 is matched with one for cam4. Those missing cam4 are ignored.
3. Within each dump folder, it looks for DLC CSV files aithin analyze_videos subfolders,
failing that it looks within the dump folder itself. For with extension .csv that
contain "scorer" as the first few characters, thus identifying all DLC output.
4. If multiple files matching this criteria are found, it only returns the most recently
modified file that matches the criteria for the current directory.

Other directories containing appropriate DLC output files but not having directories
above with the corret cam and rat in the right location will be ignored.
""")

"""
PROBLEM TO FIX NEXT:
THIS IS BUG IN INTERPOLATION - FIX LATER. TOOK OUT INTERPOLATION FOR NOW.
Directory 790 of 2458
cam3: /zfstank3/storage/Shriners Study/20200712 shriners jte sb4/sb4/week1/cam3/rat172/2020-07-23_17_03_33
  Found a corresponding cam4 directory with correct date of dump.
cam3dirlist ['2020-10-06_12_49_26_analyze_videos']
cam3dirlist[0] or cam3newestanalysis 2020-10-06_12_49_26_analyze_videos
cam4: /zfstank3/storage/Shriners Study/20200712 shriners jte sb4/sb4/week1/cam4/rat172/2020-07-23_17_03_33
cam4dirlist ['2020-10-06_01_19_13_analyze_videos']
cam4dirlist[0] or cam4newestanalysis 2020-10-06_01_19_13_analyze_videos
Successfully merged coordinates for both cameras
Traceback (most recent call last):
  File "/home/spencelab/spencelab/code/python/Dreads_Tracking_Requirement/20201015_jteedits_copyDLCtoMarkersFinalResults_NO_IP.py", line 323, in <module>
    FRip[:,col] = A
ValueError: could not broadcast input array from shape (334) into shape (999)
"""

debug=False
#Can specify one time point to do
# To do all, specifiy empty weektoanalyze=[]
weektoanalyze=[]
# can skip ahead if previous runs crashed...
startat=0

# Get a pandas data frame of valid dumps and dlc csv files. See sci_file_tools.py.
df=do_all_for_copyDLCtoMarker('.',debug)
# Narrow the week here... just use pandas.
if weektoanalyze:
    df=df[df.week==weektoanalyze]

for i in range(startat,len(df)):
    path3 = os.path.join(os.getcwd(),df.iloc[i].cam3pathtodir)
    path4 = os.path.join(os.getcwd(),df.iloc[i].cam4pathtodir)
    print("\nDirectory %d of %d\n  cam3: %s" % (i+1,len(df),path3))
    # Find any matching date camera 4 folders by checking them all:
    print("  Loading the dlc dsv files.")
    cam3csv = pd.read_csv(os.path.join(os.getcwd(),df.iloc[i].cam3dlccsv), skiprows=[0,1,2], sep=',', dtype={'ID': object})        
    cam4csv = pd.read_csv(os.path.join(os.getcwd(),df.iloc[i].cam4dlccsv), skiprows=[0,1,2], sep=',', dtype={'ID': object})
    # Do the merging
    try: # might need to add a try/os.error b/c it's looking for mfr.csv 
        File_name = 'Marker_Final_Results.csv'
        row_count = cam3csv.shape[0]

        Final_Results = np.empty([row_count,23])
        Frame = np.empty([row_count,1])
        Framedir = np.empty([row_count,2],dtype=str)

        Header1 = [np.array(["The 3D Marker tracked was used by the following settings"])]
        Header2 = [np.array(["Number of markers 5"])]
        Header3 = [np.array(["SLIC parameters as Number 1200 Sig 1 Comp 5"])]
        Header4 = [np.array(["Window Size was 35"])]
        Header5 = [np.array(["Path of the first camera was {} and path of the second camera was{}".format(path3,path4)])]
        Header6 = np.array([["Frames"],["First Camera Frames Name"],["Second Camera Frames Name"],["Y Coordinate M"],["X Coordinate M"],["Y Coordinate M2"],["X Coordinate M2"],["Y Coordinate N"],["X Coordinate N"],["Y Coordinate N2"],["X Coordinate N2"],["Y Coordinate O"],["X Coordinate O"],["Y Coordinate O2"],["X Coordinate O2"],["Y Coordinate P"],["X Coordinate P"],["Y Coordinate P2"],["X Coordinate P2"],["Y Coordinate Q"],["X Coordinate Q"],["Y Coordinate Q2"],["X Coordinate Q2"]])

        # #print(Header1.shape,Header2.shape,Header3.shape,Header4.shape,Header5.shape,Header6.shape)
        Header = np.hstack([Header1,Header2,Header3,Header4,Header5])
        #k=[0 for x in range(row_count)]
        for l in range(row_count):
        #     #Compare likelihood, should be above 95%
                #condzi = (cam3csv.iat[l,3] >0.75 and cam3csv.iat[l,6] >0.75 and cam3csv.iat[l,9] >0.75 and cam3csv.iat[l,12] >0.75 and cam3csv.iat[l,15] >0.75 and cam4csv.iat[l,3] >0.75 and cam4csv.iat[l,6] >0.75 and cam4csv.iat[l,9] >0.75 and cam4csv.iat[l,12]>0.75 and cam4csv.iat[l,15] > 0.75)
            #     #First marker cam3 y,x
                Final_Results[l+0,0] =  cam3csv.iat[l,0]#Extracts the frame number
                Final_Results[l+0,1] =  0
                Final_Results[l+0,2] =  0 #123456 should be the directory of the frames

            #if cam3csv.iat[l,3] > 0.95:
                Final_Results[l+0,3] =  cam3csv.iat[l,2]
                Final_Results[l+0,4] =  2048- cam3csv.iat[l,1]
            # else:
            #     Final_Results[l+0,3] = math.nan
            #     Final_Results[l+0,4] = math.nan

            #First marker cam4 y,x
            # if cam4csv.iat[l,3] > 0.95:
                Final_Results[l+0,5] =  cam4csv.iat[l,2]
                Final_Results[l+0,6] =  2048- cam4csv.iat[l,1]
            # else:
            #     Final_Results[l+0,5] = math.nan
            #     Final_Results[l+0,6] = math.nan
            #Second marker cam3 y,x

            # if cam3csv.iat[l,6] > 0.95:
                Final_Results[l+0,7] =  cam3csv.iat[l,5]
                Final_Results[l+0,8] =  2048-cam3csv.iat[l,4]
            # else:
            #     Final_Results[l+0,7] =  math.nan
            #     Final_Results[l+0,8] =  math.nan

            #Second marker cam4 y,x
            # if cam4csv.iat[l,6] > 0.95:
                Final_Results[l+0,9] =  cam4csv.iat[l,5]
                Final_Results[l+0,10]=  2048-cam4csv.iat[l,4]
            # else:
            #     Final_Results[l+0,9] = math.nan
            #     Final_Results[l+0,10]= math.nan

            #Third marker cam3 y,x
            # if cam3csv.iat[l,9] > 0.95:
                Final_Results[l+0,11]=  cam3csv.iat[l,8]
                Final_Results[l+0,12]=  2048-cam3csv.iat[l,7]
            # else:
            #     Final_Results[l+0,11]=  math.nan
            #     Final_Results[l+0,12]=  math.nan
            # #Third marker cam4 y,x
            # if cam4csv.iat[l,9] > 0.95:
                Final_Results[l+0,13]=  cam4csv.iat[l,8]
                Final_Results[l+0,14]=  2048-cam4csv.iat[l,7]
            # else:
            #     Final_Results[l+0,13]=  math.nan
            #     Final_Results[l+0,14]=  math.nan
            # #fourth marker cam 3 y,x, cam4 y,x
            # if cam3csv.iat[l,12] > 0.95:
                Final_Results[l+0,15]=  cam3csv.iat[l,11]
                Final_Results[l+0,16]=  2048-cam3csv.iat[l,10]
            # else:
            #     Final_Results[l+0,15]=  math.nan
            #     Final_Results[l+0,16]= math.nan
            #
            # if cam4csv.iat[l,12] > 0.95:
                Final_Results[l+0,17]=  cam4csv.iat[l,11]
                Final_Results[l+0,18]=  2048-cam4csv.iat[l,10]
            # else:
            #     Final_Results[l+0,17]=  math.nan
            #     Final_Results[l+0,18]=  math.nan
            # #Fifth marker cam 3 y,x cam4 y,x
            # if cam3csv.iat[l,15] > 0.95:
                Final_Results[l+0,19]=  cam3csv.iat[l,14]
                Final_Results[l+0,20]=  2048-cam3csv.iat[l,13]
            # else:
            #     Final_Results[l+0,19]=  math.nan
            #     Final_Results[l+0,20]=  math.nan
            #
            # if cam4csv.iat[l,15] > 0.95:
                Final_Results[l+0,21]=  cam4csv.iat[l,14]
                Final_Results[l+0,22]=  2048-cam4csv.iat[l,13]
                # else:
                #     Final_Results[l+0,21]=  math.nan
                #     Final_Results[l+0,22]=  math.nan


        # compa = np.empty([row_count,1],dtype=bool)
        # for p in range(row_count):
        #
        #     compa[p] = (cam3csv.iat[p,3] >0.75 and cam3csv.iat[p,6] >0.75 and cam3csv.iat[p,9] >0.75 and cam3csv.iat[p,12] >0.75 and cam3csv.iat[p,15] >0.75 and cam4csv.iat[p,3] >0.75 and cam4csv.iat[p,6] >0.75 and cam4csv.iat[p,9] >0.75 and cam4csv.iat[p,12]>0.75 and cam4csv.iat[p,15] > 0.75)
        #
        #
        FResults = Final_Results
        #import pdb; pdb.set_trace()
        Header = pd.DataFrame(Header)
        Header = Header.reindex([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22])

        Results = pd.DataFrame(FResults)
        #print (Results.iloc[:,0].shape)
        #print (Results)
        #print (Results.iloc[:,0].iteritems())
        for n,r in (Results.iterrows()):
            Framenumb = str(int(Results.iloc[n,0])).zfill(5)
            Results.iloc[n,1] = "{}/Frame{}.png".format(path3,Framenumb)
            Results.iloc[n,2] = "{}/Frame{}.png".format(path4,Framenumb)

        Results = Results[Results.iloc[:,0]>=1] #this gets rids of empty values
        FRData=Final_Results #to use for interpolation
        Final_Results = np.vstack([np.transpose(Header),np.transpose(Header6),Results])
        FR = pd.DataFrame((Final_Results))
        # Not sure we need the cwd stuff...
        targetfile=os.path.join(os.getcwd(),df.iloc[i].cam3pathtodir,File_name)
        if debug:
            print("  Would write: %s" % targetfile)
        print("  Writing output file: %s" % targetfile)
        FR.to_csv(targetfile,header=False,index=False)
        cprint("Successfully merged coordinates for both cameras",'green')

        if False:
            FRip=np.empty([999,23]) #Creating array for interpolation
            for col in range(Final_Results.shape[1]):
                A = FRData[:,col]
                goodframes= ~np.isnan(A)
                xp = goodframes.ravel().nonzero()[0]
                fp = A[~np.isnan(A)]
                x = np.isnan(A).ravel().nonzero()[0]

                A[np.isnan(A)] = np.interp(x,xp,fp) #interpolates for cells with nan values

                FRip[:,col] = A

            FRIP=pd.DataFrame(FRip)
            for n,r in (Results.iterrows()):

                Framenumb = str(int(FRIP.iloc[n,0])).zfill(5)
                Results.iloc[n,1] = "{}/Frame{}.png".format(path3,Framenumb)
                Results.iloc[n,2] = "{}/Frame{}.png".format(path4,Framenumb)

            FRIP = np.vstack([np.transpose(Header),np.transpose(Header6),FRIP])
            FR_IP = pd.DataFrame((FRIP))
            FR_IP.to_csv('Interpolation.csv',header=False,index=False)
    except:
        cprint("ERROR: Failed to merge coordinates for both cameras",'red')