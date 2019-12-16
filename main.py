#!/usr/bin/env python3
"""
File:          main.py
Author:        Binit Shah
Last Modified: Binit on 10/30
"""

import sys
sys.path.append('/home/ammar/.local/lib64/python3.6/site-packages')

from simulator.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
