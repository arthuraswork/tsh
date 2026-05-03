comps = {
    '>': lambda a,b: '1' if a > b else '0',
    '>=': lambda a,b: '1' if a >= b else '0',
    '<': lambda a,b: '1' if a < b else '0',
    '<=': lambda a,b: '1' if a <= b else '0',
}

def fl_condition(args: str):
    """
    fc!(3.14 > 19)
    """
    a, op, b = args[1:-1].split()
    op_func = comps.get(op)
    if op_func:
        return op_func(float(a), float(b))
    raise Exception('Error on float comporation')

def int_condition(args: str):
    """
    ic!(3 > 19)
    """
    a, op, b = args[1:-1].split()
    op_func = comps.get(op)
    if op_func:
        return op_func(int(a), int(b))
    raise Exception('Error on int comporation')