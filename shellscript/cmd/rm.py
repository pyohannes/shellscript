import os
import sys

from shellscript.proto import Command, OutString, ErrString, resolve


class rm(Command):
    """Remove files or directories.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        f: The file or directory to be removed, or a list of those.
        bool recurse: Remove directories and their contents recursively.
        bool verbose: Print verbose output.
        bool force: Ignore nonexistent files, never prompt.
        str interactive: Prompt according to: 'never', 'once', 'always'.
        Defaults to 'always' if stdin is a terminal and 'never' otherwise.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """

    def __init__(self, f=None, recurse=False, verbose=False, force=False,
            interactive=None, *args, **kwargs):
        self._f = f
        self._recurse = recurse
        self._verbose = verbose
        self._force = force
        self._tty = sys.stdin.isatty()
        if not interactive:
            if sys.stdin.isatty():
                self._interactive = 'always'
            else:
                self._interactive = 'never'
        else:
            self._interactive = interactive
        super(rm, self).__init__(*args, **kwargs)

    def initialize(self):
        super(rm, self).initialize()
        self._flist = resolve(self._f)
        if not self._flist:
            if self._force:
                self.stop()
            else:
                self.stop_with_error('No files given.', 1)

    def _verbose_output(self, fname, isdir=False):
        if isdir:
            self.buffer_return(OutString("removed directory: `%s'" % fname))
        else:
            self.buffer_return(OutString("removed `%s'" % fname))

    def _ask(self, question):
        sys.stdout.write(question)
        sys.stdout.flush()
        return sys.stdin.readline().strip() in ('y', 'yes')

    def _is_interactive_for(self, when):
        return self._interactive == when and not self._force

    def _remove_dir(self, d):
        if self._is_interactive_for('always'):
            if not self._ask("descend into directory `%s'? " % d):
                return
        for entry in os.listdir(d):
            entry_full = os.path.join(d, entry)
            if os.path.isdir(entry_full):
                self._remove_dir(d)
            else:
                self._remove_file(entry_full)
        os.rmdir(d)
        if self._verbose:
            self._verbose_output(d, True)

    def _remove_file(self, f):
        if self._is_interactive_for('always'):
            if not self._ask("remove regular file `%s'? " % f):
                return
        os.remove(f)
        if self._verbose:
            self._verbose_output(f)

    def work(self):
        if self._is_interactive_for('once'):
            if not self._ask("remove all arguments? "):
                self.stop()
        for f in self._flist:
            try:
                if os.path.isdir(f):
                    if not self._recurse:
                        self.buffer_return(ErrString('%s is a directory' % f))
                        self.ret = 1
                    else:
                        self._remove_dir(f)
                elif os.path.isfile(f):
                    self._remove_file(f)
                elif not self._force:
                    self.buffer_return(ErrString(
                        'No such file or directory: %s' % f))
                    self.ret = 1
            except:
                self.buffer_return(ErrString(sys.exc_info()[1]))
                self.ret = 1
        self.stop()
