import os
import numpy as np
import pandas as pd
import statistics as stats

curdir = os.getcwd()

#variables for the hip, knee and ankle TD angles at touchdown and mid stride
hip0tat=[]
hip5tat=[]
knee0tat=[]
knee5tat=[]
ank0tat=[]
ank5tat=[]

#variables for the hip, knee and ankle SD angles at touchdown and mid stride
hip0skin=[]
hip5skin=[]
knee0skin=[]
knee5skin=[]
ank0skin=[]
ank5skin=[]


weektoanalyze = 'tattoo-marker'
for path, sub_directories, files in os.walk(curdir):
    for file in files:


        if len(os.path.split(path)[0].split("/")) <4:
            continue

        main_folder = os.path.split(path)[0].split("/")[-4]
        week = os.path.split(path)[0].split("/")[-3]
        cam = os.path.split(path)[0].split("/")[-2]
        rat = os.path.split(path)[0].split("/")[-1]
        dates = os.path.split(path)[1] #here are where the videos are located
        
        source = os.path.join(path,file)


        if file.endswith('00_00_00_00.csv'):
            if 'speed48' in source:            
                angdir= os.path.join(path,str(file))

                dat=pd.read_csv(angdir,index_col=False)

                dat_0 = dat[dat['Stride Percentage']==0] #selecting data of the touch down
                dat_50 = dat[dat['Stride Percentage']>0.55]
                dat_50 = dat_50[dat_50['Stride Percentage']<0.57] #selecting data in mid stride

                if 'retry-tat' in source:
                    print('processing tat data from',file)
                    hip0tat.append(dat_0['Angle Asis Hip Knee'])
                    hip5tat.append(dat_50['Angle Asis Hip Knee'])
                    knee0tat.append(dat_0['Angle Hip Knee Ankle'])
                    knee5tat.append(dat_50['Angle Hip Knee Ankle'])
                    ank0tat.append(dat_0['Angle Knee Ankle Toe'])
                    ank5tat.append(dat_50['Angle Knee Ankle Toe'])

                elif 'retry-skin' in source:
                    print('processing skin data from',file)
                    hip0skin.append(dat_0['Angle Asis Hip Knee'])
                    hip5skin.append(dat_50['Angle Asis Hip Knee'])
                    knee0skin.append(dat_0['Angle Hip Knee Ankle'])
                    knee5skin.append(dat_50['Angle Hip Knee Ankle'])
                    ank0skin.append(dat_0['Angle Knee Ankle Toe'])
                    ank5skin.append(dat_50['Angle Knee Ankle Toe'])
                        

indi=['mean','SD','meanVar']
colz=['HipTAT','KneeTAT','AnkTAT','HipSKIN','KneeSKIN','AnkSKIN']
Summary_Data = pd.DataFrame(columns=colz,index=indi)

Summary_Data['HipTAT']['mean']=stats.mean(hip0tat[1])
Summary_Data['HipTAT']['SD']=stats.stdev(hip0tat[1])
Summary_Data['HipTAT']['meanVar']=stats.mean(hip0tat[1])-stats.mean(hip5tat[1])

Summary_Data['HipSKIN']['mean']=stats.mean(hip0skin[1])
Summary_Data['HipSKIN']['SD']=stats.stdev(hip0skin[1])
Summary_Data['HipSKIN']['meanVar']=stats.mean(hip0skin[1])-stats.mean(hip5skin[1])

Summary_Data['KneeTAT']['mean']=stats.mean(knee0tat[1])
Summary_Data['KneeTAT']['SD']=stats.stdev(knee0tat[1])
Summary_Data['KneeTAT']['meanVar']=stats.mean(knee0tat[1])-stats.mean(knee5tat[1])

Summary_Data['KneeSKIN']['mean']=stats.mean(knee0skin[1])
Summary_Data['KneeSKIN']['SD']=stats.stdev(knee0skin[1])
Summary_Data['KneeSKIN']['meanVar']=stats.mean(knee0skin[1])-stats.mean(knee5skin[1])

Summary_Data['AnkTAT']['mean']=stats.mean(ank0tat[1])
Summary_Data['AnkTAT']['SD']=stats.stdev(ank0tat[1])
Summary_Data['AnkTAT']['meanVar']=stats.mean(ank0tat[1])-stats.mean(ank5tat[1])

Summary_Data['AnkSKIN']['mean']=stats.mean(ank0skin[1])
Summary_Data['AnkSKIN']['SD']=stats.stdev(ank0skin[1])
Summary_Data['AnkSKIN']['meanVar']=stats.mean(ank0skin[1])-stats.mean(ank5skin[1])


print('Finished analyzing the data and created the summary dataframe')
Summary_Data.to_csv('Summary_Data.csv',index=False)

#print('For the likelihood of the tattoo for',weektoanalyze,'the mean likelihood is: ',stats.mean(meanz),'the median likelihood is: ',stats.median(meanz),'and the mode is: ',stats.mode(meanz))