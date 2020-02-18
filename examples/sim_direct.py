#!/usr/bin/env python3
"""
File:          sim_direct.py
Author:        Binit Shah
Last Modified: Binit on 2/18

Do NOT call the simulator as shown in this example,
follow `sim_remote.py`'s example instead.
"""

from simulator.game import Game

if __name__ == "__main__":
    game = Game()
    game.setup("")

    while True:
        game.step()
