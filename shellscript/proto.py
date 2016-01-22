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


class InputReaderMixin(object):
    """
    """

    def initialize_input(self, files):
        self._input_files = files
        self._active_input_file = None
        self._input_files_pos = -1

    @property
    def curr_input_file_name(self):
        if self.is_ipipe:
            return '<input>'
        else:
            return self._input_files[self._input_files_pos]

    @property
    def len_input_files(self):
        return len(self._input_files)

    @property
    def is_ready(self):
        mixinready = len(self._input_files) or self.is_ipipe
        return mixinready and super(self, InputReaderMixin).is_ready

    def get_input_line(self):
        if self.is_ipipe:
            return self._inp.get_line().strip('\n')

        if not self._active_input_file:
            self._input_files_pos += 1
            if self._input_files_pos >= len(self._input_files):
                raise StopIteration
            else:
                self._active_input_file = open(self._input_files[self._input_files_pos])
        try:
            return self._active_input_file.__next__().strip('\n')
        except StopIteration:
            self._active_input_file.close()
            self._active_input_file = None
            return self.get_input_line()


class OutputWriterMixin(object):

    class Writer(object):

        def __init__(self, obj):
            self._target = obj

        def close(self):
            pass


    class StreamWriter(Writer):

        @staticmethod
        def check(o):
            return o in (dev.out, dev.err)

        def __init__(self, obj):
            if obj == dev.out:
                self._target = sys.stdout
            elif obj == dev.err:
                self._target = sys.stderr

        def write(self, l):
            self._target.write('%s\n' % l)


    class FileWriter(Writer):

        @staticmethod
        def check(o):
            return hasattr(o, 'write') and hasattr(o, 'tell')

        def write(self, l):
            self._target.write('%s%s' % ( '\n' if self._target.tell() else '', 
                l ))


    class ListWriter(Writer):

        @staticmethod
        def check(o):
            return hasattr(o, 'append')

        def write(self, l):
            self._target.append(l)


    class FilenameWriter(FileWriter):

        @staticmethod
        def check(o):
            return isinstance(o, str)

        def __init__(self, fn):
            self._target = open(fn, 'w')

        def close(self):
            self._target.close()

    class NullWriter(Writer):

        @staticmethod
        def check(o):
            return o == dev.nul

        def write(self, l):
            pass


    def make_writer(self, obj, streamname):
        for c in (self.StreamWriter, self.FileWriter, self.ListWriter, 
                self.FilenameWriter, self.NullWriter):
            if c.check(obj):
                return c(obj)
        raise ProtocolError("'%s' is not a valid argument for %s" % (obj,
            streamname))


    def initialize(self):
        self._outwriter = self._errwriter = None
        if not self.is_epipe and not self.is_eiter:
            self._errwriter = self.make_writer(self._err, 'err')
        if not self.is_opipe and not self.is_oiter:
            self._outwriter = self.make_writer(self._out, 'out')

    def finalize(self):
        for w in (self._errwriter, self._outwriter):
            if w:
                w.close()

    def write_error(self, l):
        self._errwriter.write(l)

    def write_output(self, l):
        self._outwriter.write(l)


class Command(OutputWriterMixin):

    def __init__(self, out=None, err=None, outerr=None):
        if outerr is not None:
            self._out = self._err = outerr
        else:
            self._out = dev.out if out is None else out
            self._err = dev.err if err is None else err
        if self.is_opipe and self.is_epipe and self._out != self._err:
            raise ProtocolError('Invalid pipe: err pipe cannot differ from ' \
                    'out pipe.')
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
        super(Command, self).initialize()

    def finalize(self):
        super(Command, self).finalize()

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
    def is_epipe(self):
        """
        Checks if the error output of this *Command* is piped into another 
        *Command*.

        Return:
            bool: True if the error output of this *Command* is input for 
            another *Command*.
        """
        return isinstance(self._err, Command)

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
    def is_oiter(self):
        if self.is_opipe:
            return self._out.is_oiter
        else:
            return self._out == dev.itr

    @property
    def is_eiter(self):
            return self._err == dev.itr

    def get_line(self):
        ret = None
        while True:
            if self._buffer:
                ret = self._buffer.pop()
            elif self._stop:
                globals()['ret'] = self.ret
                self.finalize()
                raise StopIteration
            else:
                try:
                    ret = self.work() or OutString('')
                except StopIteration:
                    self._stop = True
                    continue
            if ret is None:
                continue
            elif isinstance(ret, ErrString) and not self.is_epipe \
                    and not self.is_eiter:
                self.write_error(ret)
            else:
                break
        return ret

    def interact_attempt(self):
        if not self.is_ready:
            return
        elif self.is_oiter or self.is_eiter:
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
        for l in self:
            if isinstance(l, OutString):
                self.write_output(l)
            elif isinstance(l, ErrString):
                self.write_error(l)
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
    elif hasattr(arg, '__next__'):
        arg = list(arg)
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
