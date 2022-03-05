import os
import numpy as np
import pandas as pd
import statistics as stats

curdir = os.getcwd()
meanz=[]

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

        if file.endswith('000.csv'):
            if weektoanalyze in source:            
                likedir= os.path.join(path,str(file))
                #print(likedir[:,1])

                dat=pd.read_csv(likedir,skiprows=2)
                meantatlik = dat.iloc[:,3].mean()
                meanz.append(meantatlik)

#print('The average likelihood of the tattoo for',weektoanalyze,'is: ',stats.mean(meanz))

print('For the likelihood of the tattoo for',weektoanalyze,'the mean likelihood is: ',stats.mean(meanz),'the median likelihood is: ',stats.median(meanz),'and the mode is: ',stats.mode(meanz))