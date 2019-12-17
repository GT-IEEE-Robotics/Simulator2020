#!/usr/bin/env python3
"""
File:          trainingbot_agent.py
Author:        Binit Shah 
Last Modified: Binit on 12/11
"""

import pybullet as p

from simulator.utilities import Utilities

class TrainingBotAgent:
    """The TrainingBotAgent class maintains the trainingbot agent"""
    def __init__(self, motion_delta=0.5):
        """Setups infomation about the agent
        """
        self.camera_link = 15
        self.caster_links = [12, 13]
        self.motor_links = [3, 8]

        # differential motor control
        self.max_force = 1
        self.motion_delta = motion_delta
        self.velocity_limit = 5
        self.ltarget_vel, self.rtarget_vel = 0, 0

    def load_urdf(self, cwd):
        """Load the URDF of the trainingbot into the environment

        The trainingbot URDF comes with its own dimensions and
        textures, collidables.
        """
        self.robot = p.loadURDF(Utilities.gen_urdf_path("TrainingBot/urdf/TrainingBot.urdf", cwd), [-0.93, 0, 0.1], [0.5, 0.5, 0.5, 0.5], useFixedBase=False)
        p.setJointMotorControlArray(self.robot, self.caster_links, p.VELOCITY_CONTROL, targetVelocities=[100000, 100000], forces=[0, 0])


        # print("num_joints", p.getNumJoints(self.robot))
        # for i in range(p.getNumJoints(self.robot)):
        #     print(p.getJointInfo(self.robot, i))
        
        # print(p.getLinkState(self.robot, 15))
        # print('\n')
        # print(p.getJointInfo(self.robot, 15))
        # print(p.getLinkState(self.robot, 15)[0])
        # print(p.getLinkState(self.robot, 15)[1])
        # self.debug_pose = Utilities.add_debug_pose(position=p.getJointInfo(self.robot, self.camera_link)[14], parentObjectUniqueId=self.robot, parentLinkIndex=14)
        # self.debug_pose = Utilities.add_debug_pose(position=p.getLinkState(self.robot, self.camera_link)[0], orientation=p.getLinkState(self.robot, self.camera_link)[1])

    def increaseLTargetVel(self):
        self.ltarget_vel += self.motion_delta
        if self.ltarget_vel >= self.velocity_limit:
            self.ltarget_vel = self.velocity_limit

    def decreaseLTargetVel(self):
        self.ltarget_vel -= self.motion_delta
        if self.ltarget_vel <= -self.velocity_limit:
            self.ltarget_vel = -self.velocity_limit

    def normalizeLTargetVel(self):
        if self.ltarget_vel < 0:
            self.ltarget_vel += self.motion_delta
        elif self.ltarget_vel > 0:
            self.ltarget_vel -= self.motion_delta

    def increaseRTargetVel(self):
        self.rtarget_vel += self.motion_delta
        if self.rtarget_vel >= self.velocity_limit:
            self.rtarget_vel = self.velocity_limit

    def decreaseRTargetVel(self):
        self.rtarget_vel -= self.motion_delta
        if self.rtarget_vel <= -self.velocity_limit:
            self.rtarget_vel = -self.velocity_limit

    def normalizeRTargetVel(self):
        if self.rtarget_vel < 0:
            self.rtarget_vel += self.motion_delta
        elif self.rtarget_vel > 0:
            self.rtarget_vel -= self.motion_delta

    def set_max_force(self, max_force):
        self.max_force = max_force

    def update(self):
        # movement
        p.setJointMotorControlArray(self.robot, self.motor_links, p.VELOCITY_CONTROL, targetVelocities=[self.rtarget_vel, self.ltarget_vel], forces=[self.max_force, self.max_force])

        # Camera
        *_, camera_position, camera_orientation = p.getLinkState(self.robot, self.camera_link)
        camera_look_position, _ = p.multiplyTransforms(camera_position, camera_orientation, [0,0.1,0], [0,0,0,1])
        # view_matrix = p.computeViewMatrix(
        #   cameraEyePosition=camera_position,
        #   cameraTargetPosition=camera_look_position,
        #   cameraUpVector=(0, 0, 1))
        # projection_matrix = p.computeProjectionMatrixFOV(
        #   fov=45.0,
        #   aspect=1.0,
        #   nearVal=0.1,
        #   farVal=3.1)
        # p.getCameraImage(300, 300, view_matrix, projection_matrix)
    