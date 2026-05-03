import sys
import readline
import subprocess
import json
import os
from src.external import animations
from src.consts import *
import src.modules as modules

def execution(line:str):
    if '/bin/bash' in line:
        sh_cmd = line.split('/bin/bash')[-1]
        return subprocess.run(sh_cmd.strip(), shell=True, text=True).stdout
    if '/python-unsafe' in line:
        py_cmd = line.split('/python-unsafe')[-1]
        exec(py_cmd.strip())

def var_define(line: str):
    words = line.split(maxsplit=1)
    name = words[0].split(':')[-1]
    value = words[1].replace('\n','')
    return name, value

def include(line: str):
    func = line.split('<')[-1].split('>')[0].strip()
    if func in modules.libs:
        result = modules.libs[func]
        if isinstance(result, dict):
            return result
        else:
            return {func:result}
    raise Exception('Unknown module')


def questoins_func(line: str):
    for question in QUESTIONS:
        choices, message = None, None
        if question in line:
            if '(' in line and ')' in line:
                message = line.split('(')[-1].split(')')[0]
            if '{' in line and '}' in line:
                choices = line.split('{')[-1].split('}')[0].split(',')
            if message and not choices:
                q = QUESTIONS[question](message=message)
            elif message and choices:  
                q = QUESTIONS[question](message=message, choices=choices)
            else:
                raise Exception('Question exception')
            result = q.ask()
            if question == 'Checkbox':
                return ''.join(result)
            return str(result)
    else:
        return input('>>>')

def styling_func(line: str):
    for style_type in STYLES:
        if f'[{style_type}:' in line:
            for style in STYLES[style_type]:
                if f'[{style_type}:{style}]' in line:
                    line = line.replace(f'[{style_type}:{style}]', STYLES[style_type][style])
    return line

def dump(line: str, vars: dict):
    path = line.split('(')[-1].split(')')[0]
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(vars,f)

def load(line: str):
    path = line.split('(')[-1].split(')')[0]
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

def conditions(line: str):
    args = line.split('(')[1].split(')')[0].split()
    for op in COMPFUNCS:
        if op == args[1]:
            return COMPFUNCS[op](args[0],args[2])
    return False

def path_extract(line):
    path = line.split('(')[-1].split(')')[0]
    info = True if '-i' in line else False
    if os.path.exists(path): 
        return path, info
    return '', info    

class Core:
    def __init__(self, path, args = None):
        if not args:
            try:
                with open(path, 'r') as f:
                    file = f.readlines()
                    meta = file[0].split(':')
                    self.name: str = meta[0]
                    self.lines: str = file[1:]
                    self.dtime: str = meta[1]
                    self.path = path
                    self.locals: dict = dict()
                    self.funcs: dict = dict()
            except FileNotFoundError:
                raise FileExistsError()
        else:
            self.lines = args['lines']
        

    def interpolation(self, line: str):
        for name in self.locals:
            if name in line:
                line = line.replace(name, self.locals[name])
        return line

    def funcman(self, line: str):
        words = line.split()
        if len(words) == 1:
            func_in_text = words[0]
            funcname = func_in_text.split('!')[0] + '!'
            args = func_in_text.split('!',1)[-1]
            func = self.funcs.get(funcname)
            if func:
                return func(args)
        else:
            for i, word in enumerate(words):
                if '!' in word:
                    funcname = word.split('!')[0] + '!'
                    if '(' in word and ')' not in word:
                        for w in words[i+1:]:
                            word += f' {w}'
                            if ')' in w:
                                break
                    args = word.split('!',1)[-1]
                    func = self.funcs.get(funcname)
                    if func:
                        return line.replace(word, func(args))
        return line

    def execution_func(self, line: str):
        if line.startswith('//'):
            return
        if '//' in line:
            line = line.split('//')[0]

        if self.locals:
            line = self.interpolation(line)

        if self.funcs:
            if '!' in line:
                line = self.funcman(line)

        if line.startswith('fork'):
            path, info = path_extract(line)
            if path:
                if info: 
                    sys.stdout.write(f'{self.path} -> {path}\n')
                self.fork(path)
                if info:
                    sys.stdout.write(f'{path} -> {self.path}\n')
                return
            else:
                raise Exception(f'File {path} not found')
        if line.startswith('dump'):
            dump(line, self.locals)
            
        if line.startswith('load'):
            extra = load(line)
            self.locals = self.locals | extra

        if line.startswith('#'):
            return self.sharpfuncs(line)
            
        if line.startswith('?'):
            return self.questfuncs(line)

        self.console_out(line)
    
    def console_out(line: str):
        sys.stdout.write(styling_func(line))

    def sharpfuncs(self, line):
        if line.startswith('#!'):
            line = execution(line)
            if not line: return
        if line.startswith('#include'):
            result = include(line)
            self.funcs = self.funcs | result

    def questfuncs(self, line: str):
        if line.startswith('?draw'):
            animations(line)
        if line.startswith('?set:'):
            name, value = var_define(line)
            self.locals[name] = value
        if line.startswith('?:'):
            if '>>' in line:
                name   = line.split('>>')[1].strip()
                result = questoins_func(line)
                self.locals[name] = result
            else:
                sys.stdout.write(questoins_func(line) + '\n')
        if line.startswith('?('):
            if conditions(line):
                self.execution_func(line.split('->')[-1].split('||')[0].strip())
            else:
                self.execution_func(line.split('||')[-1].strip())
    def fork(self, path):
        new = Core(path)
        new.run()

    def run(self, index=0):

        for line in self.lines[index:]:
            self.execution_func(line)     
        sys.stdout.write('\n')