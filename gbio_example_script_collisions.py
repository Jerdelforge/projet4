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

import glm_data_processing as glm
import derive as der
import plot_graphes as plot
import FindPeaks as fp

# Fermeture des figures ouvertes
plt.close('all')

subjects = ["Achille1"] #Names of subjects
trials = [1, 2, 3, 4, 5, 6] #Trials for each subject


longueur = 28000
rapporttab = np.zeros(shape=(len(trials)*len(subjects),longueur))
GFtab = np.zeros(shape=(len(trials)*len(subjects),longueur))
LFtab = np.zeros(shape=(len(trials)*len(subjects),longueur))
Acctab = np.zeros(shape=(len(trials)*len(subjects),longueur))
GFipktab = np.zeros(shape=(len(trials)*len(subjects)))

i=0
# Double for-loop that runs thrgough all subjects and trials
for s in subjects:
    
    #ax  = fig.subplots(1,1)
    for trial in trials: 
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
        clock  = glm_df.loc[:,'Metronome_b0'].to_numpy()
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
        
        #%% Compute derivative of LF
        dGF=der.derive(GF,800)
        dGF=glm.filter_signal(dGF,   fs = freqAcq, fc = 10)
        
        dLF=der.derive(LF,800)
        dLF=glm.filter_signal(dLF,   fs = freqAcq, fc = 10)
        
        dAcc=der.derive(accX,800)
        dAcc=glm.filter_signal(dAcc,   fs = freqAcq, fc = 10)
        
        
        #%% CUTTING THE TASK INTO SEGMENTS (your first task)
        #ipk, cycle_starts, cycle_ends = fp.FindPeaks(accX)
        #GF_ipk, GF_cs, GF_ce = fp.FindPeaks(GF)
        ipk, cycle_starts, cycle_ends = fp.FindPeaks(dLF, accX)
        #dAcc_ipk, dAcc_cs, dAcc_ce = fp.FindPeaks(dAcc)
        #ipk, cycle_starts, cycle_ends = dLF_ipk, dLF_cs, dLF_ce
        
        rapporttab[i] = GF/LF
        Acctab[len(trials)-1] = accX
        GFtab[len(trials)-1] = GF
        LFtab[len(trials)-1] = LF
        
        i=i+1
        #%% Basic plot of the data
        
        #plt.figure(figsize = [15,7])
        #plt.plot(time, clock)
        
        plot.basic_plot(time, accX, ipk, cycle_starts, cycle_ends, LF, GF, dGF, s, trial)
        
        plot.plot_segments(GF, LF, accX, cycle_starts, cycle_ends, s, trial)
        
    #plot.plot_diff_position(time, Acctab, GFtab, LFtab, rapporttab, len(trials), s)
    #plot.plot_diff_pos2(time, GFtab)
#plot.plot_diff_samecond(time, rapporttab, len(trials))
        
        
        #%% Save the figure as png file. Creates a folder "figures" first if it
        # doesn't exist
        #if not os.path.exists('figures'):
        #    os.makedirs('figures')
        

        
    
    
