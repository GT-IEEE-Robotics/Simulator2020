#!/usr/bin/env python3
"""
File:          blockstacker_agent.py
Author:        Binit Shah 
Last Modified: Binit on 2/20
"""

import pybullet as p

from simulator.utilities import Utilities

class BlockStackerAgent:
    """The BlockStackerAgent class maintains the blockstacker agent"""
    def __init__(self, motion_delta=0.3, skew=0.0):
        """Setups infomation about the agent
        """
        self.camera_links = [6, 8]
        self.motor_links = [10, 12]
        self.flywheel_links = [14, 16]
        self.stepper_link = 1
        self.button_link = 4
        self.caster_link = 18

        # Differential motor control
        self.max_force = 1
        self.motion_delta = motion_delta
        self.velocity_limit = 4
        self.ltarget_vel, self.rtarget_vel = 0, 0
        self.lskew = abs(skew) + 1 if skew > 0.0 else 1.0
        self.rskew = abs(skew) + 1 if skew < 0.0 else 1.0

        self.enabled = False
        self.blink = 0
        self.blink_count = 0

    def load_urdf(self):
        """Load the URDF of the blockstacker into the environment

        The blockstacker URDF comes with its own dimensions and
        textures, collidables.
        """
        # TODO - load closer to the ground, ideally on it.
        self.robot = p.loadURDF(Utilities.gen_urdf_path("blockstacker/urdf/blockstacker.urdf"), [0, 0, 0.2], [0, 0, 0.9999383, 0.0111104], useFixedBase=False)

        p.setJointMotorControlMultiDof(self.robot,
                                       self.caster_link,
                                       p.POSITION_CONTROL,
                                       [0, 0, 0],
                                       targetVelocity=[100000, 100000, 100000],
                                       positionGain=0,
                                       velocityGain=1,
                                       force=[0, 0, 0])

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

    def read_wheel_velocities(self, noisy=True):
        # TODO - implement noisy
        noise = 0.0
        rmotor, lmotor = p.getJointStates(self.robot, self.motor_links)
        # print("positions ", rmotor[0], lmotor[0])
        return (rmotor[1] + noise, lmotor[1] + noise)

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
                                    targetVelocities=[-self.rtarget_vel * self.rskew, self.ltarget_vel * self.lskew] if self.enabled else [0, 0],
                                    forces=[self.max_force, self.max_force])

        if not self.enabled:
            p.changeVisualShape(self.robot, self.button_link, rgbaColor=[1, 1, self.blink, 1])
            self.blink_count += 1
            if self.blink_count > 40:
                self.blink = not self.blink
                self.blink_count = 0
        else:
            p.changeVisualShape(self.robot, self.button_link, rgbaColor=[1, 1, 0, 1])
