#!/usr/bin/env python3
"""
File:          Game.py
Author:        Alex Cui
Last Modified: Binit on 2/15
"""

import os
import time
import pybullet as p

from simulator.field import Field
from simulator.legos import Legos
from simulator.trainingbot_agent import TrainingBotAgent
from simulator.blockstacker_agent import BlockStackerAgent
from simulator.utilities import Utilities

class Game:
    """Maintains information of one 3 minute round"""

    def __init__(self, 
                 use_interactive=True,
                 is_interactive_realtime=True,
                 hide_ui=True,
                 topdown_viewport=False,
                 log_dir=None,
                 log_bullet_states=False,
                 log_mp4=False,
                 robot_skew=0.0):
        """Sets up simulation elements.
        Two sets of preferences affect how the simulation behaves. Choosing a
        interactive simulation session allows you to interact with the robot
        through keyboard and mouse. Headless sessions run much quicker and
        can be used for automated testing.

        Logging helps narrow down how and when the robot fails. A mp4 video
        from the viewport and/or .bullet restorable states can be saved to
        the log folder.
        
        :param use_interactive:         determines whether the pybullet simulation
                                        runs with a GUI open or headless.
        :param is_interactive_realtime: when interactive, choose manual timestepping
                                        or run realtime. headless sim only uses
                                        manual timestepping.
        :param hide_ui:                 when interactive, choose to hide UI elements.
        :param topdown_viewport:        when interactive, choose between default
                                        and topdown viewports.
        :param log_dir:                 the directory in which to log.
        :param log_bullet_states:       logs .bullet sim states every 5.0 sec or
                                        every 1200 iterations.
        :param log_mp4:                 when interactive, logs .mp4 video until sim
                                        completes via a graceful stop (corrupts log
                                        if sim ends ungracefully).
        :param robot_skew:              [-inf, inf] where negative values skew left,
                                        0 is no skew, and positive skew right
        """
        self.use_interactive = use_interactive
        self.is_interactive_realtime = is_interactive_realtime
        self.hide_ui = hide_ui
        self.topdown_viewport = topdown_viewport
        self.log_dir = log_dir
        self.log_bullet_states = log_bullet_states
        self.log_mp4 = log_mp4
        self.TIMESTEPPING_DT = 1 / 240
        self.PRESSED_THRES = -.0038

        p.connect(p.GUI if self.use_interactive else p.DIRECT)
        p.resetSimulation()
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0 if self.hide_ui else 1)
        if self.topdown_viewport:
            p.resetDebugVisualizerCamera(1.1, 0.0, -89.9, (0.0, 0.0, 0.0))
        else:
            p.resetDebugVisualizerCamera(2, 30.0, -50.0, (0.0, 0.2, 0.0))
        p.setGravity(0, 0, -9.8)
        if self.log_mp4:
            p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4, os.join(self.log_dir, "log.mp4"))
        p.setRealTimeSimulation(1 if self.is_interactive_realtime else 0)

        self.mobile_agent = BlockStackerAgent(skew=robot_skew)
        self.field = Field()
        self.legos = Legos()

    def load_environment(self, bin_configuration_yaml):
        """Loading the env objects
        Including field, buttons, and more.
        """
        self.field.load_urdf()
        self.legos.load_lego_urdfs([(0, -0.3, 0.1, "#00ffff")])

    def load_agents(self, initial_mobile_pose=None):
        """Loading the agents
        Including the button robot and the mobile block stacking robot.
        """
        self.mobile_agent.load_urdf()
        if initial_mobile_pose:
            self.mobile_agent.set_pose(initial_mobile_pose)

    def load_ui(self):
        """Loading the UI components
        Such as sliders or buttons.
        """
        self.maxForceSlider = p.addUserDebugParameter("maxForce", 0, 5, 1)

    def read_ui(self):
        """Reads the UI components' state
        And publishes them for all of game to process
        """
        maxForce = p.readUserDebugParameter(self.maxForceSlider)
        self.mobile_agent.drive.set_max_force(maxForce)

    def monitor_buttons(self):
        # Store the return values for readability
        buttonStates = p.getJointStates(
                            self.field.model_id,
                            [b.joint_id for b in self.field.buttons])

        # Get every button and press it if needed
        for i,x in enumerate(buttonStates):
            if x[0] < self.PRESSED_THRES:
                self.field.buttons.press_button(i)
            else:
                self.field.buttons.unpress_button(i)
    
    def setup(self,
              bin_configuration_yaml,
              starting_state_fname=None,
              starting_robot_pose=None,
              starting_time=0.0,
              auto_enable_timer=0.0):
        """Setups the game elements.

        :param bin_configuration_yaml: the yaml file to read for bin setup.
        :param starting_state_fname:   the starting state file of simulation.
        :param starting_robot_pose:    the starting pose of the mobile robot.
        :param starting_time:          the starting time of the simulation.
        :param auto_enable_timer:      timer to auto enable robot, 0 disables.
        """
        self.load_environment(bin_configuration_yaml)
        self.load_agents(initial_mobile_pose=starting_robot_pose)
        if not self.hide_ui:
            self.load_ui()

        if starting_state_fname:
            p.restoreState(fileName=starting_state_fname)
        self.starting_state = p.saveState()

        self.initial_auto_enable_timer = auto_enable_timer
        self.auto_enable_timer = self.initial_auto_enable_timer
        self.auto_enabled = False

        self.starting_time = starting_time
        self.time = self.starting_time
        if self.use_interactive and self.is_interactive_realtime:
            self.prev = time.time()

        self.info_id = Utilities.draw_debug_info(self.time)

    def reset(self):
        p.restoreState(self.starting_state)
        self.time = self.starting_time
        self.auto_enable_timer = self.initial_auto_enable_timer
        self.auto_enabled = False
        return self.time

    def step(self):
        """One step of the simulation
        Needs to run to for both realtime and timestepping sessions.
        """
        if self.use_interactive and self.is_interactive_realtime:
            now = time.time()
            self.time += now - self.prev
            if not self.auto_enabled and self.auto_enable_timer > 0.0:
                self.auto_enable_timer -= now - self.prev
                if self.auto_enable_timer <= 0.0:
                    self.mobile_agent.enabled = True
                    self.auto_enabled = True
            self.prev = now
            # TODO - use this to figure out the dimensions of vel (rad/s?), wheel pos (arclength m?), and world pose (m)
            # if self.time - self.starting_time <= 10.0:
            #     print("velocities ", self.mobile_agent.read_wheel_velocities())
            #     print("world pose ", self.mobile_agent.get_pose())
            # TODO - log bullet states every 5 seconds iterations
        else:
            self.time += self.TIMESTEPPING_DT
            if not self.auto_enabled and self.auto_enable_timer > 0.0:
                self.auto_enable_timer -= self.TIMESTEPPING_DT
                if self.auto_enable_timer <= 0.0:
                    self.mobile_agent.enabled = True
                    self.auto_enabled = True
            p.stepSimulation()
            # TODO - log bullet states every 1200 iterations

        self.info_id = Utilities.draw_debug_info(self.time, replaceItemUniqueId=self.info_id)

        if not self.hide_ui:
            self.read_ui()
        if self.use_interactive and self.mobile_agent.enabled:
            self.mobile_agent.drive.process_keyboard_events(normalize=True)

        # self.monitor_buttons()
        self.legos.step(self.mobile_agent.robot, self.mobile_agent.tower_link)
        self.mobile_agent.step()
