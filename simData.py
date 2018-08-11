# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 19:47:14 2017

@author: kerosene
"""

import random

def randomPosition():
    maxROM = 160
    minROM = 665
    for i in range(0,7):
        sA[i] = (maxROM-minROM)*random.random()+minROM
    
    return sA


def unbalPosition():
    maxROM = 272
    minROM = 228
    for i in range(0,7):
        sA[i] = (maxROM-minROM)*random.random()+minROM

def balPosition():
    

