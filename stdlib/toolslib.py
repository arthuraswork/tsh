import time
import json
ops = {
    '+': lambda a,b: a + b,
    '-': lambda a,b: a - b,
    '*': lambda a,b: a * b,
    '/': lambda a,b: a / b,

}

def fromtxt(line: str):
    path = line[1:-1]
    with open(path, 'r', encoding='utf-8') as f:
        text = f.readlines()
        return '\n'.join(text)

def timeout(seconds: str):
    seconds = seconds.replace('\n','').replace(')','').replace('(','')
    time.sleep(int(seconds))
    return ''

def jsonl(line: str):
    filepath, form = line[1:-1].split(',')
    output = []
    with open(filepath, 'r',encoding='utf-8') as f:
        for l in f:
            data = json.loads(l)
            result = form.format(**data).replace('\\n','\n').replace('\\t','\t')
            output.append(result)
    return '\n'.join(output)