"""
File:           legos.py
Author:         Ammar Ratnani
Last Modified:  Ammar on 11/26
"""

import pybullet as p
from typing import List, Tuple
import re

from simulator.utilities import Utilities


class Legos:
    """
    A class to provide for the importing of legos.

    Provides functions to import a list of legos and put them at desired 
    positions. Also allows specifying the colors. Will eventually provide 
    functionality to calculate the score based off the legos so we don't have 
    to do it manually.
    """

    """The height to spawn the blocks at"""
    SPAWN_HEIGHT = .4

    def __init__(self):
        """Creates an array of all the block ids to be populated.
        Right now there isn't much of a need for internal state, but when we 
        start keeping track of score this may expand.
        """
        self.block_ids : List[int] = []

    def __str__(self) -> str:
        """Prints out instance variables."""
        return "(" + str(self.block_ids) + ")"

    def __repr__(self) -> str:
        """Returns `__str__` for easy debugging."""
        return str(self)

    def load_lego_urdfs(self, cwd : str, blocks : List[Tuple[float, float, str]]) -> None:
        """Loads the blocks specified in the list.
        Takes in a list of x and y positions, as well as the rgb color to 
        make the blocks, and loads them upright into the play field. Also 
        does validation to make sure the blocks are in range, and throws an 
        exception if they are not.

        :param blocks: a list of tuples of x, y, and rgb hex
        :raises ValueError: if the x or y is out of range or hex is invalid
        """

        for b in blocks:
            # For readability
            b_x = b[0]
            b_y = b[1]

            # Check that the color is valid with regex
            if re.match(r"#[0-9a-f]{6}", b[2]) == None:
                raise ValueError("Must have valid rgb hex color")
            # Compute its color
            # We hard code the alpha as it must be exactly 0 or 1
            # From stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
            b_color = [int(b[2].lstrip('#')[i:i+2], 16) / 256 for i in (0,2,4)] + [1]

            # Check that it is valid
            # Basic sanity check that it is in bin area for now
            if abs(b_x) >= .682625 \
            or abs(b_y) >= .5715 \
            or abs(b_y) <= .2667:
                raise ValueError("Center of lego block not in bin area")

            # Load the block
            b_id = p.loadURDF(
                fileName = Utilities.gen_urdf_path("lego/lego.urdf", cwd),
                basePosition = [b_x, b_y, Legos.SPAWN_HEIGHT])
            # Change its color with white specular
            p.changeVisualShape(
                objectUniqueId = b_id,
                linkIndex = -1,
                rgbaColor = b_color,
                specularColor = [1,1,1])
            # Change the collision properties so they stick
            # Requires further testing
            p.changeDynamics(
                bodyUniqueId = b_id,
                linkIndex = -1,
                contactStiffness = 1e6, # Unknown units
                contactDamping = 1e5) # Unknown units

            # Append the block id to the list we are maintaining
            self.block_ids.append(b_id)
