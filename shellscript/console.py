import code
import sys

from shellscript.settings import prompt_1, prompt_2, load


def readfunc(self, prompt=''):
    if prompt == sys.ps2:
        return input(prompt_2())
    else:
        return input(prompt_1())


if __name__ == '__main__':
    import shellscript
    local = shellscript.__dict__
    custom = load()
    if custom:
        local.update(custom.__dict__)
    code.interact(readfunc=readfunc, local=local)
