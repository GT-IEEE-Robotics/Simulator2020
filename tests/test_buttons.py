"""
File:			ButtonsTest.py
Author:			Ammar Ratnani
Last Modified:	Ammar on 9/26
"""

import unittest

from simulator.Buttons import *


class ButtonsTest(unittest.TestCase):
	"""A class to unit test `Buttons`.
	
	This code does its best to test all the cases in `Buttons`. It 
	simulates play and checks to see if the results are as expected. 
	More tests can be added later, and as of now, they are only 
	preliminary tests.
	"""

	def setUp(self):
		"""Overloaded method of `TestCase`.

		Run before any of the unit tests.
		"""
		self.bs : Buttons = Buttons()

	def test_initialization(self):
		"""Tests to make sure the `Buttons` class is set up right.

		Checks all the variables in the default `Buttons` instance and 
		makes sure they are set to the correct values.
		"""
		self.assertEqual(self.bs.num_sequenced, 0)
		self.assertEqual(self.bs.extra_not_sequenced, 0)
		self.assertEqual(self.bs.time, 0.0)
		
		self.assertTrue(self.bs.in_sequence)

		for b in self.bs.button_state:
			self.assertFalse(b.button_state)
			self.assertFalse(b.last_button_state)
			self.assertEqual(b.last_debounce_time, 0.0)


	def test_sequence_digits(self):
		"""Sequences the digits of PI in order.

		Just a basic sanity check to make sure the code works as 
		expected. Pushes the digits of PI in the correct order and 
		makes sure the score is calculated right.
		"""
		for d in map(int, Buttons.PI):
			self.bs.press_button(d)
			self.bs.update_buttons(.03) # Anything > .025
			self.bs.unpress_button(d)
			self.bs.update_buttons(.03) # Anything > .025

		self.assertEqual(self.bs.num_sequenced, len(Buttons.PI))
		self.assertEqual(self.bs.extra_not_sequenced, 0)
		self.assertTrue(self.bs.in_sequence)

		# Make sure the buttons are cleared
		for b in self.bs.button_state:
			self.assertFalse(b.button_state)
			self.assertFalse(b.last_button_state)
			self.assertFalse(b.reading)


	def test_spam_digits(self):
		"""Presses the same button over and over.
		
		This test just wants to make sure the scoring is done 
		correctly. If we just spam a button, we should not have 
		that count as in sequence.
		"""
		for _ in range(1000):
			self.bs.press_button(1)
			self.bs.update_buttons(.03) # Anything > .025
			self.bs.unpress_button(1)
			self.bs.update_buttons(.03) # Anything > .025

		self.assertEqual(self.bs.num_sequenced, 0)
                # For some reason, even though we do this 1000 times, 
                # only 999 of them count. I looked over the code, and 
                # Arduino code seems to have this too. As such, I 
                # count it a success, but I want to discuss it.
		self.assertEqual(self.bs.extra_not_sequenced, 999)
		self.assertFalse(self.bs.in_sequence)

		# Make sure the buttons are cleared
		for b in self.bs.button_state:
			self.assertFalse(b.button_state)
			self.assertFalse(b.last_button_state)
			self.assertFalse(b.reading)



if __name__ == '__main__':
	unittest.main()
