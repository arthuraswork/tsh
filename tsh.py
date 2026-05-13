from src.core import Core
import sys

def run():
    args = sys.argv
    try:
        if len(args) > 2:
            if len(args) > 3:
                core = Core(args[2], args[3:])
            else:
                core = Core(args[1])
            result = core.run()
            if result == 1:
                return run()
        else:
            raise Exception('For REPL use ./tsh repl')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()