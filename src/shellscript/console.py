import code
import sys

from shellscript.settings import prompt_1, prompt_2


def interactive_output(obj):
    if isinstance(obj, shellscript.proto.Command):
        obj.interact()
    return None


def readfunc(prompt=''):
    if prompt == sys.ps2:
        prompt = prompt_2()
    else:
        prompt = prompt_1()
    return 'interactive_output(%s)' % input(prompt).strip()


if __name__ == '__main__':
    import shellscript
    local = shellscript.__dict__
    local['interactive_output'] = interactive_output
    code.interact(readfunc=readfunc, local=local)
