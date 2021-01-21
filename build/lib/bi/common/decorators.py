

from builtins import zip
def accepts(*types, **kwdtypes):
    """ Function decorator to enforce parameter data types
    :param types:   positional parameter types
    :param kwdtypes: keyword parameter types
    :return:
    """
    def check_accepts(f):
        num_pos_args = len(types)
        num_kwd_args =  len(list(kwdtypes.keys()))
        assert num_pos_args + num_kwd_args == f.__code__.co_argcount
        def new_f(*args, **kwds):
            # ensure positional arguments data types are valid
            for (a, t) in zip(args[0:len(types)], types):
                assert isinstance(a, t), "arg %r does not math %s" %(a,t)
            # ensure kwd arguments data types are valid
            for karg in list(kwds.keys()):
                assert isinstance(kwds.get(karg), kwdtypes.get(karg)), 'kwarg %r does not match %s' %(karg, kwdtypes.get(karg))
            return f(*args, **kwds)
        new_f.__name__ = f.__name__
        return new_f

    return check_accepts
