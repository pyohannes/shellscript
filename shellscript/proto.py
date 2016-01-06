import os
import sys
import glob
import string


class ProtocolError(Exception):
    pass


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
        self._buffer = []
        self._stop = False

    def stop_with_error(self, msg, ret):
        self.ret = ret
        self._buffer.append(ErrString(msg))
        return self.stop()

    def stop(self):
        self._stop = True
        raise StopIteration

    def __iter__(self):
        return self

    def __next__(self):
        if self._buffer:
            ret = self._buffer[0]
            del self._buffer[0]
            return ret
        if self._stop:
            #shellscript.settings.set_lastreturn(self._returncode)
            raise StopIteration
        try:
            return self.generator_step() or OutString('')
        except StopIteration:
            self._stop = True
            return self.__next__()

    def interact(self):
        for l in self:
            if isinstance(l, OutString):
                sys.stdout.write('%s\n' % l)
            elif isinstance(l, ErrString):
                sys.stderr.write('%s\n' % l)
            else:
                raise ProtocolError("Not an OutString or ErrString: '%s'" % l)


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
