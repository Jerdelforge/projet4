# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 17:26:02 2020

@author: Jérôme
"""

import numpy as np
from scipy import signal


def FindPeaks(var, acc) :
    pk = signal.find_peaks(var,  prominence=10,distance=700)
    ipk = pk[0]
    k = 0
    #print(ipk)
        
    while ipk[k] < 4800 :
            k = k+1
    ipk = np.delete(ipk, range(0, k))
    #print(ipk)
    
    rayon = 25
    for i in range(len(ipk)) :
        #print(str(ipk[i]) + " : " + str(acc[ipk[i]]))
        #print(np.amax(np.abs(acc[(ipk[i]-rayon):(ipk[i]+rayon)])))
        #print(np.where(np.abs(acc[(ipk[i]-rayon):(ipk[i]+rayon)]) == np.amax(np.abs(acc[(ipk[i]-rayon):(ipk[i]+rayon)]))))
        ipk[i] = np.where(np.abs(acc[(ipk[i]):(ipk[i]+rayon)]) == np.amax(np.abs(acc[(ipk[i]):(ipk[i]+rayon)]))) +ipk[i]
        #print(str(ipk[i]) + " : " + str(acc[ipk[i]]))
        #print("---")
        
    
    cycle_starts = ipk-400
    cycle_ends = ipk+200
    return ipk, cycle_starts, cycle_ends