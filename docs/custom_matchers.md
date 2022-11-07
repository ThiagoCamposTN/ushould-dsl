# Custom Matchers

Extending uShould-DSL with custom matchers is very easy. It is possible to add matchers through simple and complex classes, for simple and complex behaviors.

## Simple Custom Matchers

Expanding uShould-DSL with simple matchers is as easy as having your new matcher class extend from `simple_matcher`. Just implement the function `matcher` with *self*  as the only parameter and have it return a tuple containing two elements.

The first tuple item is the function (or lambda), receiving two parameters, to be run for the comparison, and the second is the failure message. The failure message must have three string formatting operators (such as `%s`, `%r`, `%d`, etc) placeholders. The first and the third will be used for the actual and expected values, respectively. The second operator will be the placeholder for a 'not ' string for failed expectations or an empty string for a succeeded expectation - and the opposite if `should_not` is used.

```bash
>>> from ushould_dsl import simple_matcher, should, should_not

>>> class be_the_square_root_of(simple_matcher):
...     def matcher(self):
...         import math
...         return (lambda x, y: x == math.sqrt(y), "%s is %sthe square root of %s")

>>> 3 |should| be_the_square_root_of(9)

>>> 4 |should| be_the_square_root_of(9)
Traceback (most recent call last):
...
ShouldNotSatisfied: 4 is not the square root of 9


>>> 4 |should_not| be_the_square_root_of(16)
Traceback (most recent call last):
...
ShouldNotSatisfied: 4 is the square root of 16
```

## Not so Simple Matchers

If your custom matcher has a more complex behavior, or if both should and should_not messages differ, you can create custom matchers by extending the `matcher` class. In fact, this is the preferred way to create matchers, being the `simple_matcher` class only a convenience for simple cases.

Below is an example of the square root matcher defined as a standard class:

```bash
>>> from ushould_dsl import matcher, should, should_not
>>> import math
>>> 
>>> class be_the_square_root_of(matcher):
...     
...     def should_match(self, left_value=None):
...         self._expected = math.sqrt(self.right_value)
...         return left_value == self._expected
...     
...     def message_for_failed_should(self, left):
...         raise Should_NotSatisfied("expected '{}' to be the square root of '{}', got '{}'.".format(left, self.right_value, self._expected))
...     
...     def message_for_failed_should_not(self, left):
...         raise ShouldNot_NotSatisfied("expected '{}' not to be the square root of '{}'.".format(left, self.right_value))
... 
>>> 3 |should| be_the_square_root_of(9)
>>> 4 |should| be_the_square_root_of(9)
Traceback (most recent call last):
...
Should_NotSatisfied: expected '4' to be the square root of '9', got '3.0'.
>>> 2 |should_not| be_the_square_root_of(4.1)
>>> 2 |should_not| be_the_square_root_of(4)
Traceback (most recent call last):
...
ShouldNot_NotSatisfied: expected '2' not to be the square root of '4'.
```

A matcher class must fill the following requirements:

* A *should_match* method receiving the actual value of the expectation as a parameter (e.g., in *2 \|should\| equal_to(3)* the left is 2 and the right is 3). This method should return the boolean result of the desired comparison;
* Two methods, called *message_for_failed_should* and *message_for_failed_should_not* for returning the failure messages for, respectively, *should* and *should_not*.

You can also overwrite the *should_not_match* method, but it's not mandatory. By default, it returns the negation of the *should_match* method, but in particular scenarios you may need to describe a different behavior.

## should or should_not?

For most of the matchers, `should` is the exact opposite to `should_not`. For the same expected and actual values, if *should_not* fails, *should* will pass; in the same way, if *should* fails, *should_not* passes. However, this is not true for all matchers. Depending on your matcher semantics, the same expected and actual values can fail or pass both *should* and *should_not*. A good example is the matcher `include_keys`. The calls shown below will fail:

```bash
>>> {'a': 1, 'b': 2, 'c': 3} |should| include_keys('a', 'd')
Traceback (most recent call last):
...
ShouldNotSatisfied: expected target to include key 'd'

>>> {'a': 1, 'b': 2, 'c': 3} |should_not| include_keys('a', 'd')
Traceback (most recent call last):
...
ShouldNotSatisfied: expected target to not include key 'a'
```