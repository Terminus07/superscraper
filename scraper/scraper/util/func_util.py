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
