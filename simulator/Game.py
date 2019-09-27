#!/usr/bin/env python3
"""
File:          Game.py
Author:        Alex Cui
Last Modified: Binit on 9/23
"""

import pygame

from simulator import Field
from simulator import Utilities

class Game:
    """Maintains and coordinates the game loop"""

    def __init__(self):
        """Initializes game elements
        Sets up game and simulation elements. For example,
        the three minute timer of the game.
        """
        self.clock = pygame.time.Clock()
        self.limit = 3 * 60 * 1000
        self.elapsed = 0
        self.field = Field()
        self.utilities = Utilities(2000, 8.0, 1000, 4.0)
        pass


    def render_field(self):
        """Rendering the field to the window
        Renders field elements to the window.
        """
        window = pygame.display.set_mode((utilities.window_width_p, utilities.window_height_0), 0, 32)
        pygame.display.set_caption('2020 simulation')
        window.fill(0, 0, 0)

        pass


    def run(self):
        """Maintains the game loop
        Coordinates other functions to execute here and
        tracks the delta time between each game loop.
        """
        pygame.init()
        clock.tick()
        
        while True:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            time_passed = clock.tick()
            if time_passed >= limit:
                pygame.quit()
        pass