import os
import sys
import numpy as np
import pandas as pd
import math

#This code must run in the desired Results Kinematics folder
#What this code does is omit the y space from computed 3D coordinates, 
#compute angles from the x and z coordinates of the 5 joints of interest,
#and replace the 3D angles with the 2D angles and rewrite the file so it
#can run with the Kinematics GUI

#Run this code after computing the stride features on the kinematics GUI,
#but before you create the time series. The remainder of the steps should be done
#on the GUI 

#Function to compute angles from 2D vectors
def ang2D(joint1,joint2,joint3) :
	cosA=np.dot(joint1-joint2,joint3-joint2)/(np.linalg.norm(joint1-joint2)*np.linalg.norm(joint3-joint2))
	angdeg=math.degrees(math.acos(cosA))
	return angdeg

#iterating over the files in Results Kinematics
directory = os.listdir()
feats=[]
#retrieving files with Stride_Features in them
for i in directory:
	if 'Stride_Features' in i:
		feats.append(i)

#iterating over files that contain Stride_Features
for file in feats:
	data=pd.read_csv(file)

	#now assigning 2d variables for the 5 joints by omitting the y space:
	ASIS=np.transpose(np.array([data["Asis_x"],data["Asis_z"]]))
	Hip=np.transpose(np.array([data["Hip_x"],data["Hip_z"]]))
	Knee=np.transpose(np.array([data["Knee_x"],data["Knee_z"]]))
	Ankle=np.transpose(np.array([data["Ankle_x"],data["Ankle_z"]]))
	Toe=np.transpose(np.array([data["Toe_x"],data["Toe_z"]]))

	#creating DataFrame for the 3 2D angles that are going to be computed with the
	#size of the same strides features
	Angs2D = pd.DataFrame(index=np.arange(data.shape[0]),columns=np.arange(3))
	Angs2D.columns=["Hip_Angle_2D","Knee_Angle_2D","Ankle_Angle_2D"]

	for ind in range(data.shape[0]):
		Angs2D["Hip_Angle_2D"][ind]= ang2D(ASIS[ind],Hip[ind],Knee[ind])
		Angs2D["Knee_Angle_2D"][ind]= ang2D(Hip[ind],Knee[ind],Ankle[ind])
		Angs2D["Ankle_Angle_2D"][ind]= ang2D(Knee[ind],Ankle[ind],Toe[ind])

	#overwriting the 3D angles into the 2D computed angles
	data['Angle Asis Hip Knee'] = Angs2D['Hip_Angle_2D']
	data['Angle Hip Knee Ankle'] = Angs2D['Knee_Angle_2D']
	data['Angle Knee Ankle Toe'] = Angs2D['Ankle_Angle_2D']

	
	#now saving and overwriting the Stride_Features file
	data.to_csv(file)
	print("Successfully replaced 3D angles with 2D angles for file",file)