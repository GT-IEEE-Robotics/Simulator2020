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

        # Differential motor control
        self.max_force = 1
        self.motion_delta = motion_delta
        self.velocity_limit = 5
        self.ltarget_vel, self.rtarget_vel = 0, 0

    def load_urdf(self):
        """Load the URDF of the trainingbot into the environment

        The trainingbot URDF comes with its own dimensions and
        textures, collidables.
        """
        self.robot = p.loadURDF(Utilities.gen_urdf_path("TrainingBot/urdf/TrainingBot.urdf"), [-0.93, 0, 0.1], [0.5, 0.5, 0.5, 0.5], useFixedBase=False)
        p.setJointMotorControlArray(self.robot, self.caster_links, p.VELOCITY_CONTROL, targetVelocities=[100000, 100000], forces=[0, 0])

    def get_pose(self):
        # TODO - fix orientation
        pos, ort = p.getBasePositionAndOrientation(self.robot)
        return (pos[0], pos[1], 0.0)

    def set_pose(self, pose):
        # TODO - fix orientation
        p.resetBasePositionAndOrientation([pose[0], pose[1], 0.1], [0.5, 0.5, 0.5, 0.5])
        return self.get_pose()

    def increaseLTargetVel(self):
        self.ltarget_vel += self.motion_delta
        if self.ltarget_vel >= self.velocity_limit:
            self.ltarget_vel = self.velocity_limit

    def decreaseLTargetVel(self):
        self.ltarget_vel -= self.motion_delta
        if self.ltarget_vel <= -self.velocity_limit:
            self.ltarget_vel = -self.velocity_limit

    def increaseRTargetVel(self):
        self.rtarget_vel += self.motion_delta
        if self.rtarget_vel >= self.velocity_limit:
            self.rtarget_vel = self.velocity_limit

    def decreaseRTargetVel(self):
        self.rtarget_vel -= self.motion_delta
        if self.rtarget_vel <= -self.velocity_limit:
            self.rtarget_vel = -self.velocity_limit

    def set_max_force(self, max_force):
        self.max_force = max_force

    def read_wheel_velocities(self):
        # TODO - implement this
        return (self.rtarget_vel, self.ltarget_vel)

    def command_wheel_velocities(self, rtarget_vel, ltarget_vel):
        self.rtarget_vel = rtarget_vel
        self.ltarget_vel = ltarget_vel
        return self.read_wheel_velocities()

    def capture_image(self):
        # Camera
        *_, camera_position, camera_orientation = p.getLinkState(self.robot, self.camera_link)
        camera_look_position, _ = p.multiplyTransforms(camera_position, camera_orientation, [0,0.1,0], [0,0,0,1])
        view_matrix = p.computeViewMatrix(
          cameraEyePosition=camera_position,
          cameraTargetPosition=camera_look_position,
          cameraUpVector=(0, 0, 1))
        projection_matrix = p.computeProjectionMatrixFOV(
          fov=45.0,
          aspect=1.0,
          nearVal=0.1,
          farVal=3.1)
        return p.getCameraImage(300, 300, view_matrix, projection_matrix, renderer=p.ER_BULLET_HARDWARE_OPENGL)[2]

    def step(self):
        p.setJointMotorControlArray(self.robot, self.motor_links, p.VELOCITY_CONTROL,
                                    targetVelocities=[self.rtarget_vel + 1, self.ltarget_vel + 1],
                                    forces=[self.max_force, self.max_force])