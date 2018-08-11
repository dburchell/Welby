# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
#import quatMath as qM
#from SF_9DOF import IMU
#from servolib import PWMDriver


    
#Contains functions for rotations about axes"        
def Rx(point, angle):
    # Rotates point about the x-axis by angle. 
    rx = np.array([[1,0,0,0],
                   [0,np.cos(angle),-np.sin(angle),0],
                   [0,np.sin(angle),np.cos(angle),0],
                   [0,0,0,1]])
    point = np.matrix(point)
    return point*rx
    
def Ry(point, angle):
    # Rotates point about the y-axis by angle. 
    ry = np.array([[np.cos(angle),0,np.sin(angle),0],
                   [0,1,0,0],
                   [-np.sin(angle),0,np.cos(angle),0],
                   [0,0,0,1]])
    point = np.matrix(point)

    return point*ry
    
def Rz(point, angle):
    # Rotates point about the z-axis by angle. 
    rz = np.array([[np.cos(angle),-np.sin(angle),0,0],
                   [np.sin(angle),np.cos(angle),0,0],
                   [0,0,1,0],
                   [0,0,0,1]])
    point = np.matrix(point)
    return point*rz
    
def Rzyx(point,a,b,c):
    # Rotates point about the z, then the y, then the x-axis.
    rzyx = np.array([[np.cos(b)*np.cos(c),np.cos(c)*np.sin(a)*np.sin(b)-np.cos(a)*np.sin(c),np.cos(a)*np.cos(c)*np.sin(b)+np.sin(a)*np.sin(c),0],
                     [np.cos(b)*np.sin(c),np.cos(a)*np.cos(c)+np.sin(a)*np.sin(b)*np.sin(c),-np.cos(c)*np.sin(a)+np.cos(a)*np.sin(b)*np.sin(c),0],
                     [-np.sin(b),np.cos(b)*np.sin(a),np.cos(a)*np.cos(b),0],
                     [0,0,0,1]])
    point = np.matrix(point)
    return point*rzyx

def loadConstants():
    "load constants from constants file"
    fudgeVector = np.loadtxt('welby_fudge_file.txt',skiprows=2,unpack=True)
    segLengths = np.loadtxt('welby_segment_file.txt',skiprows=2,unpack=True)
    return fudgeVector, segLengths    
      
def calcCoord(angles,sA):
#    "calculates servo positions when given servo angles and gyro angles."
#    
#    # Read the gyroscope    
#    imu=IMU()    # Default IC2 port 1
#    pwm=PWMDriver()
#    imu.gyro_range("245DPS")    
#    imu.read_gyro()
#    angles = qM.getEuler()
#    
#    # Read the servo angles, assuming 150 to 600 (out of 4096) is the servo ROM
#    minROM = 160    
#    maxROM = 665
#    sA = np.array([0,0,0,0,0,0,0,0])    
#    for i in range(0, 8):
#        sA[i] = (maxROM-minROM)*pwm.readPWM(i)/4096+minROM
#    
    # Gyro Euler angles
    alpha = angles[0]
    beta = angles[1]
    gamma = angles[2]
    
    fudgeVector, segLengths = loadConstants()
    
    # Turn these into numpy arrays
    fudgelHip1 = fudgeVector[0]
    fudgelHip2 = fudgeVector[1]
    fudgelKnee = fudgeVector[2]
    fudgelAnkle = fudgeVector[3]
    fudgelFoot = fudgeVector[4]
    fudgerHip1 = fudgeVector[5]
    fudgerHip2 = fudgeVector[6]
    fudgerKnee = fudgeVector[7]
    fudgerAnkle = fudgeVector[8]
    fudgerFoot = fudgeVector[9]
    
    lThighlength = segLengths[0]
    lShinlength = segLengths[1]
    lFootlength = segLengths[2]
    rThighlength = segLengths[3]
    rShinlength = segLengths[4]
    rFootlength = segLengths[5]

    # Angles in radians w.r.t origin        
    lHip1Angle = sA[0] #+pi/2;
    lHip2Angle = sA[1] 
    lkneeAngle = sA[2] 
    lankleAngle = sA[3] 
    rHip1Angle = sA[4] 
    rHip2Angle = sA[5] 
    rkneeAngle = sA[6] 
    rankleAngle = sA[7] 
         
    # Determination of coordinates of servo geometric center               
    coordlHip1 = Rzyx(fudgelHip1,alpha,beta,gamma)
    coordlHip2 = coordlHip1  + Rzyx(Ry(fudgelHip2,lHip1Angle),alpha,beta,gamma)
    coordlKnee = coordlHip2  + Rzyx(Ry(Rx(fudgelKnee+[0,-lThighlength,0,0],lHip2Angle),lHip1Angle),alpha,beta,gamma)
    coordlAnkle = coordlKnee + Rzyx(Ry(Rx(Rx(fudgelAnkle+[0,lShinlength,0,0],lkneeAngle),lHip2Angle),lHip1Angle),alpha,beta,gamma)
    coordlFoot = coordlAnkle + Rzyx(Ry(Rx(Rx(Ry(fudgelFoot+[-lFootlength*np.cos(lankleAngle),lFootlength*np.sqrt(2),lFootlength*np.sin(lankleAngle),0],lankleAngle),lkneeAngle),lHip2Angle),lHip1Angle),alpha,beta,gamma)

    coordrHip1 = Rzyx(fudgerHip1,alpha,beta,gamma)
    coordrHip2 = coordrHip1  + Rzyx(Ry(fudgerHip2,rHip1Angle),alpha,beta,gamma)
    coordrKnee = coordrHip2  + Rzyx(Ry(Rx(fudgerKnee+[0,-rThighlength,0,0],rHip2Angle),rHip1Angle),alpha,beta,gamma)
    coordrAnkle = coordrKnee + Rzyx(Ry(Rx(Rx(fudgerAnkle+[0,rShinlength,0,0],rkneeAngle),rHip2Angle),rHip1Angle),alpha,beta,gamma)
    coordrFoot = coordrAnkle + Rzyx(Ry(Rx(Rx(Ry(fudgerFoot+[rFootlength*np.cos(rankleAngle),rFootlength*np.sqrt(2),rFootlength*np.sin(rankleAngle),0],rankleAngle),rkneeAngle),rHip2Angle),rHip1Angle),alpha,beta,gamma)

    sC = np.array([coordlHip1,coordlHip2,coordlKnee,coordlAnkle,coordlFoot,coordrHip1,coordrHip2,coordrKnee,coordrAnkle,coordrFoot])
    return sC
    
    
    
