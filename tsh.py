from src.core import Core
import sys

def run():
    args = sys.argv
    try:
        if len(args) > 1:
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