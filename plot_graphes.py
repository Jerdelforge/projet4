# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:54:49 2020

@author: Jérôme
"""

import matplotlib.pyplot as plt
import numpy as np


plt.close('all')

def basic_plot(time, accX, ipk, cycle_starts, cycle_ends, LF, GF, dGF, s, trial) :
    fig = plt.figure(figsize = [15,7])
    ax = fig.subplots(3,1)
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
    
    fig.savefig("figures\%s_%d_acc_forces_dGF.png" %(s,trial))
    
    

def plot_segments(GF, LF, cycle_starts, cycle_ends) :
    plt.figure(figsize = [15,7])
    plt.axis([0,620, 0, 120])
    #rapport = GF/LF
    for i in range(0,len(cycle_starts)-1):
        if i<10 :
            col = "b"
        else :
            col = "r"
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), rapport[cycle_starts[i]:cycle_ends[i]],color = col, label = i)
        plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), GF[cycle_starts[i]:cycle_ends[i]],color = col, label = i)
        plt.legend(fontsize=12)



def plot_diff_samecond(time, rapport, n) :
    fig = plt.figure(figsize = [15,7*n])
    ax = fig.subplots(n,1)
    col = ['b', 'r', 'g', 'c', 'm', 'y']
    for i in range(0,n):
        lab = "condition " + str(i)
        ax[i].plot(time,(rapport[n+i]-rapport[i]), color = col[i], label = lab)
        ax[i].plot(time,np.zeros(28000),"k")
        ax[i].legend(fontsize=12)
        
        
def plot_diff_position(time, Acctab, GFtab, n) :
    for i in range(0, n-1) : 
        fig = plt.figure(figsize = [15,14])
        ax = fig.subplots(2, 1)
        ax[0].plot(time, GFtab[i], label = " GF tete en bas "+str(i+1))
        ax[0].plot(time, GFtab[i+1], label = "GF tete en haut "+str(i+2))
        ax[0].legend(fontsize=12)
        ax[1].plot(time, Acctab[i], label = "Acc tete en bas "+str(i+1))
        ax[1].plot(time, Acctab[i+1], label = "Acc tete en haut "+str(i+2))
        ax[1].legend(fontsize=12)
        i+=2