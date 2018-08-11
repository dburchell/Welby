# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:27:11 2017

@author: kerosene
"""

import quatMath as qM
from SF_9DOF import IMU
from servolib import PWMDriver

def readGyroAngles():
    # Read the gyroscope    
    imu=IMU()    # Default IC2 port 1
    imu.gyro_range("245DPS")    
    imu.read_gyro()
    angles = qM.getEuler()
    return Angles
    
def readServoAngles():# Read the servo angles, assuming 150 to 600 (out of 4096) is the servo ROM
    pwm=PWMDriver()
    minROM = 160    
    maxROM = 665
    sA = np.array([0,0,0,0,0,0,0,0])    
    for i in range(0, 8):
        sA[i] = (maxROM-minROM)*pwm.readPWM(i)/4096+minROM
    return sA