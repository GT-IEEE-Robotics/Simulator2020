#!/usr/bin/env python3
"""
File:          differentialdrive.py
Author:        Binit Shah 
Last Modified: Binit on 3/2
"""

import pybullet as p

class DifferentialDrive:
    """Generalized differential drive functionality""" 

    def __init__(self, motor_links, max_force=1.0, vel_limit=5.0, vel_delta=0.5, skew=0.0):
        self.motor_links = motor_links
        self.max_force = max_force
        self.vel_limit = vel_limit
        self.vel_delta = vel_delta
        self.ltarget_vel, self.rtarget_vel = 0, 0
        self.lskew = abs(skew) + 1 if skew > 0.0 else 1.0
        self.rskew = abs(skew) + 1 if skew < 0.0 else 1.0

    def __increaseLTargetVel__(self):
        self.ltarget_vel += self.vel_delta
        if self.ltarget_vel >= self.vel_limit:
            self.ltarget_vel = self.vel_limit

    def __decreaseLTargetVel__(self):
        self.ltarget_vel -= self.vel_delta
        if self.ltarget_vel <= -self.vel_limit:
            self.ltarget_vel = -self.vel_limit

    def __normalizeLTargetVel__(self):
        if self.ltarget_vel < 0:
            self.ltarget_vel += self.vel_delta
        elif self.ltarget_vel > 0:
            self.ltarget_vel -= self.vel_delta

    def __increaseRTargetVel__(self):
        self.rtarget_vel += self.vel_delta
        if self.rtarget_vel >= self.vel_limit:
            self.rtarget_vel = self.vel_limit

    def __decreaseRTargetVel__(self):
        self.rtarget_vel -= self.vel_delta
        if self.rtarget_vel <= -self.vel_limit:
            self.rtarget_vel = -self.vel_limit

    def __normalizeRTargetVel__(self):
        if self.rtarget_vel < 0:
            self.rtarget_vel += self.vel_delta
        elif self.rtarget_vel > 0:
            self.rtarget_vel -= self.vel_delta

    def process_keyboard_events(self, normalize=False):
        """Read keyboard events
        And publishes them for all of game to process
        """
        keys = p.getKeyboardEvents()

        if keys.get(65296):   #right
            self.__increaseRTargetVel__()
            self.__decreaseLTargetVel__()
        elif keys.get(65295): #left
            self.__increaseLTargetVel__()
            self.__decreaseRTargetVel__()
        elif keys.get(65297): #up
            self.__increaseLTargetVel__()
            self.__increaseRTargetVel__()
        elif keys.get(65298): #down
            self.__decreaseLTargetVel__()
            self.__decreaseRTargetVel__()
        elif normalize:
            self.__normalizeLTargetVel__()
            self.__normalizeRTargetVel__()

    def step(self, robot_id, enabled):
        p.setJointMotorControlArray(robot_id, self.motor_links, p.VELOCITY_CONTROL,
                                    targetVelocities=[-self.rtarget_vel * self.rskew, self.ltarget_vel * self.lskew] if enabled else [0, 0],
                                    forces=[self.max_force, self.max_force])
