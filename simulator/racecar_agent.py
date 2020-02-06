#!/usr/bin/env python3
"""
File:          racecar_agent.py
Author:        Binit Shah 
Last Modified: Binit on 10/30
"""

import pybullet as p

from simulator.utilities import Utilities


class RacecarAgent:
    """The RacecarAgent class maintains the demo racecar agent"""
    def __init__(self, motion_delta=1):
        """Setups infomation about the agent
        """
        self.accel_wheel_links = [8, 15]
        self.steer_wheel_links = [0, 2]
        self.targetVelocity = 0 # -50 to 50
        self.steeringAngle = 0 # -10 to 10
        self.motion_delta = motion_delta
        self.max_force = 20

    def load_urdf(self):
        """Load the URDF of the racecar into the environment

        The racecar URDF comes with its own dimensions and
        textures, collidables.
        """
        # Load robot
        self.car = p.loadURDF(Utilities.gen_urdf_path("racecar/racecar_differential.urdf"), [0, 0, 0.5], useFixedBase=False, globalScaling=0.5)
        for wheel in range(p.getNumJoints(self.car)):
            p.setJointMotorControl2(self.car, wheel, p.VELOCITY_CONTROL, targetVelocity=0, force=0)
            p.getJointInfo(self.car, wheel)

        # Constraints
        #p.setJointMotorControl2(car,10,p.VELOCITY_CONTROL,targetVelocity=1,force=10)
        c = p.createConstraint(self.car,
                                9,
                                self.car,
                                11,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        c = p.createConstraint(self.car,
                                10,
                                self.car,
                                13,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.car,
                                9,
                                self.car,
                                13,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.car,
                                16,
                                self.car,
                                18,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        c = p.createConstraint(self.car,
                                16,
                                self.car,
                                19,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.car,
                                17,
                                self.car,
                                19,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.car,
                                1,
                                self.car,
                                18,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=-1, gearAuxLink=15, maxForce=10000)
        c = p.createConstraint(self.car,
                                3,
                                self.car,
                                19,
                                jointType=p.JOINT_GEAR,
                                jointAxis=[0, 1, 0],
                                parentFramePosition=[0, 0, 0],
                                childFramePosition=[0, 0, 0])
        p.changeConstraint(c, gearRatio=-1, gearAuxLink=15, maxForce=10000)
        
    def increaseTargetVel(self):
        self.targetVelocity += self.motion_delta
        if self.targetVelocity >= 50:
            self.targetVelocity = 50

    def decreaseTargetVel(self):
        self.targetVelocity -= self.motion_delta
        if self.targetVelocity <= -50:
            self.targetVelocity = -50

    def normalizeTargetVel(self):
        if self.targetVelocity < 0:
            self.targetVelocity += self.motion_delta
        elif self.targetVelocity > 0:
            self.targetVelocity -= self.motion_delta

    def increaseLeftSteering(self):
        self.steeringAngle -= self.motion_delta
        if self.steeringAngle <= -10:
            self.steeringAngle = -10

    def increaseRightSteering(self):
        self.steeringAngle += self.motion_delta
        if self.steeringAngle >= 10:
            self.steeringAngle = 10

    def normalizeSteering(self):
        if self.steeringAngle < 0:
            self.steeringAngle += self.motion_delta
        elif self.steeringAngle > 0:
            self.steeringAngle -= self.motion_delta

    def update_racecar(self):
        for wheel in self.accel_wheel_links:
            p.setJointMotorControl2(self.car,
                                    wheel,
                                    p.VELOCITY_CONTROL,
                                    targetVelocity=self.targetVelocity,
                                    force=self.max_force)

        for steer in self.steer_wheel_links:
            p.setJointMotorControl2(self.car, steer, p.POSITION_CONTROL, targetPosition=-self.steeringAngle / 10)

    def set_max_force(self, max_force):
        self.max_force = max_force