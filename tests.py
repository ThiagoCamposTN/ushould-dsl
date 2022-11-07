from ushould_dsl import *
from ushould_dsl import utils
import time


class CustomTests:
    def set_up(self):
        pass
    
    def test_equal_to_ignoring_case(self):
        value("I'm specifying it")  |should     | equal_to_ignoring_case("I'M SPECIFYING it")

        value("I")                  |should     | equal_to_ignoring_case("i")
        value("i")                  |should     | equal_to_ignoring_case("I")
        value("I")                  |should     | equal_to_ignoring_case("I")

        value("I")                  |should_not | equal_to_ignoring_case("wi")
        value("I")                  |should_not | equal_to_ignoring_case("iw")

        value("Atencao") |should| equal_to_ignoring_case("ATENCAO")

        value('abc') |should| equal_to_ignoring_case('AbC')
        value('XYZAb') |should| equal_to_ignoring_case('xyzaB')

    def test_equal_to(self):
        value(1)        |should     | equal_to(1)
        value(2)        |should_not | equal_to(3)
        value(1)        |should_not | equal_to(2)
        name = 'dsl'
        value(name)     |should     | equal_to('dsl')
        value(name)     |should_not | equal_to('dsl\ntest')
        value('CaSe')   |should     | equal_to('case', case_sensitive=False)
        value('CaSE')   |should_not | equal_to('CasE\nInsensitive', case_sensitive=False)

        class Foo: pass
        Foo() |should_not| equal_to(Foo())

        class Foo(object):
            def __eq__(self, other):
                return True
        Foo() |should| equal_to(Foo())

        value('abc') |should| equal_to('abC', case_sensitive=False)
        value('abc') |should_not| equal_to('cba')
    
    def test_be(self):
        value(1)    |should     | be(1)

        a = "some message"
        b = "some message"
        value(a)    |should     | be(b)

        c = "another message"
        d = c
        value(c)    |should     | be(d)

        value(1)    |should_not | be(1.1)

        value(2)    |should     | be(2)

    def test_include(self):
        value("should")         |should     | include("oul")
        value("should")         |should_not | include("could")

        value(['x', 'y', 'z'])  |should     | include('z')

        value([1,2,3]) |should| include(1)

        # value([1,2]) |should| include(3) # Should throw error

        value([1,2]) |should_not| include(3)

        # value('should') |should_not| include('oul') # Should throw error
    
    def test_contain(self):
        value([1,2,3])          |should     | contain(1)
        value([1,2,3])          |should_not | contain(7)

        value(['x', 'y', 'z'])  |should     | contain('z')

        value([1,2])            |should_not | contain(3)
        value('should')         |should     | contain('oul')
    
    def test_be_into(self):
        value(1)                |should     | be_into([1,2,3])
        value(5)                |should_not | be_into([1,2,3])
        value('a')              |should_not | be_into(['b', 'c'])

        value(1)                |should     | be_into(range(2))
        value(['a'])            |should_not | be_into(['a'])
        value(['a'])            |should     | be_into([['a']])
    
    def test_be_greater_than(self):
        value(1)    |should     | be_greater_than(0.9)

        # value(1) |should| be_greater_than(1) # Should throw error

        # value(1) |should| be_greater_than(2) # Should throw error

        value(1)    |should_not | be_greater_than(2)
        name = 'b'
        value(name) |should     | be_greater_than('a')

        # value(name) |should_not| be_greater_than('a') # Should throw error
        value(1)    |should_not | be_greater_than(1)


    def test_be_greater_than_or_equal_to(self):
        value(1)    |should     | be_greater_than_or_equal_to(0.9)
        value(1)    |should     | be_greater_than_or_equal_to(1)
        value(1)    |should_not | be_greater_than_or_equal_to(2)
        name = 'b'
        value(name) |should     | be_greater_than_or_equal_to('a')
        value(name) |should     | be_greater_than_or_equal_to('b')

        value(2)    |should     | be_greater_than_or_equal_to(2)
    
    def test_be_less_than_or_equal_to(self):
        value(0.9)  |should     | be_less_than_or_equal_to(1)
        value(1)    |should     | be_less_than_or_equal_to(1)
        value(2)    |should_not | be_less_than_or_equal_to(1)
        name = 'a'
        value(name) |should     | be_less_than_or_equal_to('b')
        value(name) |should     | be_less_than_or_equal_to('a')
        value(3000) |should     | be_less_than_or_equal_to(3001)
    
    def test_be_less_than(self):
        value(0.9)  |should     | be_less_than(1)
        value(2)    |should_not | be_less_than(2)
        value(2)    |should_not | be_less_than(1)
        name = 'a'
        value(name) |should     | be_less_than('b')
    
    def test_be_instance_of(self):
        class Foo(object):
            pass
        class Bar(object):
            pass
        
        foo = Foo()
        value(foo)  |should     | be_instance_of(Foo)
        value(foo)  |should_not | be_instance_of(Bar)
    
    def test_be_like(self):
        value('Hello World')        |should     | be_like(r"Hello W.+")
        value('Hello\nWorld')       |should     | be_like(r"Hello.+")
        value('123 is a number')    |should_not | be_like(r'^[12]+ is a number')
    
    def test_be_empty(self):
        value([])                   |should     |   be_empty
        # value([]) |should_not| be_empty # Should throw error
        value([1])                  |should_not |   be_empty
        # value([1]) |should| be_empty # Should throw error
        value(())                   |should     |   be_empty
        value((1,))                 |should_not |   be_empty
        # value(()) |should_not| be_empty # Should throw error
        # (1,) |should| be_empty # Should throw error
        value('')                   |should     |   be_empty
        value('a')                  |should_not |   be_empty
        value({})                   |should     |   be_empty
        value({'a': 1})             |should_not |   be_empty

        class MyCollection:
            def __init__(self, count):
                self.count = count
            def __len__(self):
                return self.count
        
        value(MyCollection(0))      |should     | be_empty
        value(MyCollection(1))      |should_not | be_empty

    def test_be_kind_of(self):
        class Foo(object):
            pass

        class Bar(object):
            pass

        foo = Foo()
        
        value(foo)  |should     | be_kind_of(Foo)
        # value(foo)  |should | be_kind_of(Bar) # Should throw error

        value(1) |should| be_kind_of(int)
        class Bar(Foo): pass
        value(Bar()) |should| be_kind_of(Foo)

    
    def test_be_thrown_by(self):
        def divide_one_by_zero():
            return 1 / 0
        
        def divide_x_by_y(x, y):
            return x / y
        
        value(ZeroDivisionError)    |should     | be_thrown_by(divide_one_by_zero)
        value(AttributeError)       |should_not | be_thrown_by((divide_x_by_y, 1, 0))

        # value(ZeroDivisionError) |should_not| be_thrown_by(divide_one_by_zero) # Should throw error
        value(ZeroDivisionError) |should| be_thrown_by((divide_x_by_y, 5, 0))

        # ZeroDivisionError |should| be_thrown_by([divide_x_by_y, 2, 1]) # Should throw error
        AttributeError |should_not| be_thrown_by((divide_x_by_y, 1, 0))
    
    def test_close_to(self):
        value(1)    |should     | close_to(0.9, delta=0.1)
        value(0.8)  |should     | close_to(0.9, delta=0.1)
        value(1)    |should_not | close_to(0.89, delta=0.1)
        value(4.9)  |should     | close_to(4, delta=0.9)
        # value(1)    |should     | close_to(0.89, delta=0.1) # Should throw error
        # value(0.91) |should_not| close_to(0.9, delta=0.01) # Should throw error
            
    def test_end_with(self):
        value('hello world')                            |should     | end_with('world')
        value('hello motto')                            |should_not | end_with('world')
        value("Brazil champion of 2010 FIFA world cup") |should     | end_with('world cup')
        value("hello world")                            |should_not | end_with('worlds')

        # value('hello motto') |should| end_with('world') # Should throw error

    def test_include_all_of(self):
        value([4, 5, 6, 7]) |should     | include_all_of([5, 6])
        value(['b', 'c'])   |should     | include_all_of(['b', 'c'])
        value(['b', 'c'])   |should_not | include_all_of(['b', 'c', 'a'])

        # value([1, 2, 3]) |should| include_all_of([3, 4]) # Should throw error

    def test_include_in_any_order(self):
        value([4, 5, 6, 7]) |should     | include_in_any_order([5, 6])
        value(['b', 'c'])   |should     | include_in_any_order(['b', 'c'])
        value(['b', 'c'])   |should_not | include_in_any_order(['b', 'c', 'a'])

        value([1, 2, 3]) |should| include_in_any_order([3, 1])

        # value([1, 2, 3]) |should| include_in_any_order([3, 4]) # Should throw error

        value([1, 2, 3]) |should| include_in_any_order((3, 1))

        # value([1, 2, 3]) |should| include_in_any_order((3, 4)) # Should throw error

        value('should') |should| include_in_any_order(('s', 'd', 'l'))

        # value('should') |should| include_in_any_order(('h', 'a')) # Should throw error
        value((1, 2, 3)) |should| include_in_any_order([2, 1])

    def test_include_any_of(self):
        value([1, 2, 3])    |should| include_any_of([3, 4, 5])
        value((1,))         |should| include_any_of([4, 6, 3, 1, 9, 7])
        value([1, 2, 3]) |should| include_any_of([1, 2])

        # value([1, 2, 3]) |should| include_any_of([4, 5]) # Should throw error

    def test_start_with(self):
        value("Brazil champion of 2010 FIFA world cup") |should     | start_with('Brazil champion')
        value("hello world")                            |should_not | start_with('Hello')

        value('Hello world') |should| start_with('Hello')

        # value('Hello world') |should| start_with('Hola') # Should throw error
    
    def test_include_keys(self):
        value({'a': 1, 'b': 2, 'c': 3}) |should     | include_keys()
        value({'a': 1, 'b': 2, 'c': 3}) |should_not | include_keys()
        value({})                       |should     | include_keys()
        value({})                       |should_not | include_keys()
        value({})                       |should_not | include_keys('d')
        value({'a': 1, 'b': 2, 'c': 3}) |should     | include_keys('a', 'b')
        value({'a': 1, 'b': 2, 'c': 3}) |should_not | include_keys('d')
        # value({'a': 1, 'b': 2, 'c': 3}) |should     | include_keys('c', 'd')              # Should throw error
        # value({'a': 1, 'b': 2, 'c': 3}) |should_not | include_keys('c', 'd')              # Should throw error
        # value({'a': 1, 'b': 2, 'c': 3}) |should_not | include_keys('d', 'b', 'a')         # Should throw error
        # value({'a': 1, 'b': 2, 'c': 3}) |should_not | include_keys('c', 'd', 'b', 'a')    # Should throw error

        value({'a': 1, 'b': 2, 'c': 3}) |should| include_keys('a')
        value({'a': 1, 'b': 2, 'c': 3}) |should| include_keys('a', 'c')
        value({'a': 1, 'b': 2, 'c': 3}) |should| include_keys('a', 'c', 'b')
        # value({'a': 1, 'b': 2, 'c': 3}) |should| include_keys('a', 'd') # Should throw error
        # value({'a': 1, 'b': 2, 'c': 3}) |should| include_keys('a', 'd', 'e') # Should throw error
        # value({'a': 1, 'b': 2, 'c': 3}) |should| include_keys('f', 'a', 'd', 'e') # Should throw error

        value({'a': 1, 'b': 2, 'c': 3}) |should_not| include_keys('d', 'e')

        # value({'a': 1, 'b': 2, 'c': 3}) |should_not| include_keys('a', 'b', 'd') # Should throw error
        # value({'a': 1, 'b': 2, 'c': 3}) |should_not| include_keys('c', 'd') # Should throw error

        # value(['a', 'b', 'c']) |should| include_keys('a', 'b', 'c') # Should throw error

    def test_include_values(self):
        {'a': 1, 'b': 2, 'c': 3} |should| include_values(1)
        {'a': 1, 'b': 2, 'c': 3} |should| include_values(1, 3)
        {'a': 1, 'b': 2, 'c': 3} |should| include_values(1, 2, 3)
        # {'a': 1, 'b': 2, 'c': 3} |should| include_values(1, 4)            # Should throw error
        # {'a': 1, 'b': 2, 'c': 3} |should| include_values(1, 4, 5)         # Should throw error
        # {'a': 1, 'b': 2, 'c': 3} |should| include_values(6, 1, 4, 5)      # Should throw error
        {'a': 1, 'b': 2, 'c': 3} |should_not| include_values(4, 5)
        # {'a': 1, 'b': 2, 'c': 3} |should_not| include_values(1, 2, 4)     # Should throw error
        # {'a': 1, 'b': 2, 'c': 3} |should_not| include_values(3, 4)        # Should throw error
        # ['a', 'b', 'c'] |should| include_values('does not matter')        # Should throw type error
        {'a': 1, 'b': 2, 'c': 3} |should| include_values(2, 3)
        {'a': 1, 'b': 2, 'c': 3} |should_not| include_values(0, 4)
    
    def test_respond_to(self):
        value('some string') |should| respond_to('startswith')

        class Foo:
            def __init__(self):
                self.foobar = 10
            def bar(self): pass
        
        Foo() |should| respond_to('foobar')
        Foo() |should| respond_to('bar')

        class Foo(object):
            def bar(self):
                pass
            def _internal_bar(self):
                pass
            def __name_clashing_bar(self):
                pass

        f = Foo()

        value(f) |should| respond_to('bar')
        # f |should_not| respond_to('bar')          # Should throw error
        # f |should| respond_to('unexisting_bar')   # Should throw error
        value(f) |should| respond_to('_internal_bar')
        value(f) |should| respond_to('__name_clashing_bar')
    
    def test_have_same_attribute_values_as(self):
        class Foo(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b

        a = Foo(1,2)
        b = Foo(1,2)

        a |should| have_same_attribute_values_as(b)

        c = Foo(1,3)

        # a |should| have_same_attribute_values_as(c)       # Should throw error
        # a |should_not| have_same_attribute_values_as(b)   # Should throw error

        a.c = 3
        b.c = 3

        a |should| have_same_attribute_values_as(b)

        del a.c
        a |should_not| have_same_attribute_values_as(b)



    
    def test_throw(self):
        value(ZeroDivisionError) |should| be_thrown_by(lambda: 1/0)
        value((lambda: 1/0.000001)) |should_not| throw(ZeroDivisionError)

        def foo():
            raise TypeError("Hey, it's cool!")
        
        value(foo) |should      | throw(TypeError, message="Hey, it's cool!")
        # value(foo) |should      | throw(TypeError, message="This won't work...") # Should throw error
        
        def divide(x, y): return x / y
        value((lambda: divide(1, 0))) |should| throw(ZeroDivisionError)
        value((divide, 1, 0)) |should| throw(ZeroDivisionError)

        def divide_one_by_zero():
            return 1 / 0

        def divide_x_by_y(x, y):
            return x / y

        value(divide_one_by_zero) |should| throw(ZeroDivisionError)

        # value(divide_one_by_zero) |should_not| throw(ZeroDivisionError) # Should throw error

        value((divide_x_by_y, 5, 0)) |should| throw(ZeroDivisionError)

        # value([divide_x_by_y, 2, 1]) |should| throw(ZeroDivisionError) # Should throw error

        value((divide_x_by_y, 1, 0)) |should_not| throw(AttributeError)

        class Foo(Exception): pass
        def raise_foo(message):
            raise Foo(message)

        value((raise_foo, 'cool! it works!')) |should| throw(Foo, message='cool! it works!')
        value((raise_foo, 'cool! it works! ble')) |should| throw(Foo('cool! it works! ble'))

        # value((lambda: raise_foo('what a pro!'))) |should| throw(Foo, message='cool! it works!') # Should throw error

        # value((lambda: raise_foo('what a pro!'))) |should| throw(Foo('cool! it works! ble')) # Should throw error

        # value((lambda: raise_foo('who?'))) |should_not| throw(Foo, message='who?') # Should throw error

        value((lambda: raise_foo('who?'))) |should_not| throw(Foo, message='what?')

        value((raise_foo, 'what a pro!')) |should| throw(Foo, message_regex=r'what a .+!')
        value((raise_foo, 'what a jerk!')) |should| throw(Foo, message_regex=r'what a .+!')
        value((raise_foo, 'what a pro?')) |should_not| throw(Foo, message_regex=r'what a .+!')
        value((raise_foo, 'what da hell!')) |should_not| throw(Foo, message_regex=r'what a .+!')

        # value((raise_foo, 'what a pro!')) |should| throw(Foo, message_regex="what a .+ yeah") # Should throw error
        
        # value((raise_foo, 'what a pro!')) |should_not| throw(Foo, message_regex=r'what a .+!') # Should throw error
    
    def test_have(self):
        value(['b', 'c', 'd']) |should| have(3).elements
        value([1, [1, 2, 3], 'a', lambda: 1, 2**3])                 |should| have(5).heterogeneous_things
        value(['asesino', 'japanische kampfhoerspiele', 'facada'])  |should| have(3).grindcore_bands
        value("left")                                               |should| have(4).characters

        class Foo:
            def __init__(self):
                self.inner_things = ['a', 'b', 'c']
            def pieces(self):
                return range(10)
        Foo() |should| have(3).inner_things
        Foo() |should| have(10).pieces

        class Field:
            def __init__(self, number_of_players):
                self.players = range(number_of_players)

        class SoccerGame:
            def __init__(self):
                self.field = Field(22)

        SoccerGame() |should| have(22).players_on_field

        ['a', 'b', 'c'] |should| have(3).elements
        value("abcdef") |should| have(6).characters
        # ['a', 'b', 'c'] |should_not| have(3).things               # Should throw error
        # value("abcde") |should| have(6).alphabetical_characters   # Should throw error
        (1, 2, 3) |should_not| have(2).numbers

        class Game(object):
            def __init__(self, number_of_players):
                self.field = Field(number_of_players)

        Game(10) |should| have(10).players_on_field
        Game(10) |should_not| have(11).players_on_field
        # Game(10) |should| have(11).players_on_field               # Should throw error
        # Game(10) |should_not| have(10).players_on_field           # Should throw error

        class Field(object):
            def __init__(self, number_of_players):
                self._players = range(number_of_players)
                self.goals = 2
            def players(self):
                return self._players
            def ball(self):
                return 0

        class Game(object):
            def __init__(self, number_of_players):
                self._field = Field(number_of_players)
            def field(self):
                return self._field
        
        Game(10) |should| have(10).players_on_field
        Game(10) |should_not| have(11).players_on_field
        # Game(10) |should| have(11).players_on_field               # Should throw error
        # Game(10) |should_not| have(10).players_on_field           # Should throw error
        # Game(10) |should_not| have(1).ball_on_field               # Should throw error
        # Game(10) |should_not| have(1).goals_on_field              # Should throw error

        class Car(object):
            def __init__(self, wheels):
                self.wheels = wheels
            def wild_wheels(self):
                return self.wheels
            def broken_wheels(self):
                return len(self.wheels)
        
        Car([1, 2, 3, 4]) |should| have(4).wheels
        # Car ([1, 2, 3]) |should| have(4).wheels
        Car([1, 2, 3, 4]) |should_not| have(5).wheels
        # Car ([1, 2]) |should_not| have(2).wheels
        # Car([1, 2, 3, 4]) |should| have(4).legs
        # 2 |should| have(1).things
        # Car(42) |should| have(42).wheels
        Car([1, 2, 3, 4]) |should| have(4).wild_wheels
        # Car([1, 2, 3, 4]) |should| have(4).broken_wheels
        {'a': 1, 'b': 2, 'c': 3} |should| have(3).keys
        {'a': 1, 'b': 2, 'c': 3} |should| have(3).values


    def test_change(self):
        class Box(object):
            def __init__(self):
                self.items = []
            def add_items(self, *items):
                for item in items:
                    self.items.append(item)
            def item_count(self):
                return len(self.items)
            def clear(self):
                self.items = []

        box = Box()
        box.add_items(5, 4, 3)
        box.clear |should| change(box.item_count)
        box.clear |should_not| change(box.item_count)

        (lambda: box.add_items(1, 2, 3)) |should| change(box.item_count)
        (box.add_items, 1, 2, 3) |should| change(box.item_count)

        box.clear()
        box.add_items(1, 2, 3)
        box.clear |should| change(box.item_count).by(-3)
        # box.add_items(1, 2, 3)
        # box.clear |should| change(box.item_count).by(-2)                          # Should throw error
        (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(3)
        # (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(2)    # Should throw error
        (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(3)
        # (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(4)   # Should throw error
        box.clear()
        (box.add_items, 1, 2, 3) |should| change(box.item_count).from_(0).to(3)
        box.clear |should| change(box.item_count).to(0)
        # box.clear |should| change(box.item_count).to(0)                           # Should throw error
        # (box.add_items, 1) |should| change(box.items)                             # Should throw error
        (lambda: box.add_items(1)) |should| change(box.item_count)
        # (lambda: box.add_items(1)) |should_not| change(box.item_count)            # Should throw error
        # (lambda: 0) |should| change(box.item_count)                               # Should throw error
        (lambda: 0) |should_not| change(box.item_count)
        (box.add_items, 1) |should| change(box.item_count)
        # (box.add_items, 1) |should| change(box.items)                             # Should throw error
        # (1, box.add_items) |should| change(box.item_count)                        # Should throw error
        (lambda: box.add_items(1)) |should| change(box.item_count).by(1)
        # (lambda: box.add_items(1)) |should| change(box.item_count).by(2)          # Should throw error
        (lambda: 1) |should| change(box.item_count).by(0)
        box.clear()
        box.add_items('a')
        box.clear |should| change(box.item_count).by(-1)
        (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(3)
        (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(2)
        # (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(4)   # Should throw error
        (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(3)
        (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(4)
        # (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(2)    # Should throw error
        box.clear()
        (box.add_items, 3, 5, 7) |should| change(box.item_count).from_(0).to(3)
        box.clear |should| change(box.item_count).from_(3).to(0)
        # (box.add_items, 3, 5, 7) |should| change(box.item_count).from_(0).to(2)   # Should throw error
        # box.add_items(3, 5, 7)
        # box.clear |should_not| change(box.item_count).from_(3).to(0)              # Should throw error
        box.add_items(1)
        box.clear |should| change(box.item_count).to(0)
        (box.add_items, 3, 4) |should_not| change(box.item_count).to(3)
        # box.clear |should_not| change(box.item_count).to(0)                       # Should throw error
        # box.clear |should| change(box.item_count).to(1)                           # Should throw error
        box.clear()
        # box.clear |should| change(box.item_count).to(0)                           # Should throw error
        box.clear |should_not| change(box.item_count).to(0)
        box.clear()
        box.add_items('a', 'b')
        # box.clear |should| change(box.item_count).from_(1).to(0)                  # Should throw error

        class ClientRepository(object):
            def __init__(self):
                self._clients = []
            def insert(self, client_name):
                self._clients.append(client_name)
            def clients(self):
                return self._clients

        client_repository = ClientRepository()
        (client_repository.insert, 'Paul') |should| change(client_repository.clients)
    
    def test_have_at_least(self):
        value(range(20)) |should| have_at_least(19).items
        value(range(20)) |should| have_at_least(20).items
        value(range(20)) |should_not| have_at_least(21).items

        value(['a', 'b', 'c']) |should| have_at_least(3).elements

        value("abcdef") |should| have_at_least(5).characters

        # value(['a', 'b', 'c']) |should_not| have_at_least(3).things # Should throw error

        # value("abcde") |should| have_at_least(6).alphabetical_characters # Should throw error

        value((1, 2, 3)) |should_not| have_at_least(4).numbers

        class Car(object):
            def __init__(self, *wheels):
                self.wheels = wheels
            def wild_wheels(self):
                return self.wheels

        my_car = Car(1, 2, 3, 4)
        value(my_car) |should| have_at_least(3).wheels

        value(my_car) |should| have_at_least(4).wheels

        # value(my_car) |should| have_at_least(5).wheels # Should throw error

        value(my_car) |should_not| have_at_least(5).wheels

        # value(my_car) |should_not| have_at_least(4).wheels # Should throw error

    def test_have_at_most(self):
        value(range(20)) |should_not| have_at_most(19).items
        value(range(20)) |should| have_at_most(20).items
        value(range(20)) |should| have_at_most(21).items

        value(['a', 'b', 'c']) |should| have_at_most(3).elements

        value("abcdef") |should| have_at_most(7).characters

        # value(['a', 'b', 'c']) |should_not| have_at_most(3).things # Should throw error

        # value("abcde") |should| have_at_most(4).alphabetical_characters # Should throw error

        value((1, 2, 3)) |should_not| have_at_most(2).numbers

        class Car(object):
            def __init__(self, *wheels):
                self.wheels = wheels
            def wild_wheels(self):
                return self.wheels

        my_car = Car(1, 2, 3, 4)
        value(my_car) |should| have_at_most(5).wheels

        value(my_car) |should| have_at_most(4).wheels

        # value(my_car) |should| have_at_most(3).wheels # Should throw error

        value(my_car) |should_not| have_at_most(3).wheels

        # value(my_car) |should_not| have_at_most(4).wheels # Should throw error


def run_tests():
    tests = CustomTests()
    tests.set_up()

    verbosity = False

    method_list = [attribute for attribute in dir(CustomTests) if utils.isfunction(getattr(CustomTests, attribute)) and not attribute.startswith('__') and attribute != "set_up"]
    
    n_tests = 0
    time_before = time.time()
    for m in method_list:
        getattr(tests, m)()
        if verbosity:
            print("{} () ... ok".format(m))
        else:
            print(".", end="")
        n_tests += 1
    time_after = time.time()
    
    print("\n----------------------------------------------------------------------")
    print("Ran {} tests in {}s".format(n_tests, round(time_after - time_before,3)))
