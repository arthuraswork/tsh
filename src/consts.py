import questionary

INCLUDE_FUNCS = {
    'fork', 'dump', 'load'
}

FILE_EXT = {
    '.csv', '.jsonl'
}

STYLES = {
    "color": {
        "black": '\033[30m',
        "red": '\033[31m',
        "green": '\033[32m',
        "yellow": '\033[33m',
        "blue": '\033[34m',
        "magenta": '\033[35m',
        "cyan": '\033[36m',
        "gray": '\033[37m',
        "white": '\033[97m'
        
    },
    "style": {
        "reset": '\033[0m',
        "bold": '\033[01m',
        "dim": '\033[2m',
        "italic": '\033[3m',
        "underline": '\033[4m',
        "hidden": '\033[8m',
        "strike": '\033[9m'
    },
    "bg": {
        "black": '\033[40m',
        "red": '\033[41m',
        "green": '\033[42m',
        "yellow": '\033[43m',
        "blue": '\033[44m',
        "magenta": '\033[45m',
        "cyan": '\033[46m',
        "gray": '\033[47m',
        "white": '\033[107m'
    },
}

COMPFUNCS = {
    '==' : lambda a,b: a == b,
    '!=' : lambda a,b: a != b,
    'in' : lambda a,b: a in b,
    'starts' : lambda a,b: a.startswith(b),
    'ends' : lambda a,b: a.endswith(b),
}

QUESTIONS = {
    'Select': questionary.select,
    'Confirm': questionary.confirm,
    'Password': questionary.password,
    'Checkbox': questionary.checkbox,
    'Complete': questionary.autocomplete,
    'Path': questionary.path

}
