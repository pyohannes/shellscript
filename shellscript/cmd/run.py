import os
import subprocess
import sys

from shellscript.proto import Command, OutString, ErrString, resolve, \
                              InputReaderMixin


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
        try:
            cmd = [ self._args['cmd'] ]
            for arg in self._args['args']:
                cmd.extend(resolve(arg))
            self._proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE)
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
        self._stdout_buf = []
        self._stderr_buf = []


    def finalize(self):
        super(run, self).finalize()
        try:
            self._proc.wait()
            self.ret = self._proc.returncode
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
                ret.append(''.join(buf[:index]))
                buf = buf[index+1:]
            except:
                break
        if finished:
            ret.append(''.join(buf))
            buf.clear()
        return ret

    def work(self):
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