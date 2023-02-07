def call_func(module, func_name, args):
    try:
        function = getattr(module, func_name)
        if callable(function):
            return function(**args) if type(args) is dict else function(args)
        else:
            return function
    except AttributeError as e:
        print(e)
    return None

def create_object(vars,string:str, args=None):
    o = vars[string] #globals() object
    if args:
        instance = o(**args) if type(args) is dict else o(args)
    else:
        instance = o()
    
    return instance
