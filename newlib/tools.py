import time
import json
from newlib.define import Module

def write_text(line: str):
    path = line
    with open(path, 'r', encoding='utf-8') as f:
        text = f.readlines()
        return '\n'.join(text)

def sleep(seconds: str):
    seconds = seconds.replace('\n','')
    time.sleep(int(seconds))
    return ''

def jsonl(line: str):
    filepath, form = line.split(',')
    output = []
    with open(filepath, 'r',encoding='utf-8') as f:
        for l in f:
            data = json.loads(l)
            result = form.format(**data).replace('\\n','\n').replace('\\t','\t')
            output.append(result)
    return '\n'.join(output)

tools = Module('tools',{
    'jsonl': jsonl, 'sleep': sleep, 'write-text':write_text
})

