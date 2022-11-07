import re
from .exceptions import Should_NotSatisfied, ShouldNot_NotSatisfied, MicroPythonNotImplemented
from . import utils
from .infixes import should, should_not
import copy
import sys

class matcher:
    def __init__(self, right_value):
        self.right_value = right_value

    def should_match(self):
        raise NotImplementedError()

    def should_not_match(self, left_value=None):
        return not self.should_match(left_value)
    
    def message_for_failed_should(self, left):
        raise NotImplementedError()

    def message_for_failed_should_not(self, left):
        raise NotImplementedError()

class equal_to_ignoring_case(matcher):
    '''Checks equality of strings ignoring case.'''

    def should_match(self, left_value=None):
        return (self.right_value.lower() == left_value.lower())
    
    def message_for_failed_should(self, left_value):
        raise Should_NotSatisfied("expected '{}' to be equal to '{}'.".format(left_value, self.right_value))

    def message_for_failed_should_not(self, left_value):
        raise ShouldNot_NotSatisfied("expected '{}' not to be equal to '{}'.".format(left_value, self.right_value))

class equal_to(matcher):
    '''Checks object equality (not identity).
    This matcher can check string equality ignoring case too.
    A bonus: you can combine this feature with the diff parameter too.'''

    def __init__(self, right_value, case_sensitive=True):
        self.right_value = right_value
        self.case_sensitive = case_sensitive

    def should_match(self, left_value=None):
        if self.case_sensitive:
            return (self.right_value == left_value)
        else:
            return equal_to_ignoring_case.should_match(self, left_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be '{}'.".format(left, self.right_value))

class include(matcher):
    '''Verify if an object is contained (*be_into*) or contains (*contain*) another.
    The *contain* and *include* matchers do exactly the same job.'''
    def should_match(self, left_value=None):
        return (self.right_value in left_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be '{}'.".format(left, self.right_value))

class be(matcher):
    '''Checks object identity (*is*).'''

    def should_match(self, left_value=None):
        return (self.right_value is left_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be '{}'.".format(left, self.right_value))

class include(matcher):
    '''Verify if an object contains another. The `include` and `contain` matchers do exactly the same job.'''

    def should_match(self, left_value=None):
        return (self.right_value in left_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to include '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to include '{}'.".format(left, self.right_value))

class contain(include):
    '''Verify if an object contains another. The `contain` and `include` matchers do exactly the same job.'''

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to contain '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to contain '{}'.".format(left, self.right_value))

class be_into(matcher):
    '''Verify if an object is contained in another.'''

    def should_match(self, left_value=None):
        return (left_value in self.right_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be into '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be into '{}'.".format(left, self.right_value))

class be_greater_than(matcher):
    '''Simply check the return of comparisons.'''
    def should_match(self, left_value=None):
        return (left_value > self.right_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be greater than '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be greater than '{}'.".format(left, self.right_value))

class be_greater_than_or_equal_to(matcher):
    '''Simply check the return of comparisons.'''
    def should_match(self, left_value=None):
        return (left_value >= self.right_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be greater than or equal to '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be greater than or equal to '{}'.".format(left, self.right_value))

class be_less_than(matcher):
    '''Simply check the return of comparisons.'''
    def should_match(self, left_value=None):
        return (left_value < self.right_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be less than '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be less than '{}'.".format(left, self.right_value))

class be_less_than_or_equal_to(matcher):
    '''Simply check the return of comparisons.'''
    def should_match(self, left_value=None):
        return (left_value <= self.right_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be less than or equal to '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be less than or equal to '{}'.".format(left, self.right_value))

class be_kind_of(matcher):
    '''Verifies if an object is of a given type.'''

    def should_match(self, left_value=None):
        return isinstance(left_value, self.right_value)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("'{}' is not a kind of '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("'{}' is a kind of '{}'.".format(left, self.right_value))

class be_instance_of(be_kind_of):
    '''Same as `be_kind_of`, but using *instance* word.'''
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be an instance of '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be an instance of '{}'.".format(left, self.right_value))

class be_like(matcher):
    '''Checks matching against a regular expression.'''

    def __init__(self, right_value, flags=0):
        self.right_value = right_value
        self.flags = flags
        
        if self.flags != 0:
            raise MicroPythonNotImplemented("MicroPython does not implement flags for matching in regex.")

    def should_match(self, left_value=None):
        return re.match(self.right_value, left_value, self.flags) is not None
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be like '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be like '{}'.".format(left, self.right_value))

class _be_empty(matcher):
    '''Verifies if an object is empty. Works for lists, strings, tuples, dictionaries, and any object that implements *__len__()*.'''

    def should_match(self, left_value=None):
        return (utils.is_empty(left_value))
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected '{}' to be empty.".format(left))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected '{}' not to be empty.".format(left))

class be_thrown_by(matcher):
    '''Check the raising of exceptions.'''

    def should_match(self, left_value=None):
        try:
            if type(self.right_value) is tuple:
                fun = self.right_value[0]
                fun(*self.right_value[1:])
            else:
                self.right_value()
        except left_value:
            return True
        except Exception as e:
            return False
        
        return False

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("'{}' is not thrown by '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("'{}' is thrown by '{}'.".format(left, self.right_value))

class close_to(matcher):
    '''Checks if a number is close to another, given a delta.'''

    def __init__(self, right_value, delta):
        self.right_value = right_value
        self.delta = delta

    def should_match(self, left_value=None):
        return abs(round(self.right_value - left_value, 3)) <= round(self.delta, 3)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected to be close to '{}' (within +/- '{}'), got '{}'".format(self.right_value, self.delta, left))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected not to be close to '{}' (within +/- '{}'), got '{}'".format(self.right_value, self.delta, left))

class end_with(matcher):
    '''Verifies if a string ends with a given suffix.'''

    def should_match(self, left_value=None):
        return left_value.endswith(self.right_value)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("'{}' does not end with '{}'".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("'{}' does end with '{}'".format(left, self.right_value))

class include_all_of(matcher):
    '''Check if an iterable includes all elements of another.'''

    def should_match(self, left_value=None):
        return set(self.right_value).issubset(left_value)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("'{}' does not include all of '{}'".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("'{}' does include all of '{}'".format(left, self.right_value))

class include_in_any_order(include_all_of):
    '''Check if an iterable includes all elements of another. Do the same as `include_all_of`.'''

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("'{}' does not include in any order '{}'".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("'{}' does include in any order '{}'".format(left, self.right_value))

class include_any_of(matcher):
    '''Checks if an iterable includes any element of another.'''

    def should_match(self, left_value=None):
        return not set(self.right_value).isdisjoint(left_value)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("'{}' does not include any of '{}'.".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("'{}' does include any of '{}'.".format(left, self.right_value))

class start_with(matcher):
    '''Verifies if a string starts with a given prefix.'''

    def should_match(self, left_value=None):
        return left_value.startswith(self.right_value)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("'{}' does not start with '{}'".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("'{}' does start with '{}'".format(left, self.right_value))

class throw(matcher):
    '''Check the raising of exceptions.'''

    def __init__(self, right_value, message=None, message_regex=None):
        self._expected_message = message
        self._expected_message_regex = message_regex
        if isinstance(right_value, Exception):
            self._expected_exception = right_value.__class__
            if message is None and message_regex is None:
                self._expected_message = str(right_value)
        else:
            self._expected_exception = right_value
    
    def should_match(self, left_value=None):
        self._left_value = left_value
        if utils.is_iterable(left_value):
            args = left_value[1:]
            left_value = left_value[0]
        else:
            args = []
        try:
            left_value(*args)
            self._actual_exception = None
            return False
        except self._expected_exception:
            e = sys.exc_info()[1]
            self._actual_exception = self._expected_exception
            self._actual_message = str(e)
            return self._handle_expected_message() and self._handle_expected_regex()
        except Exception:
            e = sys.exc_info()[1]
            self._actual_exception = e.__class__
            return False
    
    def _using_message(self):
        return self._expected_message is not None

    def _using_regex(self):
        return self._expected_message_regex is not None and not self._using_message()

    def _got_exception(self):
        return hasattr(self, '_actual_exception') and self._actual_exception is not None

    def _handle_expected_message(self):
        if not self._using_message():
            return True
        return self._expected_message == self._actual_message

    def _handle_expected_regex(self):
        if not self._using_regex():
            return True
        return re.match(self._expected_message_regex, self._actual_message) is not None

    def message_for_failed_should(self, left):
        message = "expected to throw %r" % self._expected_exception.__name__
        if self._using_message():
            message += " with the message %r" % self._expected_message
        elif self._using_regex():
            message += " with a message that matches %r" % self._expected_message_regex
        if self._got_exception():
            message += ', got %r' % self._actual_exception.__name__
            if self._using_message():
                message += ' with %r' % self._actual_message
            elif self._using_regex():
                message += ' with no match for %r' % self._actual_message
        else:
            message += ', got no exception'
        raise Should_NotSatisfied(message)

    def message_for_failed_should_not(self, left):
        message = "expected not to throw %r" % self._expected_exception.__name__
        if self._using_message():
            message += " with the message %r" % self._expected_message
        elif self._using_regex():
            message += " with a message that matches %r" % self._expected_message_regex

        raise ShouldNot_NotSatisfied("%s, but got it" % message)

