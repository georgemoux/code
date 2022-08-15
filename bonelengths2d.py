import os
import numpy as np
import pandas as pd
import statistics as stats
from matplotlib import pyplot as plt

curdir = os.getcwd()


def FemurLength(Hx,Hy,Kx,Ky) :
    Fem = np.sqrt(((Kx-Hx)**2)+((Ky-Hy)**2))
    return Fem

def FibulaLength(Kx,Ky,Ax,Ay):
    Fib = np.sqrt(((Ax-Kx)**2)+((Ay-Ky)**2))
    return Fib 


files=[]
cols = ['Coord','rat','type','date','csv']

for file in os.listdir():
    if file.startswith("Coord"):
        file=file.split('.')
        files.append(file)

files=pd.DataFrame(files,columns=cols)

files=files.sort_values('date') #this helps me sort values so i have the same trials (skin then tattoo) next to each other

sortedfiles = []

for i in range(files.shape[0]):
    sortedfiles.append('.'.join(files.iloc[i])) #here i place the same trials in pairs skin then tattoo and so on


#now that i have my data tidied up I can finally load skin and tattoo data
# I will do it in increments of 2

for x in range(0,len(sortedfiles),2):
    if 'tat' in sortedfiles[x]:
        TD = pd.read_csv(sortedfiles[x])
        SD = pd.read_csv(sortedfiles[x+1])

    elif 'skin' in sortedfiles[x]:
        SD = pd.read_csv(sortedfiles[x])
        TD = pd.read_csv(sortedfiles[x+1])

    print('using files ',sortedfiles[x],sortedfiles[x+1])

    skinfem = FemurLength(SD['Hip_x'],SD['Hip_y'],SD['Knee_x'],SD['Knee_y'])
    skinfib = FibulaLength(SD['Knee_x'],SD['Knee_y'],SD['Ankle_x'],SD['Ankle_y'])

    tatfem = FemurLength(TD['Hip_x'],TD['Hip_y'],TD['Knee_x'],TD['Knee_y'])
    tatfib = FibulaLength(TD['Knee_x'],TD['Knee_y'],TD['Ankle_x'],TD['Ankle_y'])

    plt.plot(range(len(skinfem)),skinfem,range(len(tatfem)),tatfem)
    plt.show()

    plt.plot(range(len(skinfib)),skinfib,range(len(tatfib)),tatfib)
    plt.show()