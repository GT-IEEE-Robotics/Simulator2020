#!/usr/bin/env python3
"""
File:          Pistons.py
Author:        Felipe Castro
Last Modified: Felipe Castro on 10/07
"""
#Consider piston transient status

from enum import Enum

piston_state=Enum('pistonState', 'off on')

class Pistons:
	"""The Piston class turns the piston Arduino micro-controllers on/off and maintains the status of the pistons """
	def __init__(self, piston_length: int):
		""" Generates a default list of each piston's status, 'piston_list' of length 'piston_length', each element a piston.
		If a piston is in the Nth column of the piston complex, then piston ID will be identified as so: [N]
		For example, a piston in column 2 will be identified by the ID [2].

		:param int piston_length: number of pistons maintained
		:return string piston_list: default list of piston status' all off

		"""
		self.status_list = []
		for i in range(piston_length):
			self.status_list.append(piston_state.off)




	def turn_on_piston(self, pistonID: int):
		""" This function will turn the Arduino micro-controller on, allowing current flow through the coil and extending
		the piston. If piston with piston ID 'pistonID' needs to be turned on and is in its default state ('off'), it will update
		the state of the piston and the piston will extend

		:param int pistonID: identification code of an individual piston
		:return the new state of the extended piston"""

		self.status_list[pistonID] = piston_state.on


	def turn_off_piston(self, pistonID: int):
		"""This function will turn the Arduino micro-controller off, preventing current flow through the coil
		via transistor. If piston with piston ID 'pistonID' is not in its default state ('off'), it will change the state
		of the piston back to its default state and the piston will return the piston to its normal state.
		:param int pistonID: identification code of an individual piston
		:return: the default state of the piston"""

		self.status_list[pistonID] = piston_state.off

	def piston_status(self):
		"""This function will return the current status of all individual pistons as one of two states: 'on' or 'off'.

		:param int pistonID: identifications code of an individual piston
		:return updated statusList list"""

		return self.status_list





