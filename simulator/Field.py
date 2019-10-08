
"""
File:          Field.py
Author:        Moungsung Im 
Last Modified: Moungsung on 10/8
"""

import Buttons


class Field:
    """The Field class maintains the state of the simulated elements within the field"""
    def __init__(self):
        """Setups concrete measurements known about the field
        Save measurements known about the field to the class
        here. For example, the walls and their positions/
        lengths. Also initializes simulated elements within
        the field, like the buttons.
        """
        
        self.arena_width = 93
        self.arena_height = 43

        self.arena_thickness = 1/2
        self.arena_nominal_thickness = 15/32

        

        self.wall_width = 1.5
        self.wall_length = 12
        self.wall_height = 3.5

        self.length_between_walls = 10.75
        self.length_between_buttons = 3.00

        #page 2 
        self.centerX_of_hole = 9.5
        self.centerY_of_hole = 8

        self.starting_sqaure_edgeX = 3.5 #from 4' walls
        self.hole_edgeX = 7.5

        self.starting_space_height = 12
        self.starting_space_width = 12

        self.dividing_wall_width =1 #nominal 0.75''
        self.dividing_wall_height = 2 #nominal 1.5'' vertical

        self.first_dividing_wallX = 19.25 #from inside of 4' walls

        #hole
        self.stacking_area_width = 5
        self.stacking_area_height = 5 

        #pushbutton page 8              0 ~ 9 order
        self.pushbutton_diameter = 1
        self.pushbuttonY_center = 1.75
        self.pushbutton_inset = 0.125
