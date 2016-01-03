import os
import glob
import string

class OutString(str):
    """
    A line of normal output yielded by a command instance. This corresponds
    to a line of stdout.
    """
    pass


class ErrString(str):
    """
    A line of error output yielded by a command instance. This corresponds
    to a line of stderr.
    """
    pass


class Command(object):

    def __init__(self, inp=None):
        self._inp = inp
        self.ret = 0

    def set_error(self, err=1):
        self.ret = err

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.generator_step() or OutString('')
        except StopIteration:
            #shellscript.settings.set_lastreturn(self._returncode)
            raise

    def __repr__(self):
        return '\n'.join(self)


class OnceReturnCommand(Command):

    def __next__(self):
        if hasattr(self, '_step_done'):
            raise StopIteration()
        else:
            self._step_done = True
        return super(OnceReturnCommand, self).__next__()


def resolve(arg):
    if isinstance(arg, str):
        arg = string.Template(arg).safe_substitute(os.environ)
        if glob.has_magic(arg):
           arg = glob.glob(arg)
           arg.sort()
        else:
            arg = [ arg ]
    return arg




#import sys
#import string
#import os
#import glob
#
##import shellscript.settings
#
#
#class OnceReturnGenerator(Generator):
#
#    def next(self):
#        if hasattr(self, '_step_done'):
#            raise StopIteration()
#        else:
#            self._step_done = True
#        return self.generator_step()
#
#
#def resolve(arg):
#    if isinstance(arg, str):
#        arg = string.Template(arg).safe_substitute(os.environ)
#        if glob.has_magic(arg):
#            arg = glob.glob(arg)
#            arg.sort()
#        else:
#            arg = [ arg ]
#    return arg
#
#
#def resolveargs(f):
#    def _wrapper(*args, **kwargs):
#        args = [ _resolve_arg(a) for a in args ]
#        kwargs = dict([ (k, _resolve_arg(a)) for k, a in kwargs.items() ])
#        return f(*args, **kwargs)
#    return _wrapper
#
#
#def openfiles(files, *args, **kwargs):
#    if isinstance(files, str):
#        files = [ files ]
#    for f in files:
#        with open(f, *args, **kwargs) as fobj:
#            for line in fobj:
#                yield line
#
#
#def out(generator):
#    try:
#        return generator.out()
#    except AttributeError:
#        return []
