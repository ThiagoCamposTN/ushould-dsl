def isfunction(obj):
    '''
        Method based on the "inspect" micropython library.
        
        https://github.com/micropython/micropython-lib/blob/3a6ab0b46d6471bee00ae815444c624709dd4cdd/python-stdlib/inspect/inspect.py

        Parameters
        ----------
        first : object
            the object to be verified if it's a function.

        Returns
        -------
        bool
            return True if the object is a function or False if not.
    '''
    return isinstance(obj, type(isfunction))

def isclass(obj):
    '''
        Method based on the "inspect" micropython library.
        
        https://github.com/micropython/micropython-lib/blob/3a6ab0b46d6471bee00ae815444c624709dd4cdd/python-stdlib/inspect/inspect.py

        Parameters
        ----------
        first : object
            the object to be verified if it's a class.

        Returns
        -------
        bool
            return True if the object is a class or False if not.
    '''
    return isinstance(obj, type)

def is_empty(input_value):
    if input_value == '' or input_value == [] or input_value == () or input_value == {}:
        return True
    
    if hasattr(input_value, '__len__'):
        return len(input_value) == 0
    
    return False

def exception_type(input_value):
    try:
        input_value()
    except Exception as exception:
        return type(exception)
    
    return None

def keys_in_phrase(keys, name):
    keys = list(keys)
    if len(keys) == 0:
        return ""
    elif len(keys) == 1:
        return "{} '{}'".format(name, keys[-1])
    else:
        first_term = keys.pop(0)
        last_term = keys.pop(-1)
        middle_term = [", '{}'".format(x) for x in keys]

        result = "{}s '{}'{} and '{}'".format(name, first_term, "".join(middle_term), last_term)
        return result

def is_iterable(obj):
    '''
        Checks if an object can be iterable or not.

        Parameters
        ----------
        first : object
            the object to be verified if it's iterable.

        Returns
        -------
        bool
            return True if the object is a iterable or False if not.
    '''
    try:
        if iter(obj):
            return True
    except:
        pass
    return False
