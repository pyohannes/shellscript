import code
import sys

from shellscript.settings import prompt_1, prompt_2


def readfunc(prompt=''):
    if prompt == sys.ps2:
        prompt = prompt_2()
    else:
        prompt = prompt_1()
    return input(prompt)


if __name__ == '__main__':
    import shellscript
    code.interact(readfunc=readfunc, local=shellscript.__dict__)
