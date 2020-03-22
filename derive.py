# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:47:20 2020

@author: fschiltz
"""
import numpy as np
def derive(sig,freq):
#DERIVE Computes the derivative of the input signal.
#
# Syntax: out = derive(sig,freq)        column-wise derivative
#
# Inputs:
#   sig           input signal
#   freq          sample frequency
#
# Outputs:
#   out           derivative of input signal


    # process inputs
    q = round(0.01*freq);
    denom = 2 /freq * sum(np.square((np.linspace(1,q))));
    #compute derivative
    #out=zeros(siz);

    out = -np.convolve(sig,np.linspace(-q,q),'same')/denom;

    #out([1:q end-q+1:end],:)=nan;
    return out