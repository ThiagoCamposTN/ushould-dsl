# uShould-DSL Matchers

You can find below some explanations on the available matchers of *ushould_dsl* package.


Before all, you need to import it:

```python
from ushould_dsl import *
```

---


## be

Checks object identity (*is*).

```bash
>>> 1 |should| be(1)
>>>
>>> a = "some message"
>>> b = "some message"
>>> id(a) == id(b) # the strings are equal but with different ids
False
```

```bash
>>> a |should| be(b)
Traceback (most recent call last):
...
ShouldNotSatisfied: 'some message' was expected to be 'some message'
```

```bash
>>> c = "another message"
>>> d = c
>>> id(c) == id(d)
True
```

```bash
>>> c |should| be(d)
```

## be_greater_than, be_greater_than_or_equal_to, be_less_than, be_less_than_or_equal_to

Simply check the return of comparisons.

```bash
>>> 1       |should_not | be_greater_than(1)
>>> 2       |should     | be_greater_than_or_equal_to(2)
>>> 0.1     |should     | be_less_than(0.11)
>>> 3000    |should     | be_less_than_or_equal_to(3001)
```


## be_into, contain, include

Verify if an object is contained (`be_into`) or contains (`contain`) another. The `contain` and `include` matchers do exactly the same job.

```bash
>>> 1               |should     | be_into(range(2))
>>> ['a']           |should_not | be_into(['a'])
>>> ['a']           |should     | be_into([['a']])
>>> ['x', 'y', 'z'] |should     | contain('z')
>>> ['x', 'y', 'z'] |should     | include('z')
```

## be_empty

Verifies if an object is empty. Works for lists, strings, tuples, dictionaries, and any object that implements *\_\_len\_\_()*.

```bash
>>> '' |should| be_empty
>>> [] |should| be_empty
>>> () |should| be_empty
>>> {} |should| be_empty
```

## be_kind_of, be_instance_of

Verifies if an object is of a given type. `be_instance_of` works the exact same way but using *instance* word.

```bash
>>> 1 |should| be_kind_of(int)
>>> 1 |should| be_instance_of(int)

>>> class Foo: pass
>>> Foo() |should| be_kind_of(Foo)
>>> Foo() |should| be_instance_of(Foo)
>>> class Bar(Foo): pass
>>> Bar() |should| be_kind_of(Foo)
>>> Bar() |should| be_instance_of(Foo)
```


## be_like

Checks matching against a regular expression.

```bash
>>> value('Hello World')    |should     | be_like(r'Hello W.+')
>>> value('123 is a number')|should_not | be_like(r'^[12]+ is a number')
```

`be_like` accepts flags from *re* module as its (optional) second parameter.

```bash
>>> import re
>>> value('Hello\nWorld') |should| be_like(r'hell.+', re.DOTALL|re.IGNORECASE)
```

## be_thrown_by, throw

Check the raising of exceptions.

```bash
>>> ZeroDivisionError       |should     | be_thrown_by(lambda: 1/0)
>>> (lambda: 1/0.000001)    |should_not | throw(ZeroDivisionError)
```

`throw` matcher also supports message checking.

```bash
>>> def foo(): raise TypeError("Hey, it's cool!")
>>> foo |should| throw(TypeError, message="Hey, it's cool!")
>>> foo |should| throw(TypeError, message="This won't work...")
Traceback (most recent call last):
...
ShouldNotSatisfied: expected to throw 'TypeError' with the message "This won't work...", got 'TypeError' with "Hey, it's cool!"
```

If the function or method has parameters, it must be called within a lambda or using a tuple. The following ways are both equivalent:

```bash
>>> def divide(x, y): return x / y
>>> (lambda: divide(1, 0))  |should| throw(ZeroDivisionError)
>>> (divide, 1, 0)          |should| throw(ZeroDivisionError)
```

The same works for `be_thrown_by` matcher.


## change

Checks for changes on the result of a given function, method or lambda.

```bash
>>> class Box(object):
...     def __init__(self):
...         self.items = []
...     def add_items(self, *items):
...         for item in items:
...             self.items.append(item)
...     def item_count(self):
...         return len(self.items)
...     def clear(self):
...         self.items = []
>>> box = Box()
>>> box.add_items(5, 4, 3)
>>> box.clear |should       | change(box.item_count)
>>> box.clear |should_not   | change(box.item_count)
```

If the function or method has parameters, it must be called within a lambda or using a tuple. The following ways are both equivalent:

```bash
>>> (lambda: box.add_items(1, 2, 3))    |should| change(box.item_count)
>>> (box.add_items, 1, 2, 3)            |should| change(box.item_count)
```

`change` also works with an arbitrary change count:

```bash
>>> box.clear()
>>> box.add_items(1, 2, 3)
>>> box.clear |should| change(box.item_count).by(-3)
>>> box.add_items(1, 2, 3)
>>> box.clear |should| change(box.item_count).by(-2)
Traceback (most recent call last):
...
ShouldNotSatisfied: result should have changed by -2, but was changed by -3
```

`change` has support for maximum and minumum with *by_at_most* and *by_at_least*:

```bash
>>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(3)
>>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(2)
Traceback (most recent call last):
...
ShouldNotSatisfied: result should have changed by at most 2, but was changed by 3
```

```bash
>>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(3)
>>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(4)
Traceback (most recent call last):
...
ShouldNotSatisfied: result should have changed by at least 4, but was changed by 3
```

Finally, `change` supports specifying both the initial and final values or only the final one:

```bash
>>> box.clear()
>>> (box.add_items, 1, 2, 3) |should| change(box.item_count).from_(0).to(3)
>>> box.clear |should| change(box.item_count).to(0)
>>> box.clear |should| change(box.item_count).to(0)
Traceback (most recent call last):
...
ShouldNotSatisfied: result should have been changed to 0, but is now 0
```


## close_to

Checks if a number is close to another, given a delta.

```bash
>>> 1   |should     | close_to(0.9, delta=0.1)
>>> 0.8 |should     | close_to(0.9, delta=0.1)
>>> 1   |should_not | close_to(0.89, delta=0.1)
>>> 4.9 |should     | close_to(4, delta=0.9)
```

### Implementation differences

Originally, `close_to` uses the *Decimal* library to make its calculations, but this library is not implemented in Micropython. Due to the floating number nature, the precision for comparisons between floats is not perfect, and the Decimal library took care of solving this problem. The workable solution in Micropython was to use floats but round the values to high precision of 10 decimal places. Values with a precision higher than this may not return the expected result.

Example:

```bash
>>> round(9E-12, 10) == round(1E-12, 10)
True
```


## end_with

Verifies if a string ends with a given suffix.

```bash
>>> value("Brazil champion of 2010 FIFA world cup") |should| end_with('world cup')
>>> value("hello world") |should_not| end_with('worlds')
```

## equal_to

Checks object equality (not identity).

```bash
>>> 1 |should| equal_to(1)

>>> class Foo: pass
>>> Foo() |should_not| equal_to(Foo())

>>> class Foo(object):
...    def __eq__(self, other):
...        return True
>>> Foo() |should| equal_to(Foo())
```


```bash
>>> value('big') |should_not| equal_to('big\nstring')
```

This matcher can check string equality ignoring case too.

```bash
>>> value('abc') |should| equal_to('abC', case_sensitive=False)
```

### Implementation differences

Originally, `equal_to` has a parameter to return the difference between text strings, but unlike the original library, *ushould_dsl* does not support this functionality because there is no alternative to the *difflib* library in micropython.

There are also unexpected results from using the *case_sensitive* parameter in certain cases. This is explained in `equal_to_ignoring_case` in more detail.

## equal_to_ignoring_case

Checks equality of strings ignoring case.

```bash
>>> value('abc')    |should| equal_to_ignoring_case('AbC')

>>> value('XYZAb')  |should| equal_to_ignoring_case('xyzaB')
```

### Implementation differences

Micropython does not perform the *lower* and *upper*  operations with special characters, unlike python. Therefore, phrases with special characters can return unexpected results. The same is true for the *case_sensitive* parameter of the `equal_to` matcher.

## have

Checks the element count of a given collection. Works with iterables, requiring a qualifier expression for readability purposes, which is in fact only a syntax sugar.

```bash
>>> ['b', 'c', 'd'] |should| have(3).elements

>>> [1, [1, 2, 3], 'a', lambda: 1, 2**3] |should| have(5).heterogeneous_things

>>> ['asesino', 'japanische kampfhoerspiele', 'facada'] |should| have(3).grindcore_bands

>>> value("left") |should| have(4).characters
```

`have` also works with non-iterable objects, if the qualifier is an attribute name or method that contains the collection to be count.

```bash
>>> class Foo:
...     def __init__(self):
...         self.inner_things = ['a', 'b', 'c']
...     def pieces(self):
...         return range(10)
>>> Foo() |should| have(3).inner_things
>>> Foo() |should| have(10).pieces
```

`have` allows counting collections within field objects.

```bash
>>> class Field:
...     def __init__(self, number_of_players):
...         self.players = range(number_of_players)

>>> class SoccerGame:
...      def __init__(self):
...          self.field = Field(22)

>>> SoccerGame() |should| have(22).players_on_field
```

## have_at_least

The same as `have`, but checking if the element count is greater than or equal to the given value. Works for collections with syntax sugar, object attributes, or methods.

```bash
>>> range(20) |should       | have_at_least(19).items
>>> range(20) |should       | have_at_least(20).items
>>> range(20) |should_not   | have_at_least(21).items
```

## have_at_most

The same as `have`, but checking if the element count is less than or equal to the given value. Works for collections with syntax sugar, object attributes, or methods.

```bash
>>> range(20) |should_not   | have_at_most(19).items
>>> range(20) |should       | have_at_most(20).items
>>> range(20) |should       | have_at_most(21).items
```

## have_same_attribute_values_as

Verifies if an object have the same attribute values as another one.

```bash
>>> class Foo(object):
...    def __init__(self, a, b):
...        self.a = a
...        self.b = b

>>> a = Foo(1,2)
>>> b = Foo(1,2)

>>> a |should| have_same_attribute_values_as(b)
```

## include_all_of, include_in_any_order

Check if an iterable includes all elements of another. Both matchers do the same job.

```bash
>>> [4, 5, 6, 7]    |should     | include_all_of([5, 6])
>>> [4, 5, 6, 7]    |should     | include_in_any_order([5, 6])
>>> ['b', 'c']      |should     | include_all_of(['b', 'c'])
>>> ['b', 'c']      |should     | include_in_any_order(['b', 'c'])
>>> ['b', 'c']      |should_not | include_all_of(['b', 'c', 'a'])
>>> ['b', 'c']      |should_not | include_in_any_order(['b', 'c', 'a'])
```

## include_any_of

Checks if an iterable includes any element of another.

```bash
>>> [1, 2, 3]   |should| include_any_of([3, 4, 5])
>>> (1,)        |should| include_any_of([4, 6, 3, 1, 9, 7])
```

## include_keys

Checks if a dictionary includes all given keys.

```bash
>>> {'a': 1, 'b': 2, 'c': 3} |should    | include_keys('a', 'b')
>>> {'a': 1, 'b': 2, 'c': 3} |should_not| include_keys('d')
```

## include_values

Checks if a dictionary includes all given values.

```bash
>>> {'a': 1, 'b': 2, 'c': 3} |should| include_values(2, 3)
>>> {'a': 1, 'b': 2, 'c': 3} |should_not| include_values(0, 4)
```

## respond_to

Checks if an object has a given attribute or method.

```bash
>>> value('some string') |should| respond_to('startswith')

>>> class Foo:
...     def __init__(self):
...         self.foobar = 10
...     def bar(self): pass
>>> Foo() |should| respond_to('foobar')
>>> Foo() |should| respond_to('bar')
```

### Implementation differences

The behavior of `respond_to` between implementations are different: micropython does not have *_Foo__name_clashing_bar*, but *__name_clashing_bar*.

## start_with

Verifies if a string starts with a given prefix.

```bash
>>> value("Brazil champion of 2010 FIFA world cup") |should| start_with('Brazil champion')
>>> value("hello world") |should_not| start_with('Hello')
```