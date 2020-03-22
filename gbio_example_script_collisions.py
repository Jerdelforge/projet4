# -*- coding: utf-8 -*-
"""
Example script for processing and plotting GLM data
The script uses the data of an oscillation task performed with the 
manipulandum (file TEST_DATA.glm)

Created on Wed Jan 29 11:16:06 2020

@author: opsomerl & fschiltz
"""
#%% Importation des librairies necessaires
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

import glm_data_processing as glm
import derive as der

# Fermeture des figures ouvertes
plt.close('all')

subjects = ["Achille1","Achille2"] #Names of subjects
ntrials = 6 #Number of trials for each subject

# Double for-loop that runs thrgough all subjects and trials
subject_number=2;
for s in subjects:
    for trial in range(1,ntrials+1): 
        # Set data path
        glm_path = "gbio2\%s_%d_001.glm" % (s,trial)
        
        # Import data 
        glm_df = glm.import_data(glm_path)
        
        baseline = range(0,400)        
        # Normal Force exerted by the thumb
        NF_thumb = glm_df.loc[:,'Fygl']-np.nanmean(glm_df.loc[baseline,'Fygl'])
        # Vertical Tangential Force exerted by the thumb
        TFx_thumb  = glm_df.loc[:,'Fxgl']-np.nanmean(glm_df.loc[baseline,'Fxgl'])
        #Horizontal Tangential Force exerted by the thumb
        TFz_thumb  = glm_df.loc[:,'Fzgl']-np.nanmean(glm_df.loc[baseline,'Fzgl'])


        # Normal Force exerted by the index
        NF_index = -(glm_df.loc[:,'Fygr']-np.nanmean(glm_df.loc[baseline,'Fygr']))
        # Vertical Tangential Force exerted by the index
        TFx_index = glm_df.loc[:,'Fxgr']-np.nanmean(glm_df.loc[baseline,'Fxgr'])
        #Horizontal Tangential Force exerted by the index
        TFz_index = glm_df.loc[:,'Fzgr']-np.nanmean(glm_df.loc[baseline,'Fzgr'])
        
        
        
        #%% Get acceleration, LF and GF
        time  = glm_df.loc[:,'time'].to_numpy()
        accX  = glm_df.loc[:,'LowAcc_X'].to_numpy()*(-9.81)
        accX  = accX-np.nanmean(accX[baseline])
        GF    = glm_df.loc[:,'GF'].to_numpy()
        GF    = GF-np.nanmean(GF[baseline])
        LFv   = TFx_thumb+TFx_index
        LFh   = TFz_thumb+TFz_index
        LF    = np.hypot(LFv,LFh)
        
        # %%Filter data
        freqAcq=800 #Frequence d'acquisition des donnees
        freqFiltAcc=20 #Frequence de coupure de l'acceleration
        freqFiltForces=20 #Frequence de coupure des forces

        accX = glm.filter_signal(accX, fs = freqAcq, fc = freqFiltAcc)
        GF   = glm.filter_signal(GF,   fs = freqAcq, fc = freqFiltForces)
        LF   = glm.filter_signal(LF,   fs = freqAcq, fc = freqFiltForces)
        LFv   = glm.filter_signal(LFv,   fs = freqAcq, fc = freqFiltForces)
        LFh   = glm.filter_signal(LFh,   fs = freqAcq, fc = freqFiltForces)
        
        #%% CUTTING THE TASK INTO SEGMENTS (your first task)
        pk = signal.find_peaks(abs(accX),  prominence=9,distance=400)
        ipk = pk[0]
        cycle_starts = ipk-400
        cycle_ends = ipk+200
        
        #%% Compute derivative of LF
        dGF=der.derive(GF,800)
        dGF=glm.filter_signal(dGF,   fs = freqAcq, fc = 10)
        
        #%% Basic plot of the data
        fig = plt.figure(figsize = [15,7])
        ax  = fig.subplots(3,1)
        
        ax[0].plot(time, accX)
        ax[0].plot(time[ipk],accX[ipk], linestyle='', marker='o', 
                   markerfacecolor='None', markeredgecolor='r')
        ax[0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
        ax[0].set_title("Simple example of GLM data", fontsize=14, fontweight="bold")
        ax[0].set_xlim([0,45])
        
        # Putting grey patches for cycles
        for i in range(0,len(cycle_starts)):
            rect0=plt.Rectangle((time[cycle_starts[i]],ax[0].get_ylim()[0]),\
                               time[cycle_ends[i]-cycle_starts[i]],\
                               ax[0].get_ylim()[1]-ax[0].get_ylim()[0],color='k',alpha=0.3)
            ax[0].add_patch(rect0)
        
        ax[1].plot(time,LF, label="LF")
        ax[1].plot(time,GF, label="GF")
        ax[1].legend(fontsize=12)
        ax[1].set_xlabel("Time [s]", fontsize=13)
        ax[1].set_ylabel("Forces [N]", fontsize=13)
        ax[1].set_xlim([0,45])
        
        ax[2].plot(time,dGF)
        ax[2].set_xlabel("Time [s]", fontsize=13)
        ax[2].set_ylabel("GF derivative [N/s]", fontsize=13)
        ax[2].set_xlim([0,45])
    
        #%% Save the figure as png file. Creates a folder "figures" first if it
        # doesn't exist
        if not os.path.exists('figures'):
            os.makedirs('figures')
        
        fig.savefig("figures\%s_%d_acc_forces_dGF.png" %(s,trial))
        

        
    
    
