from newlib.define import Module


def is_safe(expr: str):
    symbs = {'*','+','-','/','//','%','**', ' ', ')','(','.'}
    for i in expr:
        if i in symbs or i.isdigit():
            ...
        else:
            return False
    
    return True

def safe_eval(line: str):
    if is_safe(line):
        return eval(line)
    else:
        raise Exception('Unsafe operation')

tsh_math = Module('math',{
    'safe':safe_eval
})