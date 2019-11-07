#!/usr/bin/env python3
"""
File:          Field.py
Author:        Moungsung Im 
Last Modified: Ammar on 11/06
"""

import pybullet as p

from simulator.utilities import Utilities
from simulator.field_components.buttons import Buttons

class Field:
    """The Field class maintains the state of the simulated elements within the field"""
    def __init__(self):
        """Sets up the electrical components of the field"""
        self.buttons = Buttons()

    def load_field_urdf(self, cwd):
        """Load the URDF of the field into the environment

        The field URDF comes with its own dimensions and
        textures, collidables. Note that this also calls 
        the method responsible for setting button joint IDs.
        """
        self.model_id = p.loadURDF(Utilities.gen_urdf_path("field/field.urdf", cwd), useFixedBase=True)
        self.buttons.populate_joint_ids([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])

        for i in range(1, 21, 2):
            p.setJointMotorControl2(self.field_model_id, i, controlMode=p.POSITION_CONTROL, targetPosition=0.0, force=0.2, positionGain=0.8)
