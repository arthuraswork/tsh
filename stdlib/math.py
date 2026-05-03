ops = {
    '+': lambda a,b: a + b,
    '-': lambda a,b: a - b,
    '*': lambda a,b: a * b,
    '/': lambda a,b: a / b,

}

def calculations(line: str):
    line = line.replace('\n','')
    a, op, b = line[1:-1].split(',')
    return str(ops[op.strip()](int(a.strip()), int(b.strip())))
    
def unsafe(line: str):
    return str(eval(line[1:-1]))
