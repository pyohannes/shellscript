import os
import shutil
import sys

from shellscript.proto import Command, OutString, ErrString, resolve


class cp(Command):
    """Copy *src* to *dst*.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        src: The source file or source directory, or a list of those.
        dst: The destination file or directory name, or a list of those.
        bool recurse: Copy src recursively.
        bool verbose: Print verbose output.
        str preserve: Preserve the specified attributes (default:
        "mode,timestamps").
        bool p: The same as preserve="mode,timestamps"

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """

    def __init__(self, src=None, dst=None, recurse=False, verbose=False,
            preserve=None, p=False, *args, **kwargs):
        self._src = src
        self._dst = dst
        self._recurse = recurse
        self._verbose = verbose
        if p:
            self._preserve = ('timestamps', 'mode')
        elif preserve is not None:
            self._preserve = preserve.split(',')
        else:
            self._preserve = []
        super(cp, self).__init__(*args, **kwargs)

    def initialize(self):
        super(cp, self).initialize()
        self._srclist = resolve(self._src)
        self._dstlist = resolve(self._dst)
        self._get_umask()
        if not self._srclist:
            self.stop_with_error('No source given.', 1)
        if not self._dstlist:
            self.stop_with_error('No destination given.', 1)

    def _get_umask(self):
        self._umask = os.umask(0)
        os.umask(self._umask)
        self._umask = 0o777 - self._umask # make it compatibel to os.chmod

    def _verbose_output(self, src, dst):
        self.buffer_return(OutString("`%s' -> `%s'" % (src, dst)))

    def _apply_preserve(self, src, dst):
        if 'mode' in self._preserve:
            shutil.copymode(src, dst)
        else:
            os.chmod(dst, self._umask)
        if 'timestamps' in self._preserve:
            if hasattr(os, 'utime'):
                st = os.stat(src)
                os.utime(dst, (st.st_atime, st.st_mtime))

    def _copy_dir(self, src, dst):
        if os.path.exists(dst):
            dst = os.path.join(dst, os.path.basename(src))
        if self._verbose:
            self._verbose_output(src, dst)
        os.makedirs(dst)
        for entry in os.listdir(src):
            entry_full = os.path.join(src, entry)
            if os.path.isdir(entry_full):
                self._copy_dir(entry_full, dst)
            else:
                self._copy_file(entry_full, os.path.join(dst, entry))
        self._apply_preserve(src, dst)

    def _copy_file(self, src, dst):
        if self._verbose:
            self._verbose_output(src, dst)
        shutil.copyfile(src, dst)
        self._apply_preserve(src, dst)

    def work(self):
        for src in self._srclist:
            for dst in self._dstlist:
                try:
                    if os.path.isdir(src):
                        if not self._recurse:
                            self.buffer_return(ErrString(
                                '%s is a directory' % src))
                            self.ret = 1
                        elif os.path.isfile(dst):
                            self.buffer_return(ErrString(
                                '%s is a file' % dst))
                            self.ret = 1
                        else:
                            self._copy_dir(src, dst)
                    elif os.path.isfile(src):
                        dstfile = dst
                        if os.path.isdir(dst):
                            dstfile = os.path.join(dst, os.path.basename(src))
                        self._copy_file(src, dstfile)
                    else:
                        self.buffer_return(ErrString(
                            'No such file or directory: %s' % src))
                        self.ret = 1
                except:
                    self.buffer_return(ErrString(sys.exc_info()[1]))
                    self.ret = 1
        self.stop()
