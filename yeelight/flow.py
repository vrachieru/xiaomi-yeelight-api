from enum import Enum
from itertools import chain

from .util import *

class Action(Enum):
    '''
    The Flow action enumeration
    Use this as the ``action`` parameter in a flow, to specify what should happen after the flow ends
    '''
    recover = 0
    stay = 1
    off = 2

class Flow(object):

    actions = Action

    def __init__(self, count=0, action=Action.recover, transitions=None):
        '''
        A complete flow, consisting of one or multiple transitions

        :param int count: the number of times to run this flow (0 to run forever)
        :param action action: the action to take after the flow stops
        :param list transitions: a list of :py:class:`FlowTransition <yeelight.FlowTransition>`
        '''
        if transitions is None:
            transitions = []

        self.count = count
        self.action = action
        self.transitions = transitions

    @property
    def expression(self):
        '''
        Return a YeeLight-compatible expression that implements this flow

        :rtype: list
        '''
        expr = chain.from_iterable(transition.as_list() for transition in self.transitions)
        expr = ", ".join(str(value) for value in expr)
        return expr

class FlowTransition(object):
    '''
    A single transition in the flow
    '''

    def as_list(self):
        '''
        Return a YeeLight-compatible expression that implements this transition

        :rtype: list
        '''
        brightness = min(int(self.brightness), 100)
        return [max(50, self.duration), self._mode, self._value, brightness]


class RGBTransition(FlowTransition):
    
    def __init__(self, red, green, blue, duration=500, brightness=100):
        '''
        A RGB transition

        :param int red: the value of red (0-255)
        :param int green: the value of green (0-255)
        :param int blue: the value of blue (0-255)
        :param int duration: the duration of the effect, in milliseconds (minimum is 50)
        :param int brightness: the brightness value to transition to (1-100)
        '''
        self.red = red
        self.green = green
        self.blue = blue

        # The mode value the YeeLight protocol mandates.
        self._mode = 1

        self.duration = duration
        self.brightness = brightness

    @property
    def _value(self):
        '''
        The YeeLight-compatible value for this transition
        '''
        red = clamp(self.red, 0, 255)
        green = clamp(self.green, 0, 255)
        blue = clamp(self.blue, 0, 255)

        return red * 65536 + green * 256 + blue

class SleepTransition(FlowTransition):
    
    def __init__(self, duration=500):
        '''
        A Sleep transition.

        :param int duration: the duration of the effect, in milliseconds (minimum is 50)
        '''
        # The mode value the YeeLight protocol mandates.
        self._mode = 7

        # Ignored by YeeLight.
        self._value = 1
        self.brightness = 2

        self.duration = duration
