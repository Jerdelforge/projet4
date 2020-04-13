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
    j=0
    if acc[ipk[0]] < 0 :
        j=1
        
    
    rayon = 30
    for i in range(len(ipk)) :
        if (i+j)%2 == 0 :
            ipk[i] = np.where(acc[(ipk[i]-rayon):(ipk[i]+rayon)] == np.amax(acc[(ipk[i]-rayon):(ipk[i]+rayon)])) +ipk[i] -rayon
        else :
            ipk[i] = np.where(acc[(ipk[i]-rayon):(ipk[i]+rayon)] == np.amin(acc[(ipk[i]-rayon):(ipk[i]+rayon)])) +ipk[i] - rayon
    
    
    
    cycle_starts = ipk-400
    cycle_ends = ipk+200
    return ipk, cycle_starts, cycle_ends