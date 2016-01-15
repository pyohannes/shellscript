import os
import sys
import glob
import string


class ProtocolError(Exception):
    pass


class dev(object):
    """
    Enumerator that can be used to redirect the output of *Command* objects.
    The enumerator values can be passed to the *out*, *err* and *outerr* 
    arguments.

    Attributes:
        out: Redirection to *stdout*.
        err: Redirection to *stderr*.
        itr: Output can be retrieved by iterating over the *Command* object.
        nul: The output is discarded.
    """

    out = 1
    err = 2
    itr = 3
    nul = 4


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

    def __init__(self, out=None, err=None, outerr=None):
        if outerr is not None:
            self._out = self._err = outerr
        else:
            self._out = dev.out if out is None else out
            self._err = dev.err if err is None else err
        if self.is_opipe:
            self._out._inp = self
        self._global_initialize()
        self.interact_attempt()

    def __iter__(self):
        self._global_initialize()
        return self

    def __next__(self):
        if self.is_opipe:
            return self._out.__next__()
        else:
            return self.get_line()

    def __repr__(self):
        return ''

    # for derived classes

    def initialize(self):
        pass

    def work(self):
        pass

    def stop_with_error(self, msg, ret):
        self.ret = ret
        self.buffer_return(ErrString(msg))
        return self.stop()

    def stop(self):
        self._stop = True
        raise StopIteration

    def buffer_return(self, value):
        self._buffer.insert(0, value)

    # for interaction amongst commands

    @property
    def is_opipe(self):
        """
        Checks if the output of this *Command* is piped into another *Command*.

        Return:
            bool: True if the output of this *Command* is input for another
            *Command*.
        """
        return isinstance(self._out, Command)

    @property
    def is_ipipe(self):
        """
        Checks if the input of this *Command* is piped from another *Command*.

        Return:
            bool: True if the input of this *Command* is piped from another
            *Command*.
        """
        try:
            return isinstance(self._inp, Command)
        except:
            return False

    @property
    def is_ready(self):
        return True

    @property
    def is_iter(self):
        if self.is_opipe:
            return self._out.is_iter
        else:
            return dev.itr in (self._out, self._err)

    def get_line(self):
        if self._buffer:
            ret = self._buffer[0]
            del self._buffer[0]
            return ret
        if self._stop:
            #shellscript.settings.set_lastreturn(self._returncode)
            raise StopIteration
        try:
            return self.work() or OutString('')
        except StopIteration:
            self._stop = True
            return self.get_line()

    def interact_attempt(self):
        if not self.is_ready:
            return
        elif self.is_iter:
            return
        elif self.is_opipe and self._out.is_ready:
            self._out.interact_attempt()
        else:
            self._interact()

    # for internal usage

    def _global_initialize(self):
        self.ret = 0
        self._buffer = []
        self._stop = False
        try:
            self.initialize()
        except StopIteration:
            try:
                self.stop()
            except StopIteration: pass

    def _interact(self):
        def make_writer(target):
            if target == dev.out:
                return lambda s: sys.stdout.write('%s\n' % s)
            elif target == dev.err:
                return lambda s: sys.stderr.write('%s\n' % s)
            elif hasattr(target, 'write') and hasattr(target, 'tell'):
                return lambda s: target.write('%s%s' % (
                    '\n' if target.tell() else '', s))
            elif hasattr(target, 'append'):
                return lambda s: target.append(s)
            else:
                return lambda s: None
        outwriter = make_writer(self._out)
        errwriter = make_writer(self._err)
        for l in self:
            if isinstance(l, OutString):
                outwriter(l)
            elif isinstance(l, ErrString):
                errwriter(l)
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
#        return self.work()
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
