def Template(line:str):
    line = line[1:-1]
    template, *values = line.split(',')
    for v in values:
        template = template.replace('<>',v,1)
    return template + '\n'

def Replace(line: str):
    line = line[1:-1]
    string, old, new = line.split('`')
    return string.replace(old, new)

tools = {
    'upper!': lambda l: l[1:-1].upper(),
    'lower!': lambda l: l[1:-1].lower(),
    'capitalize!': lambda l: l[1:-1].capitalize(),
    'reversed!': lambda l:  ''.join(list(reversed(l[1:-1]))),
    'isdigit!': lambda l: '1' if l[1:-1].isdigit() else '0',
    'sizeof!': lambda l: str(len(l[1:-1])),
    'T!': Template,
    'R!': Replace,

}

