#!/usr/bin/env python3
"""
File:		   Buttons.py
Author:		   Ammar Ratnani
Last Modified: Ammar on 9/25
"""

# Needed for typing syntax
from typing import List


class Button:
	"""A simple class to retain the state of a button.

	Represents a single button on the button wall, keeping track of its state. 
	It is deliberately structured very much like the code in the 
	`ArenaControl.ino` file, trying to keep as much parallelism between the 
	two to increase fidelity (hopefully).
	"""

	def __init__(self):
		"""Creates a button with its inital state.

		At the start of the competition, all buttons are unpressed and have 
		their last state set to unpressed. This constructor emulates that. 
		The names of variables are also kept mostly the same, just changing 
		for style.
		"""
		# These are `int`s in the code, but they are treated as booleans
		self.button_state : bool = False
		"""Represents the current state of the button."""
		self.last_button_state : bool = False
		"""Represents the last read state of the button."""

		# This is for simulation. We only change this in the `Buttons` class
		self.reading : bool = False
		"""Simulates the reading of the button."""

		self.last_debounce_time : float = 0.0 # in seconds
		"""Like the code, stores the last time the button changed its state."""


	def __str__(self) -> str:
		"""Returns a nice string representation of this button.

		Simply returns the state of the variables in order. Formats it as a 
		tuple: `(self.button_state, self.last_button_state, self.reading, 
		self.last_debounce_time)`.

		:return: a string representation of this button
		"""
		return '(' + \
			str(self.button_state) + ', ' + \
			str(self.last_button_state) + ', ' + \
			str(self.reading) + ', ' + \
			str(self.last_debounce_time) + ')'


	def __repr__(self) -> str:
		"""Return `self.__str__()`
		
		Kept here for easier debugging and printing.
		:return: `self.__str__()`
		"""
		return self.__str__()



class Buttons:
	"""The Buttons class maintains the state of pressable buttons on the left 
	   wall.
	
	Note that much of this code does its best to emulate the `ArenaControl.ino` 
	logic to (hopefully) increase the fidelity of the simulation.
	"""

	"""The time delay in seconds to verify for debouncing."""
	DEBOUNCE_DELAY : float = .025 # 25 milliseconds

	"""The first 2000 digits of PI in a string."""
	PI : str =  '31415926535897932384626433832795028841971693993751' + \
				'05820974944592307816406286208998628034825342117067' + \
				'98214808651328230664709384460955058223172535940812' + \
				'84811174502841027019385211055596446229489549303819' + \
				'64428810975665933446128475648233786783165271201909' + \
				'14564856692346034861045432664821339360726024914127' + \
				'37245870066063155881748815209209628292540917153643' + \
				'67892590360011330530548820466521384146951941511609' + \
				'43305727036575959195309218611738193261179310511854' + \
				'80744623799627495673518857527248912279381830119491' + \
				'29833673362440656643086021394946395224737190702179' + \
				'86094370277053921717629317675238467481846766940513' + \
				'20005681271452635608277857713427577896091736371787' + \
				'21468440901224953430146549585371050792279689258923' + \
				'54201995611212902196086403441815981362977477130996' + \
				'05187072113499999983729780499510597317328160963185' + \
				'95024459455346908302642522308253344685035261931188' + \
				'17101000313783875288658753320838142061717766914730' + \
				'35982534904287554687311595628638823537875937519577' + \
				'81857780532171226806613001927876611195909216420198' + \
				'93809525720106548586327886593615338182796823030195' + \
				'20353018529689957736225994138912497217752834791315' + \
				'15574857242454150695950829533116861727855889075098' + \
				'38175463746493931925506040092770167113900984882401' + \
				'28583616035637076601047101819429555961989467678374' + \
				'49448255379774726847104047534646208046684259069491' + \
				'29331367702898915210475216205696602405803815019351' + \
				'12533824300355876402474964732639141992726042699227' + \
				'96782354781636009341721641219924586315030286182974' + \
				'55570674983850549458858692699569092721079750930295' + \
				'53211653449872027559602364806654991198818347977535' + \
				'66369807426542527862551818417574672890977772793800' + \
				'08164706001614524919217321721477235014144197356854' + \
				'81613611573525521334757418494684385233239073941433' + \
				'34547762416862518983569485562099219222184272550254' + \
				'25688767179049460165346680498862723279178608578438' + \
				'38279679766814541009538837863609506800642251252051' + \
				'17392984896084128488626945604241965285022210661186' + \
				'30674427862203919494504712371378696095636437191728' + \
				'74677646575739624138908658326459958133904780275900'


	def __init__(self, num_buttons: int = 10):
		"""Sets up the simulated buttons.

		Simply creates a list `num_buttons` long consisting of separate 
		instances of the above `Button` class. Also creates some 
		variables to keep track of time and scoring.

		:param int num_buttons: the number of buttons on the wall
		"""
		# Required to create separate instances
		self.button_state : List[Button] = [Button() for _ in range(num_buttons)]

		# Scoring
		# Contains a slight change: instead of using `piDigitPosn`, just use 
		#  `numSequenced`
		self.in_sequence : bool = True
		self.num_sequenced : int = 0
		self.extra_not_sequenced : int = 0

		# Also store the time of the simulation in seconds
		self.time : float = 0.0


	def __str__(self) -> str:
		"""Returns a string representation of the current game state.

		Again, represents the current state as a tuple: `(score, 
		self.num_sequenced, self.extra_not_sequenced, self.in_sequence,
		self.time, self.button_state)`, where `score` is calculated as 
		`10 * self.num_sequenced + min(self.extra_not_sequenced, 100)`.

		:return: a string representation of this object
		"""
		return '(' + \
			str(10*self.num_sequenced + min(self.extra_not_sequenced,100)) + ', ' + \
			str(self.num_sequenced) + ', ' + \
			str(self.extra_not_sequenced) + ', ' + \
			str(self.in_sequence) + ', ' + \
			str(self.time) + ', ' + \
			str(self.button_state) + ')'


	def __repr__(self) -> str:
		"""Return `self.__str__()`
		
		Kept here for easier debugging and printing.
		:return: `self.__str__()`
		"""
		return self.__str__()


	def press_button(self, button_num: int) -> Button:
		"""Press a simulated button

		Updates the reading on the button. This will be reflected in 
		future updates to the buttons. This function will also call 
		`update_buttons()` without advancing the time any just to 
		simulate the fact that the Arduino is constantly getting 
		readings. For example, you can't press and unpress a button 
		without detection.

		:param int button_num: the button being pressed
		:return: the new state of the pressed button
		:raises IndexError: if the index is out of range
		:raises ValueError: if the index cannot index arrays
		"""
		try:
			self.button_state[button_num].reading = True
			# Note that this only happens if the first line succeeds
			self.update_buttons(0.0)
		except IndexError:
			# Just change the message
			raise IndexError("we must have 0 <= `button_num` < `num_buttons`")
		except ValueError:
			raise ValueError("`button_num` must be able to index arrays")


	def unpress_button(self, button_num: int) -> Button:
		"""Unpress a simulated button

		Updates the reading on the button to be reflected in future updates 
		to the buttons. This function also calls `update_buttons()` without 
		advancing the time. Very similar to the `press_button()` function, 
		and only differ on one line, where instead of setting the reading to
		`True`, it is set to `False`.

		:param int button_num: the button being unpressed
		:return: The new state of the unpressed button
		:raises IndexError: if the index is out of range
		:raises ValueError: if the index cannot index arrays
		"""
		# Similar try-except to `press_button()`
		try:
			self.button_state[button_num].reading = False
			self.update_buttons(0.0)
		except IndexError:
			raise IndexError("we must have 0 <= `button_num` < `num_buttons`")
		except ValueError:
			raise ValueError("`button_num` must be able to index arrays")


	def update_buttons(self, dt: float) -> None:
		"""Updates all the buttons' states

		By far the most involved function in this class, simulating both 
		the `debounce_buttons()` and `loop()` methods in `ArenaControl.ino`.
		Flashing LEDs are not simulated, as they don't affect button pushes.
		This may change in the future. Also runs indefinitely for now. If 
		there is a bug, this is the most likely place for it to be. For best 
		fidelity, this method should only be called with small timesteps. It 
		should work even with large timesteps, but you may not get some points 
		which you should have.

		:param float dt: the time passed in simulation
		"""
		# Suppose a certain (possibly zero) amount of time has passed
		self.time += dt

		# Whether a new button has been pressed
		new_press : bool = False
		# How many are pressed
		num_pressed : int = 0

		# `debounceButtons()`
		# i -> digit; b -> buttonState[digit]
		for i,b in enumerate(self.button_state):
			# It doesn't matter if it changed because noise or press
			if b.reading != b.last_button_state:
				b.last_debounce_time = self.time
			# If a reading has stayed for a certain amount of time
			# Note that this is a strict greater than
			if (self.time - b.last_debounce_time) > Buttons.DEBOUNCE_DELAY:
				# Only do this if the state has changed
				if b.reading != b.button_state:
					b.button_state = b.reading
					# If the state changed to pressed
					if b.button_state:
						new_press = True
			# If the button is pressed, update `num_pressed`
			if b.button_state:
				num_pressed += 1
			# Save the reading
			b.last_button_state = b.reading

		# Logic in `loop()`
		if num_pressed == 0:
			# Bad style, but this is what the code does
			pass
		# Currently in sequence
		elif self.in_sequence:
			# We aren't sequencing if more than one pressed
			if num_pressed > 1:
				self.in_sequence = False
			elif new_press:
				digit = int(Buttons.PI[self.num_sequenced])
				if not self.button_state[digit].button_state:
					self.in_sequence = False
				else:
					self.num_sequenced += 1
		# Case not in sequence
		else:
			if new_press:
				self.extra_not_sequenced += 1


	def button_status(self, button_num: int) -> Button:
		"""Retrieves a button's state.

		Returns the `Button` object associated with the button at index 
		`button_num`. Simply accesses it from the array, returning by 
		reference (not by value).

		:param int button_num: the index corresponding to the button
		:return: the `Button` object corresponding to the button
		:raises IndexError: if the index is out of range
		:raises ValueError: if the index cannot index arrays
		"""
		# Similar try-except block to `press_button()` and `unpress_button()`
		try:
			return self.button_state[button_num]
		except IndexError:
			raise IndexError("we must have 0 <= `button_num` < `num_buttons`")
		except ValueError:
			raise ValueError("`button_num` must be able to index arrays")
