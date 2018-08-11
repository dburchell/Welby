# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 10:29:34 2017

@author: kerosene
"""

import mraa as m
from servolib import PWMDriver
from servoDriverConfig import ServoDriver
import welby_balance as wB
from SF_9DOF import IMU
from config import GYRO
from config import XM
import numpy as np
import quatMath as qM
import time
import pandas as pd

G=GYRO()
G.CTRL_REG1_G = 240
G.CTRL_REG2_G = 40

imu = IMU()
imu.initialize()
imu.enable_gyro()
imu.gyro_range("2000DPS")
    
iterations = 10
period = 5
exes = [0]*period*iterations
wyes = [0]*period*iterations
zees = [0]*period*iterations
its = {'avg exes': [0]*iterations, 'avg wyes': [0]*iterations, 'avg zees': [0]*iterations,}
angles = {'exes': exes,'wyes': wyes,'zees': zees} 
df = pd.DataFrame(angles)
averages = pd.DataFrame(its)       

dfpath = r'Welby:/home/welbyFiles/welby_files/rawdata.csv'
avgpath = r'Welby:/home/welbyFiles/welby_files/avgs.csv'

for j in range(5,5,5):
    period = j
    for x in range(0,iterations):
        for i in range(0,period):
            imu.read_gyro()
            #print "Accel: " + str(imu.ax) + ", " + str(imu.ay) + ", " + str(imu.az) 
            #print "Mag: " + str(imu.mx) + ", " + str(imu.my) + ", " + str(imu.mz) 
            df.exes[period*x+i] = imu.gx*57.295
            df.wyes[period*x+i] = imu.gy*57.295
            df.zees[period*x+i] = imu.gz*57.295        
            #print "Gyro: " + str(imu.gx) + ", " + str(imu.gy) + ", " + str(imu.gz) 
            #print "Temperature: " + str(imu.temp) 
            time.sleep(0.01)
            averages['avg exes'][x] = np.mean(df.exes[x:x+period])
            averages['avg wyes'][x] = np.mean(df.wyes[x:x+period])
            averages['avg zees'][x] = np.mean(df.zees[x:x+period])
    
    df.to_csv('data/rawdata'+str(period)+'.csv')
    averages.to_csv('data/avgs'+str(period)+'.csv');
    
    

 
#print "AVERAGED ANGLES: " + str(its)

#def listAngles():
#    imu = IMU()
#    imu.initialize()
#    imu.enable_gyro()
#    imu.gyro_range("2000DPS")    
#    i=1    
#    while i==1:
#        time.sleep(2)
#        print(qM.getEuler()*57.296)        
        
for x in range(0,iterations):
    for i in range(0,period):
        imu.read_gyro()
        #print "Accel: " + str(imu.ax) + ", " + str(imu.ay) + ", " + str(imu.az) 
        #print "Mag: " + str(imu.mx) + ", " + str(imu.my) + ", " + str(imu.mz) 
        df.exes[period*x+i] = imu.gx*57.295
        df.wyes[period*x+i] = imu.gy*57.295
        df.zees[period*x+i] = imu.gz*57.295        
        #print "Gyro: " + str(imu.gx) + ", " + str(imu.gy) + ", " + str(imu.gz) 
        #print "Temperature: " + str(imu.temp) 
        time.sleep(0.01)
        averages['avg exes'][x] = np.mean(df.exes[x:x+period])
        averages['avg wyes'][x] = np.mean(df.wyes[x:x+period])
        averages['avg zees'][x] = np.mean(df.zees[x:x+period])

df.to_csv('data/rawdata'+str(period)+'.csv')
averages.to_csv('data/avgs'+str(period)+'.csv')        