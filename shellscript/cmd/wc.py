import sys
import time

from shellscript.proto import Command, InputReaderMixin, OutString, ErrString,\
                              resolve


class wc(Command, InputReaderMixin):
    """Print newline, word and byte counts for each file.

    ret is set to 0 on success and to 1 on failure.

    Parameters:
        f: The files, or a list of those.
        bool chars: Print the character counts.
        bool lines: Print the line counts.
        bool words: Print the word counts.
        bool max_line_length: Print the length of the longest line.

    Yields:
        shellscript.proto.OutString, shellscript.proto.ErrString:
    """
    def __init__(self, f=None, chars=None, lines=None, words=None,
            max_line_length=None,  *args, **kwargs):
        self._f = f
        if all(v is None for v in [ chars, lines, words, max_line_length ]):
            self._chars = self._lines = self._words = True
            self._max_line_length = False
        else:
            self._chars = chars
            self._lines = lines
            self._words = words
            self._max_line_length = max_line_length
        super(wc, self).__init__(*args, **kwargs)

    def initialize(self):
        super(wc, self).initialize()
        self.initialize_input(resolve(self._f) or [],
                file_change_callback=self._count_new_file)
        self._counts = []
        self._count_filename = None
        self._count_chars = self._count_words = self._count_lines \
            = self._count_max_line = 0
        self._count_total_chars = self._count_total_words \
            = self._count_total_lines = self._count_total_max_line = 0
        self._count_nr = 0

    def _count_new_file(self, fname):
        #import pdb
        #pdb.set_trace()
        if self._count_nr > 0:
            self._count_finish()
        self._count_nr += 1
        self._count_filename = fname

    def _count_finish(self):
        self._counts.append([ 
            self._count_chars, 
            self._count_words, 
            self._count_lines,
            self._count_max_line, 
            self._count_filename ])
        self._count_total_chars += self._count_chars
        self._count_total_words += self._count_words
        self._count_total_lines += self._count_lines
        self._count_total_max_line = max(self._count_total_max_line,
                self._count_max_line)
        self._count_chars = self._count_words = self._count_lines \
            = self._count_max_line = 0
        self._count_filename = None

    def _make_total(self):
        self._counts.append([ 
            self._count_total_chars, 
            self._count_total_words, 
            self._count_total_lines,
            self._count_total_max_line, 
            'total'])

    def _get_return_line(self):
        r = []
        l = self._counts[0]
        del self._counts[0]
        if self._max_line_length:
            r.append('%8d' % l[3])
        if self._lines:
            r.append('%8d' % l[2])
        if self._words:
            r.append('%8d' % l[1])
        if self._chars:
            r.append('%8d' % l[0])
        if l[4]:
            r.append(' %s' % l[4])
        return ''.join(r)

    def work(self):
        try:
            l = self.get_input_line()
            self._count_lines += 1
            linelen = len(l)
            self._count_chars += linelen
            if l.linebreak:
                self._count_chars += 1
            self._count_words += len(l.split())
            self._count_max_line = max(self._count_max_line, linelen)
            if self._counts:
                return OutString(self._get_return_line(), True)
        except StopIteration:
            self._count_finish()
            if self.len_input_files > 1:
                self._make_total()
            while self._counts:
                self.buffer_return(OutString(self._get_return_line(), True))
            raise
        except:
            self.stop_with_error(sys.exc_info()[1], 1)
