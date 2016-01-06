import code
import codeop
import sys

from shellscript.settings import prompt_1, prompt_2


def interactive_output(obj):
    if isinstance(obj, shellscript.proto.Command):
        obj.interact()
        return None
    else:
        return obj


class Read(object):

    def __init__(self):
        self.compile = codeop.CommandCompiler()

    def __call__(self, prompt=''):
        if prompt == sys.ps2:
            return input(prompt_2())
        else:
            line = input(prompt_1())
            modline = 'interactive_output(%s)' % line.strip()
            try:
                self.compile(modline)
                if '=' in line.split('(')[0]:
                    raise SyntaxError()
            except SyntaxError:
                return line
            else:
                return modline


if __name__ == '__main__':
    import shellscript
    local = shellscript.__dict__
    local['interactive_output'] = interactive_output
    code.interact(readfunc=Read(), local=local)
