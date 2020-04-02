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
    
    

def plot_segments(GF, LF, AccX, cycle_starts, cycle_ends, s, trial) :
    fig = plt.figure(figsize = [15,7])
    plt.axis([0,620, -50, 50])
    #rapport = GF/LF
    for i in range(0,len(cycle_starts)-1):
        if i == 0 :
            col = "g"
        elif i%2 :
            col = "b"
        else :
            col = "r"
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), rapport[cycle_starts[i]:cycle_ends[i]],color = col, label = i)
        plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), GF[cycle_starts[i]:cycle_ends[i]],color = col, label = i)
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), AccX[cycle_starts[i]:cycle_ends[i]],color = col, label = i)
        plt.legend(fontsize=12)
        
        fig.savefig("figures\%s_%d_acc_segments.png" %(s,trial))



def plot_diff_samecond(time, rapport, n) :
    fig = plt.figure(figsize = [15,7*n])
    ax = fig.subplots(n,1)
    col = ['b', 'r', 'g', 'c', 'm', 'y']
    for i in range(0,n):
        lab = "condition " + str(i)
        ax[i].plot(time,(rapport[n+i]-rapport[i]), color = col[i], label = lab)
        ax[i].plot(time,np.zeros(28000),"k")
        ax[i].legend(fontsize=12)
        
"""       
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
"""   
def plot_diff_position(time, Acctab, GFtab, LFtab, n) :
    fig = plt.figure(figsize = [15,21])
    axs = fig.subplots(9,1)
    for i in range(0, n) :
       
        if i%2 :
            lab = "tete en haut"
        else :
            lab = "tete en bas"
        axs[int(i/2)].plot(time, GFtab[i], label = lab)
        axs[(int(n/2)+int(i/2))].plot(time, Acctab[i], label = lab)
        axs[int(n) + int(i/2)].plot(time, LFtab[i], label = lab)
        axs[int(i/2)].legend(fontsize=12)
        axs[(int(n/2)+int(i/2))].legend(fontsize=12)
        axs[(int(n)+int(i/2))].legend(fontsize=12)
    axs[0].set_title('Bandeau')
    axs[1].set_title('Lunette')       
    axs[2].set_title('Vision')
    axs[3].set_title('Bandeau')
    axs[4].set_title('Lunette')       
    axs[5].set_title('Vision')
    axs[6].set_title('Bandeau')
    axs[7].set_title('Lunette')       
    axs[8].set_title('Vision')
    axs[0].set_ylabel('GF')
    axs[1].set_ylabel('GF')
    axs[2].set_ylabel('GF')
    axs[3].set_ylabel('Acc')
    axs[4].set_ylabel('Acc')
    axs[5].set_ylabel('Acc')
    axs[6].set_ylabel('LF')
    axs[7].set_ylabel('LF')
    axs[8].set_ylabel('LF')
    
    
def plot_diff_pos2(time, GFtab) :
    fig = plt.figure(figsize = [15,14])
    ax = fig.subplots(3,1)
    ax[0].plot(time, GFtab[1]-GFtab[0])
    ax[0].plot(time,np.zeros(28000),"k")
    ax[1].plot(time, GFtab[3]-GFtab[2])
    ax[1].plot(time,np.zeros(28000),"k")
    ax[2].plot(time, GFtab[5]-GFtab[4])
    ax[2].plot(time,np.zeros(28000),"k")
    ax[0].set_title('Bandeau tete en haut - tete en bas')
    ax[1].set_title('Lunette tete en haut - tete en bas')       
    ax[2].set_title('Classique tete en haut - tete en bas')
    