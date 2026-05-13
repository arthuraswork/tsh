from stdlib.stdvar import stdvar
from stdlib.strtools import tools
from stdlib.comporations import fl_condition, int_condition
from stdlib.toolslib import timeout, jsonl, fromtxt
from stdlib.math import calculations, unsafe
from stdlib.sound import say
libs = {
    'calculations!': calculations,
    'unsafe!': unsafe,
    'timeout!': timeout,
    'jsonl!': jsonl,
    'fromtxt!': fromtxt,
    'stdvar!': stdvar,
    'fc!': fl_condition,
    'ic!': int_condition,
    'say!': say

} | tools