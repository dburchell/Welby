# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 17:14:49 2017

@author: kerosene
"""

from SF_9DOF import IMU
import numpy as np
import time
import pandas as pd
import pysftp
import os
import quatMath as qm

def initialize():
    imu = IMU()
    imu.initialize()
    imu.enable_gyro()
    imu.gyro_range("2000DPS")
    return imu

def collectRateSample(iterations=1, period=5, dfpath=r'/home/welbyFiles/welby_files/rawdata.csv', avgpath=r'/home/welbyFiles/welby_files/avgs.csv'):
    #imu = initialize()    
    exes = [0]*period*iterations
    wyes = [0]*period*iterations
    zees = [0]*period*iterations
    its = {'avg exes': [0]*iterations, 'avg wyes': [0]*iterations, 'avg zees': [0]*iterations,}
    angles = {'exes': exes,'wyes': wyes,'zees': zees} 
    df = pd.DataFrame(angles, dtype='float')
    averages = pd.DataFrame(its, dtype='float')
#   period = j    
#   for j in range(5,5,5):    
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
        df.to_csv(dfpath, float_format='%.3f')
        averages.to_csv(avgpath, float_format='%.3f');

def collectAngleSample(iterations=1, period=5, dfpath=r'/home/welbyFiles/welby_files/rawdata.csv', avgpath=r'/home/welbyFiles/welby_files/avgs.csv'):
    #imu = initialize()    
    exes = [0]*period*iterations
    wyes = [0]*period*iterations
    zees = [0]*period*iterations
    its = {'avg exes': [0]*iterations, 'avg wyes': [0]*iterations, 'avg zees': [0]*iterations,}
    angles = {'exes': exes,'wyes': wyes,'zees': zees} 
    df = pd.DataFrame(angles, dtype='float')
    averages = pd.DataFrame(its, dtype='float')
#   period = j    
#   for j in range(5,5,5):    
    for x in range(0,iterations):
        for i in range(0,period):
            ypr = qm.getEuler()
            #print "Accel: " + str(imu.ax) + ", " + str(imu.ay) + ", " + str(imu.az) 
            #print "Mag: " + str(imu.mx) + ", " + str(imu.my) + ", " + str(imu.mz) 
            df.exes[period*x+i] = ypr[0]
            df.wyes[period*x+i] = ypr[1]
            df.zees[period*x+i] = ypr[2]      
            #print "Gyro: " + str(imu.gx) + ", " + str(imu.gy) + ", " + str(imu.gz) 
            #print "Temperature: " + str(imu.temp) 
            time.sleep(0.01)
            averages['avg exes'][x] = np.mean(df.exes[x:x+period])
            averages['avg wyes'][x] = np.mean(df.wyes[x:x+period])
            averages['avg zees'][x] = np.mean(df.zees[x:x+period])
        df.to_csv(dfpath, float_format='%.3f')
        averages.to_csv(avgpath, float_format='%.3f');

def sendData(dfpath=r'/home/welbyFiles/welby_files/rawdata.csv', avgpath=r'/home/welbyFiles/welby_files/avgs.csv'):
    with pysftp.Connection('192.168.1.170', username='kerosene', password='Seventeen17*') as sftp:
        with sftp.cd(r'/home/kerosene/welby_files/logFiles'):             # temporarily chdir to logFiles
        #with sftp.cd('logFiles'):             # temporarily chdir to logFiles
            sftp.put(dfpath)
            sftp.put(avgpath)
            #sftp.close()
            
def clearData( dfpath=r'/home/welbyFiles/welby_files/rawdata.csv', avgpath=r'/home/welbyFiles/welby_files/avgs.csv'):
    os.remove(dfpath)    
    os.remove(avgpath)
    
def streamRateData(duration = 50):
    collectRateSample(period = duration)
    sendData()    
    clearData()

def streamAngleData(duration = 50):
    collectAngleSample(period = duration)
    sendData()    
    clearData()
    
    