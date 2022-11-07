from .matchers import *

class value:
    '''Necessary in order to circumvent the fact that you can't apply 'or' operator with strings in micropython.'''

    def __init__(self, input_value):
        self._value = input_value
    
    def __or__(self, infix):
        # value() | infix
        return infix.__ror__(self._value)


def aliases(**kwargs):
    for k in kwargs:
        result = "{} = {}".format(kwargs[k], k)
        exec(result)
