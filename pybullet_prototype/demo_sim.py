import os
import time
import keyboard
import numpy as np
import pybullet as p

cwd = os.getcwd()
def gen_urdf_path(urdf_fname):
        return os.path.join(cwd, "data", urdf_fname)

class DemoSim:
    def setup(self):
        cid = p.connect(p.SHARED_MEMORY)
        if (cid < 0):
            p.connect(p.GUI)

        p.resetSimulation()
        p.setGravity(0, 0, -9.8)
        self.useRealTimeSim = 1

        #for video recording (works best on Mac and Linux, not well on Windows)
        #p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4, "racecar.mp4")
        p.setRealTimeSimulation(self.useRealTimeSim)  # either this

        # Load arena
        p.loadURDF(gen_urdf_path("ArenaLayout/ArenaLayout.urdf"), useFixedBase=True)

        # Load robot
        self.car = p.loadURDF(gen_urdf_path("racecar/racecar_differential.urdf"), [0, 0, 2], useFixedBase=False)
        for wheel in range(p.getNumJoints(self.car)):
            p.setJointMotorControl2(self.car, wheel, p.VELOCITY_CONTROL, targetVelocity=0, force=0)
            p.getJointInfo(self.car, wheel)

        # Constraints
        self.wheels = [8, 15]
        self.steering = [0, 2]

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

        self.maxForceSlider = p.addUserDebugParameter("maxForce", 0, 50, 20)
        print("----------------")

    def loop(self):
        targetVelocity = 0 # -50 to 50
        steeringAngle = 0 # -10 to 10
        delta = 1
        while (True):
            maxForce = p.readUserDebugParameter(self.maxForceSlider)

            try:
                if keyboard.is_pressed("up arrow"):
                    targetVelocity += delta
                    if targetVelocity >= 50:
                        targetVelocity = 50
                elif keyboard.is_pressed("down arrow"):
                    targetVelocity -= delta
                    if targetVelocity <= -50:
                        targetVelocity = -50
                else:
                    if targetVelocity < 0:
                        targetVelocity += delta
                    elif targetVelocity > 0:
                        targetVelocity -= delta

                if keyboard.is_pressed("right arrow"):
                    steeringAngle += delta
                    if steeringAngle >= 10:
                        steeringAngle = 10
                elif keyboard.is_pressed("left arrow"):
                    steeringAngle -= delta
                    if steeringAngle <= -10:
                        steeringAngle = -10
                else:
                    if steeringAngle < 0:
                        steeringAngle += delta
                    elif steeringAngle > 0:
                        steeringAngle -= delta
            except:
                break

            for wheel in self.wheels:
                p.setJointMotorControl2(self.car,
                                        wheel,
                                        p.VELOCITY_CONTROL,
                                        targetVelocity=targetVelocity,
                                        force=maxForce)

            for steer in self.steering:
                p.setJointMotorControl2(self.car, steer, p.POSITION_CONTROL, targetPosition=-steeringAngle / 10)

            # Front of Car Synthetic Camera - Not Working
            # pos, oren = p.getBasePositionAndOrientation(car)
            # rot_matrix = p.getMatrixFromQuaternion(oren)
            # rot_matrix = np.array(rot_matrix).reshape(3, 3)
            # # Initial vectors
            # init_camera_vector = (0, 0, 1) # z-axis
            # init_up_vector = (0, 1, 0) # y-axis
            # # Rotated vectors
            # camera_vector = rot_matrix.dot(init_camera_vector)
            # up_vector = rot_matrix.dot(init_up_vector)
            # view_matrix = p.computeViewMatrix(pos + 0.3 * camera_vector, pos + 0.5 * camera_vector, up_vector)

            # Top Down Synthetic Camera
            # view_matrix = p.computeViewMatrix(
            #   cameraEyePosition=[0, 0, 3],
            #   cameraTargetPosition=[0, 0, 0],
            #   cameraUpVector=[0, 1, 0])
            # projection_matrix = p.computeProjectionMatrixFOV(
            #   fov=45.0,
            #   aspect=1.0,
            #   nearVal=0.1,
            #   farVal=3.1)
            # p.getCameraImage(300, 300, view_matrix, projection_matrix)

            self.steering
            if (self.useRealTimeSim == 0):
                p.stepSimulation()
            # time.sleep(0.01)

if __name__ == "__main__":
    demo = DemoSim()
    demo.setup()
    demo.loop()