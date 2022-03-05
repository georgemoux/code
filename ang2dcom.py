import pandas as pd 
import numpy as np
import math

data=pd.read_csv('/zfsr01/storage/knee-tattoo/IR-Knee/RK_for_2D/Stride_Features.rat282.triangulation_speed16.2021-09-21_12_34_59 (copy 1).csv')
def ang2D(joint1,joint2,joint3) :
	cosA=np.dot(joint1-joint2,joint3-joint2)/(np.linalg.norm(joint1-joint2)*np.linalg.norm(joint3-joint2))
	angdeg=math.degrees(math.acos(cosA))
	return angdeg

#Assigning 2D variables by omitting the y space

ASIS=np.transpose(np.array([data["Asis_x"],data["Asis_z"]]))
Hip=np.transpose(np.array([data["Hip_x"],data["Hip_z"]]))
Knee=np.transpose(np.array([data["Knee_x"],data["Knee_z"]]))
Ankle=np.transpose(np.array([data["Ankle_x"],data["Ankle_z"]]))
Toe=np.transpose(np.array([data["Toe_x"],data["Toe_z"]]))

#creating DataFrame for the 3 2D angles that are going to be computed with the
#size of the same strides features
Angs2D = pd.DataFrame(index=np.arange(data.shape[0]),columns=np.arange(3))
Angs2D.columns=["Hip_Angle_2D","Knee_Angle_2D","Ankle_Angle_2D"]

for i in range(data.shape[0]):
	Angs2D["Hip_Angle_2D"][i]= ang2D(ASIS[i],Hip[i],Knee[i])
	Angs2D["Knee_Angle_2D"][i]= ang2D(Hip[i],Knee[i],Ankle[i])
	Angs2D["Ankle_Angle_2D"][i]= ang2D(Knee[i],Ankle[i],Toe[i])

print(Angs2D)

Angs2D.to_csv('2D_Angles_Computed.csv')