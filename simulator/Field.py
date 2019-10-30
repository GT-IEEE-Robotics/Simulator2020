#!/usr/bin/env python3
"""
File:          Field.py
Author:        Moungsung Im 
Last Modified: Binit on 10/30
"""

import pybullet as p

from simulator.Buttons import Buttons
from simulator.Utilities import Utilities

class Field:
    """The Field class maintains the state of the simulated elements within the field"""
    def __init__(self):
        """Setups concrete measurements known about the field

        Save measurements known about the field to the class
        here. For example, the walls and their positions/
        lengths. Also initializes simulated elements within
        the field, like the buttons.
        """
        self.buttons = Buttons()

    def load_field_urdf(self, cwd):
        """Load the URDF of the field into the environment

        The field URDF comes with its own dimensions and
        textures, collidables.
        """
        p.loadURDF(Utilities.gen_urdf_path("ArenaLayout/ArenaLayout.urdf", cwd), useFixedBase=True)
        self.buttons.load_buttons_urdf(cwd)
