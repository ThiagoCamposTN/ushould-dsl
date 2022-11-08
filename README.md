# uShould-DSL: Improve readability for should-style expectations

The goal of *uShould-DSL* is to write should expectations in the MicroPython implementation of Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language and the MicroPython implementation constraints).

This project is a port of [Should-DSL](https://github.com/nsi-iff/should-dsl).

## Documentation

* [uShould-DSL Matchers](./docs/available_matchers.md) - Description and usage of all available matchers;
* [Custom Matchers](./docs/custom_matchers.md) - How to create custom matchers;
* [Contributing](./docs/contributing.md) - How you can contribute to the library;
* [License](./LICENSE) - MIT License.


## Usage

In order to use this DSL, you need to import everything from ``ushould_dsl`` module.

For example:

```python
from ushould_dsl import *

1 |should| equal_to(1)
value('should') |should| include('oul')
3 |should| be_into([0, 1, 2])
```

```bash
Traceback (most recent call last):
...
Should_NotSatisfied: 3 is not into [0, 1, 2]
```


The ``equal_to`` matcher verifies object equality. If you want to ensure identity, you must use ``be`` as matcher:

```python
2 |should| be(2)
```


A nice example of exceptions would be:

```python
def raise_zerodivisionerror():
    return 1/0

raise_zerodivisionerror |should| throw(ZeroDivisionError)
```

``should`` has a negative version: ``should_not``:

```python
from ushould_dsl import *

2 |should_not| be_into([1, 3, 5])
value('should') |should_not| include('oul')
```

```bash
Traceback (most recent call last):
...
ShouldNotSatisfied: 'should' does include 'oul'
```

## How to include in your project

Using this library in your project can be as easy as downloading this project, copying the `ushould_dsl` folder into your project and importing the library in your script.

You can also copy the folder into your MicroPython library folder. You can find its location by running in your MicroPython terminal:

```bash
>>> import sys
>>> sys.path
['', '.frozen', '.micropython/lib', '/usr/lib/micropython']
```

Generally, the library folder will be in the `/lib/` folder on root of the filesystem from your microcontroller. This can change if using Micropython for Unix.

After finding the `/lib/` folder, just copy the `ushould_dsl` folder into it, now your MicroPython can use the *ushould_dsl* library!

## Observations and Limitations

Due to the fundamental differences in MicroPython's Python implementation, some features could not be implemented, and others had their implementations modified according to the functions offered by Micropython.

The cases where the libraries differ are properly documented, and the tests used by the original library are also present in this project, to ensure as much parity of expected behavior as possible.

One of the most proeminent is the use of the `value` object. It's usage is obligatory with strings because MicroPython doesn't support the *or* operation for this datatype. Since this behavior is fundamental for the library to work, it was required to implement an object that packages these strings. In every other case, the usage of `value` is optional.
