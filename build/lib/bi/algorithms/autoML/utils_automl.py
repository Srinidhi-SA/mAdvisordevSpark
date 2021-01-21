def drop_cols_from_list(val, *args):
    result = []
    for arg in args:
        if val in arg:
            arg.remove(val)
        result.append(arg)
    return tuple(result)
