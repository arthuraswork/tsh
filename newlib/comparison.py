from newlib.define import Module

comps = {
    '>': lambda a,b: '1' if a > b else '0',
    '>=': lambda a,b: '1' if a >= b else '0',
    '<': lambda a,b: '1' if a < b else '0',
    '<=': lambda a,b: '1' if a <= b else '0',
}

def float_comporation(args: str):
    """
    floatc(3.14 > 19)!
    """
    a, op, b = args.split()
    op_func = comps.get(op)
    if op_func:
        return op_func(float(a), float(b))
    raise Exception('Error on float comporation')

def int_comporations(args: str):
    """
    intc(3 > 19)!
    """
    a, op, b = args.split()
    op_func = comps.get(op)
    if op_func:
        return op_func(int(a), int(b))
    raise Exception('Error on int comporation')


comparison = Module('comporations', {'floatc':float_comporation, 'intc':int_comporations})