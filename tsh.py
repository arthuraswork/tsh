from src.core import Core
import sys
if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        core = Core(args[1])
        core.run()
    else:
        raise Exception('Repl is not done')
