###########################################################################################################
# SUBMIT YOUR OWN CUSTOM PATTERN AND SHARE WITH THE WORLD YOUR LED ANIMATIONS!
# Visit https://github.com/project-alice-assistant/HermesLedControl/issues/new?template=custom-pattern-proposal.md
# for more information
#
# Check models/LedPattern.py for the available functions
# Do NEVER have a function call a super class function directly!!
# It could cause a deadlock! Instead, call self._controller.THE_METHOD_YOU_WANT
#
# @author:
# @weblink:
# @email:
#
###########################################################################################################

from models.LedPattern import LedPattern
from models.LedsController import LedsController
import time

class CustomLedPattern(LedPattern):

	def __init__(self, controller: LedsController):
		super().__init__(controller)
        self._colors = {
            'black'      : [  0,   0,   0, 0],
            'blue'       : [  0,   0, 255, self._controller.defaultBrightness],
            'red'        : [255,   0,   0, self._controller.defaultBrightness],
            'dark red'   : [  5,   0,   0, 1],
            'yellow'     : [255, 255,   0, self._controller.defaultBrightness],
            'green'      : [  0, 255,   0, self._controller.defaultBrightness],
            'dark green' : [  0,   5,   0, 1]
        }

    def nothing(self, *args):
        self._logger.info('nothing')
        pass # Superseeded

    def wakeup(self, *args):
        self._logger.info('wakeup')
        color = self._colors['yellow']
        self._controller.setLedRGB(0, color)
        self._controller.setLedRGB(1, color)
        self._controller.setLedRGB(2, color)
        self._controller.show()

    def listen(self, *args):
        self._logger.info('listen')
        color = self._colors['yellow']
        self._animator.breath(color=color, minBrightness=2, maxBrightness=self._controller.defaultBrightness, speed=40)

    def think(self, *args):
        self._logger.info('think')
        color = self._colors['blue']
        self._animator.rotate(color=color, speed=40, trail=int(self.numLeds / 3))

    def speak(self, *args):
        self._logger.info('speak')
        color = self._colors['blue']
        self._animator.breath(color=color, minBrightness=2, maxBrightness=self._controller.defaultBrightness, speed=40)

    def idle(self):
        self._logger.info('idle')
        self._controller.clearLeds()
        black = self._colors['black']
        color = self._colors['dark green']
        self._controller.setLedRGB(0, black)
        self._controller.setLedRGB(1, color)
        self._controller.setLedRGB(2, black)
        self._controller.show()

    def off(self, *args):
        self._logger.info('off')
        self._controller.clearLeds()
        black = self._colors['black']
        color = self._colors['dark red']
        self._controller.setLedRGB(0, black)
        self._controller.setLedRGB(1, color)
        self._controller.setLedRGB(2, black)
        self._controller.show()

    def onError(self, *args):
        self._logger.info('onError')
        color = self._colors['red']
        self._animator.blink(color=color, minBrightness=2, maxBrightness=self._controller.defaultBrightness, speed=100, repeat=3)

    def onSuccess(self, *args):
        self._logger.info('onSuccess')
        color = self._colors['green']
        self._animator.blink(color=color, minBrightness=2, maxBrightness=self._controller.defaultBrightness, speed=100, repeat=3)

    def updating(self, *args):
        self._logger.info('updating')
        pass # Superseeded

    def call(self, *args):
        self._logger.info('call')
        pass # Superseeded

    def setupMode(self, *args):
        self._logger.info('setupMode')
        pass # Superseeded

    def conError(self, *args):
        self._logger.info('conError')
        pass # Superseeded

    def message(self, *args):
        self._logger.info('message')
        pass # Superseeded

    def dnd(self, *args):
        self._logger.info('dnd')
        pass # Superseeded

    def onVolumeSet(self, *args):
        self._logger.info('onVolumeSet')
        pass # Superseeded

    def onButton1(self, *args):
        self._logger.info('onButton1')
        siteId = self._controller._mainClass._me;
        newState = 'OFF' if self._controller.active else 'ON'
        self._logger.info('Turning ' + siteId + ' ' + newState)
        self._controller._mainClass._mqttClient.publish('jarvis/satellite/' + siteId + '/active', newState, retain=True);
        #self._controller.toggleState()

    def onStart(self, *args):
        self._logger.info('onStart')
        self.idle()

    def onStop(self, *args):
        self._logger.info('onStop')
        self._controller.clearLeds()
        #self.off()
