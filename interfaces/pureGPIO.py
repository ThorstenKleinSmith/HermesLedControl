#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.Exceptions 	import InterfaceInitError
from gpiozero 			import LED
from models.Interface 	import Interface

class PureGPIO(Interface):

	def __init__(self, numLeds, pinout):
		super(PureGPIO, self).__init__(numLeds)

		if len(pinout) != numLeds:
			raise InterfaceInitError('Pure GPIO number of led versus pinout declaration missmatch')

		self._pinout 	= pinout
		self._image 	= self._newArray()

		self._leds 		= []
		for pin in self._pinout:
			self._leds.append(LED(pin=pin, active_high=True, initial_value=False))


	def setPixel(self, ledNum, red, green, blue, brightness):
		"""
		Set pixel here doesn't take RGB(W) values but sets the led on/off instead
		:type ledNum: int
		"""

		if ledNum < 0 or ledNum >= self._numLeds:
			self._logger.warning('Trying to access a led index out of reach')
			return

		if red > 0 or green > 0 or blue > 0:
			self._image[ledNum] = 1
		else:
			self._image[ledNum] = 0


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._image = self._newArray()
		self.show()


	def show(self):
		for index, status in enumerate(self._image):
			if status <= 0:
				self._leds[index].off()
			else:
				self._leds[index].on()


	def _newArray(self):
		return [0] * self._numLeds