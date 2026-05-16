import os
from stdlib.define import Module

def say(line: str):
    os.system(f'spd-say "{line}"')
    return ''

sounds = Module('sounds',{'say':say})
