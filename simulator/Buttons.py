#!/usr/bin/env python3
"""
File:          ButtonSim.py
Author:        Ammar Ratnani
Last Modified: Binit on 9/23
"""

from enum import Enum
from typing import Tuple

ButtonState = Enum('ButtonState', 'unpressed pressed debouncing')


class Buttons:
    """The Buttons class maintains the state of pressable buttons on the left wall"""

    def __init__(self, num_buttons: int):
        """Setups simulated buttons

        Creates a list of `num_buttons` length, each element a button.
        A button is in one state of ButtonState and has a timer for 
        the debounce period.

        :param int num_buttons: the number of buttons maintained
        """
        pass


    def press_button(self, button_num: int) -> ButtonState:
        """Press a simulated button

        Updates the state of a selected button. The resulting state of
        the button is dependent on the previous state of the button. A
        unpressed button becomes a pressed button. A pressed button
        remains pressed. A debouncing button will not register new
        presses until its debounce period is over
        (see why: http://www.labbookpages.co.uk/electronics/debounce.html).

        :param int button_num: the button being pressed
        :return: The new state of the pressed button
        """
        pass


    def unpress_button(self, button_num: int) -> ButtonState:
        """Unpress a simulated button

        Updates the state of a selected button. The resulting state of
        the button is dependent on the previous state of the button. A
        unpressed button remains a unpressed button. A pressed button
        becomes a debouncing button. Additionally, a debouncing timer
        is started. A debouncing button remains a debouncing button.

        :param int button_num: the button being unpressed
        :return: The new state of the unpressed button
        """
        pass


    def update_buttons(self, dt: float) -> None:
        """Updates buttons' debounce timers

        For each maintained button, if a debounce timer is active,
        the timer's time is reduced by the time delta given by the
        simulator.

        :param float dt: the time passed in simulation
        """
        pass


    def button_status(self, button_num: int) -> Tuple[ButtonState, float]:
        """Retrieves a button's state

        Returns the current state of a button and time left on the
        debounce timer.

        :param int button_num: the selected button
        :return: button state and time remaining in debounce period
        """
        pass