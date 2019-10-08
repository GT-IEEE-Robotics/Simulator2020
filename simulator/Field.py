
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
        
        self.arenaWidth = 93
        self.arenaHeight = 43

        self.areanaThickness = 1/2
        self.areanaNominalThickness = 15/32

        

        self.wallWidth = 1.5
        self.wallLength = 12
        self.wallHeight = 3.5

        self.lengthBetweenWalls = 10.75
        self.lengthBetweenButtons = 3.00

        #page 2 
        self.centerXOfHole = 9.5
        self.centerYOfHole = 8

        self.startingSqaureEdgeX = 3.5 #from 4' walls
        self.HoleEdgeX = 7.5

        self.startingSpaceHeight = 12
        self.startingSpaceWidth = 12

        self.dividingWallWidth =1 #nominal 0.75''
        self.dividingWallHeight = 2 #nominal 1.5'' vertical

        self.firstDividingWallX = 19.25 #from inside of 4' walls

        #hole
        self.stackingAreaWidth = 5
        self.stackingAreaHeight = 5 

        #pushbutton page 8              0 ~ 9 order
        self.pushbuttonDiameter = 1
        self.pushbuttonYcenter = 1.75
        self.pushbuttonInset = 0.125
