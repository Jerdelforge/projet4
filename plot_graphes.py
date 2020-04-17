# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:54:49 2020

@author: Jérôme
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


Condition=["Bandeau Bas","Bandeau Haut","Lunette Bas","Lunette Haut","Classique Bas","Classique Haut"]
def basic_plot(time, accX, ipk, cycle_starts, cycle_ends, LF, GF, dGF, s, trial) :
    fig = plt.figure(figsize = [15,7])
    ax = fig.subplots(3,1)
    ax[0].plot(time, accX)
    ax[0].plot(time[ipk],accX[ipk], linestyle='', marker='o', 
                  markerfacecolor='None', markeredgecolor='r')
    ax[0].set_ylabel("Acceleration [m/s^2]", fontsize=13)
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
    
    if trial<=2 :
        vue = "Bandeau"
    elif trial <= 4 :
        vue = "Lunettes"
    else :
        vue = "Normal"
    if trial%2 :
        tete = "Tête en bas"
    else :
        tete = "Tête en haut"
    ax[0].set_title("%s, %s %s" %(s, vue, tete))
    
    fig.savefig("figures\%s_%d_acc_forces_dGF.png" %(s,trial))
    
    

def plot_segments(GF, LF, AccX, dAcc, cycle_starts, cycle_ends, s, trial, j) :
    fig = plt.figure(figsize = [15,7])
    plt.axis([0,600, -10, 30])
    #rapport = GF/LF
    for i in range(0,len(cycle_starts)-1):
        if (i+j)%2 == 0:
            col = "b"
            lab = "Collision en bas"
        else :
            col = "r"
            lab = "Collision en haut"
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), dAcc[cycle_starts[i]:cycle_ends[i]],color = col, label = lab)
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), GF[cycle_starts[i]:cycle_ends[i]]/LF[cycle_starts[i]:cycle_ends[i]],color = col, label = lab)
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), AccX[cycle_starts[i]:cycle_ends[i]],color = col, label = lab)
        plt.plot(np.full(80, 400), range(-40,40))
    if i == 0 or i==1 :
        plt.legend(fontsize=12)
    if trial<=2 :
        vue = "Bandeau"
    elif trial <= 4 :
        vue = "Lunettes"
    else :
        vue = "Normal"
    if trial%2 :
        tete = "Tête en bas"
    else :
        tete = "Tête en haut"
    plt.title("%s, %s %s" %(s, vue, tete))
        
        #fig.savefig("figures\%s_%d_GF_segments.png" %(s,trial))

def plot_segmentsmeanCol(GF, LF, AccX, dAcc, cycle_starts, cycle_ends, s, trial, j) :
    fig = plt.figure(figsize = [15,7])
    plt.axis([0,600, -10, 30])
    #rapport = GF/LF
    mean1 = np.zeros(600)
    mean2 = np.zeros(600)
    col1 = "b"
    lab1 = "Collision en bas"
    col2 = "r"
    lab2 = "Collision en haut"
    for i in range(0,len(cycle_starts)-1):
        if (i+j)%2 == 0:
            mean1 = (mean1 + GF[cycle_starts[i]:cycle_ends[i]]/LF[cycle_starts[i]:cycle_ends[i]])/2
        else :
            mean2 = (mean2 + GF[cycle_starts[i]:cycle_ends[i]]/LF[cycle_starts[i]:cycle_ends[i]])/2
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), dAcc[cycle_starts[i]:cycle_ends[i]],color = col, label = lab)
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), GF[cycle_starts[i]:cycle_ends[i]]/LF[cycle_starts[i]:cycle_ends[i]],color = col, label = lab)
        #plt.plot(range(0,cycle_ends[i]-cycle_starts[i]), AccX[cycle_starts[i]:cycle_ends[i]],color = col, label = lab)
    plt.plot(np.full(80, 400), range(-40,40))
        
    if trial<=2 :
        vue = "Bandeau"
    elif trial <= 4 :
        vue = "Lunettes"
    else :
        vue = "Normal"
    if trial%2 :
        tete = "Tête en bas"
    else :
        tete = "Tête en haut"
    plt.plot(range(600), mean1, col1, label = lab1)
    plt.plot(range(600), mean2, col2, label = lab2)
    plt.title("%s, %s %s" %(s, vue, tete))
    plt.legend(fontsize=12)    
        #fig.savefig("figures\%s_%d_GF_segments.png" %(s,trial))



def plot_segmentsmeanGF(GFtab,trials,subjects,ipktab):#différencie vision
    fig = plt.figure(figsize = [15,10])
    ax = fig.subplots()
    
    for x in range(0,len(trials)):
        GFsegmean=np.zeros(shape=(6,600))
        
        w=0
        while(w<len(subjects)):
            cycle_starts=ipktab[6*w+x]-400
            cycle_ends=ipktab[6*w+x]+200
            for i in range(0,len(cycle_starts)-1):
                GFsegmean[x]=(GFsegmean[x]+(GFtab[6*w+x,cycle_starts[i]:cycle_ends[i]]))/2
            w=w+1
        print(GFsegmean)
        ax.plot(range(0,cycle_ends[x]-cycle_starts[x]), GFsegmean[x],label = Condition[x])
        ax.vlines(400, ymin=0, ymax=35, linewidth=1, color='k')
        ax.set_title("%s-%s"%(subjects[0],subjects[-1]))
        ax.legend(fontsize=12)
        #ax.set_xlim([300,600])
        ax.set_ylim([-5,35])


def plot_segmentsmeanAllStar(datab,trial,subjects,ipktab):#différencie vision
    fig = plt.figure(figsize = [15,10])
    ax = fig.subplots()
    
    for x in range(0,len(subjects)):
        GFsegmean=np.zeros(shape=(6,600))
        
        w=0
        while(w<6):
            cycle_starts=ipktab[w+6*x]-400
            cycle_ends=ipktab[w+6*x]+200
            #cycle_starts1=ipktab[w+6*x]-400
            #cycle_ends1=ipktab[w+6*x]+200
            for i in range(0,len(cycle_starts)-1):
                GFsegmean[w]=(GFsegmean[w]+(datab[w+6*x,cycle_starts[i]:cycle_ends[i]]))/2
            ax.plot(range(0,cycle_ends[w]-cycle_starts[w]), GFsegmean[w], label = Condition[w])
            w=w+1
        print(GFsegmean)
        
        
        ax.vlines(400, ymin=0, ymax=30, linewidth=1, color='k')
        color=[plt.Line2D([0],[0],color='b', lw=3),Line2D([0],[0],color='r', lw=3),Line2D([0],[0],color='g', lw=3)]
        ax.set_title("%s-%s"%(subjects[0],subjects[-1]))
        ax.legend(fontsize=12)
        #ax.set_xlim([300,600])
        #ax.set_ylim([-5,20])



def plot_segmentsmeanGFHB(GFtab,trial,subjects,ipktab):#Différencie H/B
    fig = plt.figure(figsize = [20,15])
    ax = fig.subplots()
    GFsegmean=np.zeros(shape=(2,600))
    for x in range(0,len(subjects)):
        j=0
        for w in range(0,2):
            cycle_starts=ipktab[w+6*x]-400
            cycle_ends=ipktab[w+6*x]+200
            cycle_starts1=ipktab[(w+2)+6*x]-400
            cycle_ends1=ipktab[(w+2)+6*x]+200
            cycle_starts2=ipktab[(w+4)+6*x]-400
            cycle_ends2=ipktab[(w+4)+6*x]+200
            for i in range(0,len(cycle_starts)-1):
                GFsegmean[j]=(GFsegmean[j]+(GFtab[w+6*x,cycle_starts[i]:cycle_ends[i]]+GFtab[(w+2)+6*x,cycle_starts1[i]:cycle_ends1[i]]+GFtab[(w+2)+6*x,cycle_starts2[i]:cycle_ends2[i]])/3)/2
            j=j+1
        print(GFsegmean)           
        for i in range(0,2):
            if (i==0):
                col='r'
            else:
                col='g'
            ax.plot(range(0,cycle_ends[i]-cycle_starts[i]), GFsegmean[i],color = col, label = Condition[2*i])
        ax.vlines(400, ymin=0, ymax=60, linewidth=1, color='k')
        color=[plt.Line2D([0],[0],color='r', lw=3),Line2D([0],[0],color='g', lw=3),Line2D([0],[0],color='b', lw=3)]
        ax.set_title("%s-%s"%(subjects[0],subjects[-1]))
        ax.legend(color,['Bas','Haut'])
        #ax.set_xlim([300,600])
        #ax.set_ylim([0,60])  


def plot_diff_samecond(time, rapport, n) :
    fig = plt.figure(figsize = [15,7*n])
    ax = fig.subplots(n,1)
    col = ['b', 'r', 'g', 'c', 'm', 'y']
    for i in range(0,n):
        lab = "condition " + str(i+1)
        ax[i].plot(time,(rapport[n+i]-rapport[i]), color = col[i], label = lab)
        ax[i].plot(time,np.zeros(28000),"k")
        ax[i].legend(fontsize=12)
        

def plot_diff_position(time, Acctab, GFtab, LFtab, rapporttab, n, s) :
    fig = plt.figure(figsize = [15,30])
    axs = fig.subplots(9,1)
    #axs[0].axis([0, 35, -50, 50])
    #axs[1].axis([0, 35, -50, 50])
    #axs[2].axis([0, 35, -50, 50])
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
    axs[2].set_title('Normal')
    axs[3].set_title('Bandeau')
    axs[4].set_title('Lunette')       
    axs[5].set_title('Normal')
    axs[6].set_title('Bandeau')
    axs[7].set_title('Lunette')       
    axs[8].set_title('Normal')
    axs[0].set_ylabel('GF')
    axs[1].set_ylabel('GF')
    axs[2].set_ylabel('GF')
    axs[3].set_ylabel('Acc')
    axs[4].set_ylabel('Acc')
    axs[5].set_ylabel('Acc')
    axs[6].set_ylabel('LF')
    axs[7].set_ylabel('LF')
    axs[8].set_ylabel('LF')
    
    fig.savefig("figures\%s_GF_diffTeteHautBas.png" %(s))
    
    
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
    