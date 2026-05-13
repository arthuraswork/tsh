import sys
import readline
import subprocess
import json
import datetime
import os
from src.draw import animations
from src.consts import *
from src.new_module_system import modules

def execution(line:str):
    if '/bin/bash' in line:
        sh_cmd = line.split('/bin/bash')[-1]
        return subprocess.run(sh_cmd.strip(), shell=True, text=True).stdout
    if '/python-unsafe' in line:
        py_cmd = line.split('/python-unsafe')[-1]
        exec(py_cmd.strip())
    if '/python3' in line:
        py_file = line.split('/python3')[-1]
        return subprocess.run(f'python3 {py_file}', shell=True, text=True).stdout

def var_define(line: str):
    words = line.split(maxsplit=1)
    name = words[0].split(':')[-1]
    value = words[1].replace('\n','')
    return name, value

def new_including_sys(line: str):
    importing_name = line.split('<')[-1].split('>')[0].strip()
    if '::' not in importing_name:
        raise Exception('Uncorrect including form, use <module::function>')
    else:
        module, funcname = importing_name.split('::',1)
        if module in modules.modules:
            if funcname in modules.modules[module]:
                return funcname, modules.modules[module][funcname]
            raise Exception(f'Unknown function {funcname}')    
        raise Exception(f'Unknown module, {module}')
        

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

def byte_format(line: str):
    if r"\n" in line:
        line = line.replace(r"\n",'\n')
    if r"\t" in line:
        line = line.replace(r"\t",'\t')
    return line
def styling_func(line: str):
    for style_type in STYLES:
        if f'[{style_type}:' in line:
            for style in STYLES[style_type]:
                if f'[{style_type}:{style}]' in line:
                    line = line.replace(f'[{style_type}:{style}]', STYLES[style_type][style])
    return byte_format(line)

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
        
def line_former(template: str, path: str, line: str):
    if '.csv' in path:
        args = line.split(',')
        i = 0
        len_args = len(args)
        while '_' in template and i != len_args:
            template = template.replace('_', args[i],1)
            i += 1
        return template
    else:
        return line 


def conditions(line: str):
    expr = line.split('(')[1].split(')')[0]
    for func in COMPFUNCS:
        if func in expr:
            a,b = expr.split(func)
            a = a.strip()
            b = b.strip()
            return COMPFUNCS[func](a,b)
    raise Exception('Unknown operator')

def path_extract(line):
    path = line.split('(')[-1].split(')')[0]
    info = True if '-i' in line else False
    args = line.split('{')[-1].split('}')[0].split(',')
    if os.path.exists(path): 
        return path, info, args 
    raise f'fork() exception, {path} not found'

class Core:
    def __init__(self, path = None, *args):

        if path:
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
            if args: 
                for i, arg in enumerate(args[0]): 
                    self.locals[f'${i}'] = arg
        else:
            self.name: str = 'repl'
            self.lines: str = []
            self.dtime: str = datetime.datetime.now().isoformat()
            self.path = './'
            self.locals: dict = dict()
            self.funcs: dict = dict()
            print('REPL mod for tsh:')

    def repl_mod(self):
        while True:
            try:
                user_input = input('->')
                self.execution_func(user_input)
                sys.stdout.write('\n')
            except Exception as e:
                print(e)

    def interpolation(self, line: str):
        for name in self.locals:
            if name in line:
                id = line.index(name)
                if line[id-1] != '/':
                    value = self.locals[name]
                    if len(value) < len(name):
                        value += ' ' * (len(name) - len(value))
                    line = line.replace(name, value)

        return line

    def funcman(self, line: str):
        if '?set:' in line:
            funcpart = line.split(' ',1)[-1]
        else:
            funcpart = line
        funcname = funcpart.split('(')[0]
        func = self.funcs.get(funcname)
        if func:
            args = funcpart.split('(')[-1].split(')')[0]
            if args:
                result = str(func(args))
                return line.replace(funcpart, result if '\n' in line else result)
            else:
                result = str(func())
                return line.replace(funcpart, result + '\n' if '\n' in line else result)
        raise Exception(f'Unknown function {funcname}')
             


    def execution_func(self, line: str, write_line = True):
        if line.startswith('rerun!'):
            return 'rerun'
        if line.startswith('exit('):
            exit(code=line.split('exit(')[-1].split(')')[0])
        if line.startswith('//'):
            return 'comment'
        if line.startswith('exists?') and '>>' in line:
            _, varname, _, write_to = line.split()
            if varname in self.locals:
                self.locals[write_to] = 'True'
            else:
                self.locals[write_to] = 'False'
            return 'existing checking'

        if '//' in line:
            line = line.split('//')[0]
        if self.locals:
            line = self.interpolation(line)
        if self.funcs:
            if '!' in line and '(' in line and ')' in line:
                line = self.funcman(line)

        if any(True for func in INCLUDE_FUNCS if func in line):
            result = self.controls_and_memory()
            if result == 'fork':
                return result
        
        if line.startswith('<') and '>' in line:
            line = self.template_funcs(line)

        if line.startswith('#'):
            return self.sharpfuncs(line)
            
        if line.startswith('?'):
            return self.questfuncs(line, write_line)
        if write_line:
            return self.console_out(styling_func(line))
        return line
    
    def template_funcs(self, line):
        template = line.split('<')[-1].split('>')[0]
        path,_,_ = path_extract(line.split('(')[-1].split(')')[0])
        line = ''
        with open(path, 'r', encoding='utf-8') as f:
            for l in  f.readlines():
                formated_template = line_former(template, path, l) 
                line += formated_template

        return line

    @staticmethod
    def console_out(line: str):
        if '--noprint' in line:
            return 'noprint'
        if '--nolb' in line:
            line = line.replace('\n','').replace('--nolb','')
        sys.stdout.write(line)
        return line
    
    def controls_and_memory(self, line):
        if line.startswith('fork'):
            path, info, args = path_extract(line)
            if path:
                if info: 
                    sys.stdout.write(f'{self.path} -> {path}\n')
                self.fork(path, args)
                if info:
                    sys.stdout.write(f'{path} -> {self.path}\n')
                return 'fork'
            else:
                raise Exception(f'File {path} not found')
            
        if line.startswith('dump'):
            dump(line, self.locals)
            
        if line.startswith('load'):
            extra = load(line)
            self.locals = self.locals | extra

    def sharpfuncs(self, line):
        if line.startswith('#!'):
            line = execution(line)
            if not line: return
        if line.startswith('#include'):
            funcname, result = new_including_sys(line)
            self.funlcs[funcname] = result
        return 'sharp'

    def questfuncs(self, line: str, write_line):
        if line.startswith('?draw'):
            animations(line)

        if line.startswith('?set:'):
            name, value = var_define(line)
            value = self.execution_func(value, False)
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
                return self.execution_func(line.split('->')[-1].split('||')[0].strip(), write_line)
            else:
                if '||' in line:
                    return self.execution_func(line.split('||')[-1].strip(), write_line)
    def fork(self, path, args=None):
        new = Core(path)
        if args:
            new.locals = new.locals | {f'${i}': v.strip() for i, v in enumerate(args)}
        new.run()

    def run(self, index=0):
        events = []
        for line in self.lines[index:]:
            event = self.execution_func(line)
            events.append(event)
            if event == 'rerun':     
                return 1
        sys.stdout.write('\n')
        return events