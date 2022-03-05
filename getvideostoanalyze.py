import os
import numpy as np


import tensorflow as tf
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

import deeplabcut as dlc

weektoanalyze='test'

curdir = os.getcwd()
vidz=[]
for path, sub_directories, files in os.walk(curdir):
    for file in files:


        if len(os.path.split(path)[0].split("/")) <4:
            continue

        main_folder = os.path.split(path)[0].split("/")[-4]
        week = os.path.split(path)[0].split("/")[-3]
        cam = os.path.split(path)[0].split("/")[-2]
        rat = os.path.split(path)[0].split("/")[-1]
        dates = os.path.split(path)[1] #here are where the videos are located
        #
        source = os.path.join(path,file)

        if file.endswith('safe.mp4'):
            if weektoanalyze in source: 
                viddir= os.path.join(path,str(file))
                vidz.append(viddir)

dlc.analyze_videos(configg,vidz,shuffle=1,save_as_csv=True)

dlc.create_labeled_video(configg,vidz,draw_skeleton=True)

dlc.plot_trajectories(configg,vidz)
