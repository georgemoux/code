import pandas as pd
import cv2
import numpy as np
from shutil import copyfile
import os, sys
from os import path
from glob import glob
import fileinput
import pdb
from termcolor import colored, cprint
import statistics as stat
from scipy.stats import iqr
from scipy import stats as st


cwd = os.getcwd()

print('first lets print dirs')

dirhome=[]
dirrat=[]
dircam=[]
dirdate=[]
dirweek=[]
res=[]

for root,dirs,files in os.walk(cwd):

    if  files:
        root1 = os.path.split(root)       
        root2 = os.path.split(root1[0]) #gives me rat as second element       
        root3 = os.path.split(root2[0]) #gives me cam as second element     
        root4 = os.path.split(root3[0]) #gives me week as second element
        root4=list(root4)

        root4.extend([(root3[1]),(root2[1]),(root1[1])])                

        #zipping then extending the directories
        dirhome.extend(list(zip([root4[0]]*4, files)))
        dirweek.extend(list(zip([root4[1]]*4, files)))
        dircam.extend(list(zip([root3[1]]*4, files)))
        dirrat.extend(list(zip([root2[1]]*4, files)))
        dirdate.extend(list(zip([root1[1]]*4, files)))

        res.extend(list([dirhome[0], dirweek[0], dircam[0], dirrat[0],dirdate[0],files]))

#converting the directories into single dataframes then merging them into a big dataframe called dir
dirhome=pd.DataFrame(dirhome,columns=['folder','files'])
dirweek=pd.DataFrame(dirweek,columns=['week','files'])
dircam = pd.DataFrame(dircam,columns=['cam','files'])
dirrat= pd.DataFrame(dirrat,columns=['rat','files'])
dirdate= pd.DataFrame(dirdate,columns=['date','files'])

dir = pd.concat([dirhome['folder'],dirweek['week'],dircam['cam'],dirrat['rat'],dirdate['date'],dirdate['files']],axis=1)

#removing directories containing other files
dir = dir[dir.rat.str.find('rat') != -1]

fileo = dir.files == 'metadata.csv'


print(dir.date[fileo])




fdir=dir[(dir.files=='cam3_DLC.csv') |( dir.files=='cam1_DLC.csv')]

summarycols = ["Asus", "Hip", "Knee","Ankle","Toe"]
statrows = ['Bad Frames','Median','Mode','IQR','Max']
coordsummary=np.empty([len(fdir),5])
coordsummary=pd.DataFrame(coordsummary,columns=summarycols)



for k in range(len(fdir)):

    print('k',k)

    #pathcam = os.path.join(os.sep,dir.folder[fileo][i],dir.week[fileo][i],dir.cam[fileo][i],dir.rat[fileo][i],dir.date[fileo][i])          

    pathcam = os.path.join(os.sep,fdir.folder.iat[k],fdir.week.iat[k],fdir.cam.iat[k],fdir.rat.iat[k],fdir.date.iat[k])          
    os.chdir(pathcam)
    print('current directory is')
    print(os.getcwd())
    
    



    ex3 = path.exists('cam3_DLC.csv') #CHANGE NAME TO ACTUAL CSV FILE
   # print("DLC file in cam 3 exists",ex3)
    ex4= path.exists('cam1_DLC.csv')

    if ex3 == True:
        coords = pd.read_csv('cam3_DLC.csv', skiprows=[0,1,2], sep=',', dtype={'ID': object})
        

    elif ex4 == True:
        coords = pd.read_csv('cam1_DLC.csv', skiprows=[0,1,2], sep=',', dtype={'ID': object})

    sizecoords=coords.shape[0]

    coordsummary.iat[k,0]=0;
    coordsummary.iat[k,1]=0;
    coordsummary.iat[k,2]=0;
    coordsummary.iat[k,3]=0;
    coordsummary.iat[k,4]=0;

 
    counter1=0 #asus counter
    counter2=0 #hip
    counter3=0 #knee
    counter4=0 #ankle
    counter5=0 #toe

    #print('coordsummary',coordsummary)            
    
    Xasus=[] #where counters are stored
    Xhip=[]
    Xknee=[]
    Xankle=[]
    Xtoe=[]

    for l in range(sizecoords):
 
        if l+1<sizecoords:
            
            if coords.iat[l,3] <0.95:
                coordsummary.iat[k,0]=coordsummary.iat[k,0]+1
                counter1=counter1+1


            if coords.iat[l,6] <0.95:
                coordsummary.iat[k,1]=coordsummary.iat[k,1]+1
                counter2=counter2+1

            if coords.iat[l,9] <0.95:
                coordsummary.iat[k,2]=coordsummary.iat[k,2]+1   
                counter3=counter3+1

            if coords.iat[l,12] <0.95:
                coordsummary.iat[k,3]=coordsummary.iat[k,3]+1
                counter4=counter4+1
            
            if coords.iat[l,15] <0.95:
                coordsummary.iat[k,4]=coordsummary.iat[k,4]+1
                counter5=counter5+1
            
            if counter1>0 and coords.iat[l+1,3]>0.95:
                Xasus.append(counter1)
                counter1=0

            if counter2>0 and coords.iat[l+1,6]>0.95:
                Xhip.append(counter2)
                counter2=0

            if counter3>0 and coords.iat[l+1,9]>0.95:
                Xknee.append(counter3)
                counter3=0

            if counter4>0 and coords.iat[l+1,12]>0.95:
                Xankle.append(counter4)
                counter4=0

            if counter5>0 and coords.iat[l+1,15]>0.95:
                Xtoe.append(counter5)
                counter5=0

    #pdb.set_trace()

    if not Xasus:
        statasus=(0,0,0,0,0)
    else:
        statasus=(sum(Xasus),stat.median(Xasus),int(st.mode(Xasus)[0]),iqr(Xasus),max(Xasus))

    if not Xhip:
        stathip=(0,0,0,0,0)
    else:
        stathip=(sum(Xhip),stat.median(Xhip),int(st.mode(Xhip)[0]),iqr(Xhip),max(Xhip))
    

    if not Xknee:
        statknee=(0,0,0,0,0)
    else:
        statknee=(sum(Xknee),stat.median(Xknee),int(st.mode(Xknee)[0]),iqr(Xknee),max(Xknee))
    
    if not Xankle:
        statankle=(0,0,0,0,0)
    else:
        statankle=(sum(Xankle),stat.median(Xankle),int(st.mode(Xankle)[0]),iqr(Xankle),max(Xankle))
    #pdb.set_trace()

    if not Xtoe:
        stattoe=(0,0,0,0,0)
    else:
        stattoe=(sum(Xtoe),stat.median(Xtoe),int(st.mode(Xtoe)[0]),iqr(Xtoe),max(Xtoe))

    statSum=np.array([statasus,stathip,statknee,statankle,stattoe])
    statSum=np.transpose(statSum)
   # print('np',statSum)

    statSum = pd.DataFrame(statSum,index=(statrows),columns=summarycols)
    #print('pd',statSum)

    statSum.to_csv('stats_on_summary.csv')
    #statSum=statSum.T
    #statSum= pd.DataFrame(statSum,columns=summarycols)
    
    #pdb.set_trace()
    #,columns=summarycols)
    

#    print('statsum',statSum)

   
 


vidz = pd.DataFrame([fdir.date],dtype=str)
camz = pd.DataFrame([fdir.cam],dtype=str)
ratz= pd.DataFrame([fdir.rat],dtype=str)
weekz=pd.DataFrame([fdir.week],dtype=str)
camz=camz.T
ratz=ratz.T
weekz=weekz.T
camz=camz.set_index([coordsummary.index.values])
vidz=vidz.T
vidz=vidz.set_index([coordsummary.index.values])
ratz=ratz.set_index([coordsummary.index.values])
weekz=weekz.set_index([coordsummary.index.values])


coordsummaryfinal = pd.concat([weekz,camz,ratz,vidz,coordsummary],axis=1)
                
print("summary",coordsummaryfinal)


os.chdir(cwd)
coordsummaryfinal.to_csv('DLC_Frames_summary.csv',index=False)