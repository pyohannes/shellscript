import os
import subprocess
import sys

from shellscript.proto import Command, OutString, ErrString, resolve, \
                              InputReaderMixin, dev


class run(Command, InputReaderMixin):
    """Run an executable.

    ret is set to the return value of the executable or 1 if none is found.

    Parameters:
        str cmd: The name or path of the external command.
        *args: The arguments for the command.

    Yields:
        shellscript.proto.OutString: The output of the executable.
    """
    def __init__(self, cmd=None, *args, **kwargs):
        self._args = dict(
                cmd=cmd,
                args=args)
        super(run, self).__init__(**kwargs)

    def initialize(self):
        super(run, self).initialize()
        self.initialize_input([])
        self._terminal_use = (self._out == dev.out and self._err == dev.err)
        try:
            cmdlist = [ self._args['cmd'] ]
            for arg in self._args['args']:
                cmdlist.extend(resolve(arg))
            if self._terminal_use:
                self._initialize_terminal(cmdlist)
            else:
                self._initialize_redirection(cmdlist)
        except:
            self.stop_with_error(sys.exc_info()[1], 1)

    def _initialize_terminal(self, cmdlist):
        self._proc = subprocess.Popen(cmdlist)

    def _initialize_redirection(self, cmdlist):
        self._proc = subprocess.Popen(
                cmdlist,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
        self._stdout_buf = []
        self._stderr_buf = []

    def finalize(self):
        super(run, self).finalize()
        try:
            self._proc.wait()
            self.ret = self._proc.returncode
            if not self._terminal_use:
                self._proc.stdout.close()
                self._proc.stderr.close()
                self._proc.stdin.close()
        except: pass

    def _query_stream(self, stream, buf, finished=False):
        if not stream.closed:
            while True:
                r = stream.read(128)
                if r:
                    buf.extend(r.decode('utf-8'))
                else:
                    break
        ret = []
        while True:
            try:
                index = buf.index('\n')
                ret.append(OutString(''.join(buf[:index]), True))
                buf[:] = buf[index+1:]
            except:
                break
        if finished:
            ret.append(OutString(''.join(buf), False))
            buf.clear()
        return ret

    def work(self):
        if self._terminal_use:
            _, __ = self._proc.communicate()
            self.ret = self._proc.returncode
            self.stop()
        stdin_active = True
        try:
            while True:
                finished = self._proc.poll() is not None
                # read from stdout and stderr
                for l in self._query_stream(
                        self._proc.stdout, self._stdout_buf, finished):
                    self.buffer_return(OutString(l))
                for l in self._query_stream(
                        self._proc.stderr, self._stderr_buf, finished):
                    self.buffer_return(ErrString(l))
                # write to stdin
                if finished:
                    self.ret = self._proc.returncode
                    self.stop()
                elif stdin_active:
                    try:
                        line = self.get_input_line()
                        self._proc.stdin.write( ('%s\n' % line).encode('utf-8')
                                )
                    except StopIteration:
                        stdin_active = False
        except StopIteration:
            raise
        except:
            self.ret = 1
            return ErrString(sys.exc_info()[1])
