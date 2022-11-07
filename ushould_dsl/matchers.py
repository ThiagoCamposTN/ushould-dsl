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

class have(matcher):
    '''Checks the element count of a given collection.
    Works with iterables, requiring a qualifier expression for readability purposes, which is in fact only a syntax sugar.
    It also works with non-iterable objects, if the qualifier is an attribute name or method that contains the collection to be count.
    And allows counting collections within field objects.'''

    def __getattr__(self, collection_name):
        self._collection_name = collection_name
        self._humanized_collection_name = collection_name.replace('_', ' ')
        return self

    def should_match(self, left_value):
        self.left_value = left_value
        if hasattr(self.left_value, self._collection_name) and not utils.is_iterable(self.left_value):
            self._collection = getattr(self.left_value, self._collection_name)
            if not utils.is_iterable(self._collection):
                if callable(self._collection):
                    self._collection = self._collection()
                    if not utils.is_iterable(self._collection):
                        raise TypeError("target's '%s()' does not return an iterable" % self._collection_name)
                else:
                    raise TypeError("target's %r is not an iterable" % self._collection_name)
        elif utils.is_iterable(self.left_value):
            self._collection = self.left_value
        elif self._is_collection_through():
            owned_by_owned, owned = self._collection_name.split('_on_')
            owned_object = self._retrieve_owned_object(self.left_value, owned)
            owned_by_owned_object = self._retrieve_owned_object(owned_object, owned_by_owned)
            if not utils.is_iterable(owned_by_owned_object):
                if callable(getattr(owned_object, owned_by_owned)):
                    raise TypeError("target's '{}()' does not return an iterable".format(owned_by_owned))
                else:
                    raise TypeError("target's '{}' is not an iterable".format(owned_by_owned))
            self._collection = owned_by_owned_object
        else:
            raise TypeError("target does not have a '{}' collection, nor it is an iterable".format(
                self._collection_name))
        return self._compare()

    def _retrieve_owned_object(self, object_, owned):
        owned_object = getattr(object_, owned)
        if callable(owned_object):
            owned_object = owned_object()
        return owned_object

    def _is_collection_through(self):
        splitted = self._collection_name.split('_on_')
        if len(splitted) == 1:
            return False
        owned_by_owned, owned = splitted

        if not hasattr(self.left_value, owned):
            return False
        owned_object = self._retrieve_owned_object(self.left_value, owned)
        return hasattr(owned_object, owned_by_owned)

    def _compare(self):
        return self.right_value == len(self._collection)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected %r %r, got %r" % (self.right_value,
            self._humanized_collection_name, len(self._collection)))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected target not to have %d %r, got %r" % (
            self.right_value,
            self._humanized_collection_name, len(self._collection)))

class change(matcher):
    '''Checks for changes on the result of a given function, method or lambda.'''

    def __init__(self, right_value):
        self._by = None
        self._from_to = False
        self._only_to = False
        self.right_value = self._to_callable(right_value)

    def should_match(self, left_value=None):
        self.left_value = self._to_callable(left_value)
        self._before_result = copy.copy(self.right_value())
        self.left_value()
        self._after_result = self.right_value()

        if self._by is not None:
            self._actual_difference = self._after_result - self._before_result
            return self._by.comparison(self._expected_difference, self._actual_difference)
        elif self._from_to:
            return self._before_result == self._from_value and self._after_result == self._to_value
        elif self._only_to:
            self._failure_on_to_initial_value = False
            if self._before_result == self._to_value:
                self._failure_on_to_initial_value = True
                return False
            else:
                return self._after_result == self._to_value
        else:
            return self._after_result != self._before_result
    
    def message_for_failed_should(self, left):
        if self._by is not None:
            raise Should_NotSatisfied('result should have changed {} {}, but was changed by {}'.format(
                self._by.name, self._expected_difference, self._actual_difference))
        elif self._from_to:
            raise Should_NotSatisfied('result should have changed from {} to {}, but was changed from {} to {}'.format(
                self._from_value, self._to_value, self._before_result, self._after_result))
        elif self._only_to:
            if self._failure_on_to_initial_value:
                raise Should_NotSatisfied('result should have been changed to {}, but is now {}'.format(
                    self._to_value, self._before_result))
            else:
                raise Should_NotSatisfied('result should have changed to {}, but was changed to {}'.format(
                    self._to_value, self._after_result))
        else:
            raise Should_NotSatisfied('result should have changed, but is still {}'.format(
                self._before_result))

    def message_for_failed_should_not(self, left):
        if self._from_to:
            raise ShouldNot_NotSatisfied('result should not have changed from {} to {}'.format(
                  self._from_value, self._to_value))
        elif self._only_to:
            raise ShouldNot_NotSatisfied('result should not have changed to {}'.format(self._to_value))
        else:
            raise ShouldNot_NotSatisfied('should not have changed, but did change from {} to {}'.format(
                self._before_result, self._after_result))

    def by(self, difference):
        self._expected_difference = difference
        self._by = change._By(lambda exp_dif, act_dif: act_dif == exp_dif)
        return self

    def  by_at_least(self, difference):
        self._expected_difference = difference
        self._by = change._By(lambda exp_dif, act_dif: act_dif >= exp_dif, 'at least')
        return self

    def by_at_most(self, difference):
        self._expected_difference = difference
        self._by = change._By(lambda exp_dif, act_dif: act_dif <= exp_dif, 'at most')
        return self

    def from_(self, from_value):
        self._from_value = from_value
        self._from_to = True
        return self

    def to(self, to_value):
        self._only_to = not self._from_to
        self._to_value = to_value
        return self

    def _to_callable(self, obj):
        if callable(obj):
            return obj
        if utils.is_iterable(obj) and len(obj) >= 2 and callable(obj[0]):
            return lambda *params: obj[0](*obj[1:])
        else:
            raise TypeError('parameter passed to change must be a callable ' +
                'or a iterable having a callable as its first element')

    class _By(object):
        def __init__(self, comparison, name=''):
            self.name = ('by ' + name).strip()
            self.comparison = comparison

class include_keys(matcher):
    '''Checks if a dictionary includes all given keys.'''

    def __init__(self, *right_value):
        self.right_value = right_value

    def should_match(self, left_value=None):
        if type(left_value) != dict:
            raise TypeError("target must be a dictionary")
        self._non_present_keys  = set(self.right_value) - set(left_value.keys())

        return (len(self._non_present_keys) == 0)

    def should_not_match(self, left_value=None):
        self._non_present_keys  = set(self.right_value) - set(left_value.keys())
        self._present_keys      = set(self.right_value) - self._non_present_keys

        return (len(self._present_keys) == 0)

    def message_for_failed_should(self, left):
        r = utils.keys_in_phrase(self._non_present_keys, "key")
        raise Should_NotSatisfied("expected target to include {}".format(r))

    def message_for_failed_should_not(self, left):
        r = utils.keys_in_phrase(self._present_keys, "key")
        raise ShouldNot_NotSatisfied("expected target to not include {}".format(r))

class include_values(matcher):
    '''Checks if a dictionary includes all given values.'''

    def __init__(self, *right_value):
        self.right_value = right_value

    def should_match(self, left_value=None):
        self.check_left_value(left_value)
        self._non_present_keys  = set(self.right_value) - set(left_value.values())

        return (len(self._non_present_keys) == 0)

    def should_not_match(self, left_value=None):
        self.check_left_value(left_value)
        self._non_present_keys  = set(self.right_value) - set(left_value.values())
        self._present_keys      = set(self.right_value) - self._non_present_keys

        return (len(self._present_keys) == 0)
    
    def check_left_value(self, left_value):
        if type(left_value) is not dict:
            raise TypeError("target must be a dictionary")


    def message_for_failed_should(self, left):
        r = utils.keys_in_phrase(self._non_present_keys, "value")
        raise Should_NotSatisfied("expected target to include {}".format(r))

    def message_for_failed_should_not(self, left):
        r = utils.keys_in_phrase(self._present_keys, "value")
        raise ShouldNot_NotSatisfied("expected target to not include {}".format(r))

class respond_to(matcher):
    '''Checks if an object has a given attribute or method.'''

    def should_match(self, left_value=None):
        return hasattr(left_value, self.right_value)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected {} to respond to '{}'".format(left, self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected {} not to respond to '{}'".format(left, self.right_value))

class have_same_attribute_values_as(matcher):
    '''Verifies if an object have the same attribute values as another one.'''

    def should_match(self, left_value=None):
        found_different_attribute = False

        for key in self.right_value.__dict__.keys():
            got = left_value.__dict__.get(key)
            expected =  self.right_value.__dict__.get(key)
            if got != expected:
                found_different_attribute = True
                break

        return found_different_attribute == False

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected {} to have the same attribute values as {}".format(self.right_value, left))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected {} to have not the same attribute values as {}".format(self.right_value, left))


be_empty = _be_empty(None)

class have_at_least(have):
    '''The same as *have*, but checking if the element count is greater than or equal to the given value.
    Works for collections with syntax sugar, object attributes, or methods.'''

    def _compare(self):
        return self.right_value <= len(self._collection)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected %r %r, got %r" % (self.right_value,
            self._humanized_collection_name, len(self._collection)))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected target not to have at least %d %r, got %r" % (
            self.right_value,
            self._humanized_collection_name, len(self._collection)))

class have_at_most(have):
    '''The same as *have*, but checking if the element count is less than or equal to the given value.
    Works for collections with syntax sugar, object attributes, or methods.'''

    def _compare(self):
        return self.right_value >= len(self._collection)

    def message_for_failed_should(self, left):
        raise Should_NotSatisfied("expected %r %r, got %r" % (self.right_value,
            self._humanized_collection_name, len(self._collection)))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied("expected target not to have at most %d %r, got %r" % (
            self.right_value,
            self._humanized_collection_name, len(self._collection)))

class simple_matcher(matcher):
    def __init__(self, right_value):
        self.right_value = right_value
        self.custom = self.matcher()
        
    def should_match(self, left_value=None):
        return self.custom[0](left_value, self.right_value)
    
    def message_for_failed_should(self, left):
        raise Should_NotSatisfied(self.custom[1] % (left, 'not ', self.right_value))

    def message_for_failed_should_not(self, left):
        raise ShouldNot_NotSatisfied(self.custom[1] % (left, '', self.right_value))
