import os
import sys
import glob
import string

import shellscript.settings as settings


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


class _BaseString(str):
    def __new__(cls, s, linebreak=None, *args, **kwargs):
        obj = str.__new__(cls, s, *args, **kwargs)
        if isinstance(s, _BaseString) and linebreak is None:
            obj.linebreak = s.linebreak
        elif linebreak is None:
            obj.linebreak = True
        else:
            obj.linebreak = bool(linebreak)
        return obj

    def to_py_str(self):
        return '%s%s' % (self, '\n' if self.linebreak else '')


class OutString(_BaseString):
    """
    A line of normal output yielded by a command instance. This corresponds
    to a line of stdout.
    """
    pass


class ErrString(_BaseString):
    """
    A line of error output yielded by a command instance. This corresponds
    to a line of stderr.
    """
    pass


class InputReaderMixin(object):
    """
    """
    def initialize_input(self, files, file_change_callback=None):
        self._input_files = files
        self._active_input_file = None
        self._input_files_pos = -1
        self._file_change_cb = file_change_callback or (lambda fname: None)

    @property
    def curr_input_file_name(self):
        if self.is_ipipe:
            return '<input>'
        else:
            return self._input_files[self._input_files_pos]

    @property
    def len_input_files(self):
        return len(self._input_files)

    def _is_ready_for_interaction(self):
        try:
            if self._wait_for_input:
                return len(self._input_files) or self.is_ipipe
            else:
                return True
        except AttributeError:
            return False

    def get_input_line(self):
        if self.is_ipipe:
            return self._inp.get_line()

        if not self.len_input_files and sys.stdin.isatty():
            l = sys.stdin.readline()
            return OutString(l.strip('\n'), l.endswith('\n'))

        if not self._active_input_file:
            self._input_files_pos += 1
            if self._input_files_pos >= len(self._input_files):
                raise StopIteration
            else:
                fname = self._input_files[self._input_files_pos]
                self._active_input_file = open(fname)
                self._file_change_cb(fname)
        try:
            l = self._active_input_file.__next__()
            return OutString(l.strip('\n'), l.endswith('\n'))
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

        def write(self, l):
            self._target.write(l.to_py_str())


    class StreamWriter(Writer):

        @staticmethod
        def check(o):
            return o in (dev.out, dev.err)

        def __init__(self, obj):
            if obj == dev.out:
                self._target = sys.stdout
            elif obj == dev.err:
                self._target = sys.stderr


    class FileWriter(Writer):

        @staticmethod
        def check(o):
            return hasattr(o, 'write') and hasattr(o, 'tell')


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


def pipe(cmd, *args, **kwargs):
    if not kwargs:
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs = args[0]
            args = []
        elif len(args) == 2 and isinstance(args[0], list) \
                and isinstance(args[1], dict):
            kwargs = args[1]
            args = args[0]
    return cmd(*args, _wait_for_input=True, **kwargs)


class Command(OutputWriterMixin):

    def __init__(self, out=None, err=None, outerr=None, _wait_for_input=False):
        if outerr is not None:
            self._out = self._err = outerr
        else:
            self._out = settings.default_out if out is None else out
            self._err = settings.default_err if err is None else err
        if isinstance(self._out, tuple):
            if self._out == self._err:
                self._out = self._err = pipe(*self._out)
            else:
                self._out = pipe(*self._out)
        if isinstance(self._err, tuple):
            self._err = pipe(*self._err)
        if self.is_opipe and self.is_epipe and self._out != self._err:
            raise ProtocolError('Invalid pipe: err pipe cannot differ from ' \
                    'out pipe.')
        for stream in (self._out, self._err):
            if isinstance(stream, Command) and not stream._wait_for_input:
                raise ProtocolError('Invalid pipe: must not be an ' \
                        'initialized Command.')
        self._wait_for_input = _wait_for_input
        if self.is_opipe:
            self._out._inp = self
        self.ret = None
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
        r = '<%s return=%s ' % (self.__class__.__name__, str(self.ret))
        if self.is_opipe:
            r += repr(self._out)
        r += '>'
        return r

    def __str__(self):
        return '\n'.join(list(self))

    # for derived classes

    def initialize(self):
        self.ret = 0
        self._buffer = []
        self._stop = False
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

    def buffer_pop(self):
        if self._buffer:
            return self._buffer.pop()
        else:
            return None

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
        return all([ 
            cls._is_ready_for_interaction(self) \
            for cls in type(self).mro() \
            if hasattr(cls, '_is_ready_for_interaction') ])

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
        while True:
            ret = self.buffer_pop()
            if ret is None:
                if self._stop:
                    globals()['ret'] = self.ret
                    self.finalize()
                    raise StopIteration
                else:
                    try:
                        ret = self.work()
                        #if ret is None:
                        #    ret = OutString('', True)
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
        try:
            self.initialize()
            if self.is_opipe:
                self._out.initialize()
        except StopIteration:
            try:
                self.stop()
            except StopIteration: pass

    def _interact(self):
        # avoid calling __iter__ - this would cause an call to initialize again
        while True:
            try:
                l = self.__next__()
                if isinstance(l, OutString):
                    self.write_output(l)
                elif isinstance(l, ErrString):
                    self.write_error(l)
                else:
                    raise ProtocolError(
                            "Not an OutString or ErrString: '%s'" % l)
            except StopIteration:
                break


def resolve(arg):
    if isinstance(arg, str):
        arg = string.Template(arg).safe_substitute(os.environ)
        if glob.has_magic(arg):
           arg = glob.glob(arg)
           arg.sort()
        else:
            arg = [ arg ]
    else:
        try:
            exp = []
            for a in arg:
                exp.extend(resolve(a))
            arg = exp
        except TypeError: pass
    return arg
