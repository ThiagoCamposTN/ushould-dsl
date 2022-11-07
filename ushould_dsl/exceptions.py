class Should_NotSatisfied(Exception):
    pass

class ShouldNot_NotSatisfied(Exception):
    pass

'''
Exception raised for functionality expected from the original Should DSL,
but it is limited by MicroPython to run as intended. 
'''
class MicroPythonNotImplemented(RuntimeError):
    pass
