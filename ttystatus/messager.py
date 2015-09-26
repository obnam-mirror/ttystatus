# Copyright 2010, 2011  Lars Wirzenius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import curses
import fcntl
import struct
import termios
import time


class Messager(object):

    '''Write messages to the terminal.'''

    def __init__(self, output=None, period=None, open_tty=None,
                 fake_width=False):
        self._enabled = True
        if output:
            self.output = output
        else:
            try:
                self.output = (open_tty or self._open_tty)()
            except IOError:
                self.output = None
        self._period = 1.0 if period is None else period
        self._last_time = 0    # When did we write last?
        self._cached_msg = ''  # Last message from user, to write() method.
        self._first_output = True  # is our next output the first one?
        self._fake_width = fake_width
        self.set_width(self._get_terminal_width())  # Width of terminal

    def _open_tty(self):  # pragma: no cover
        f = open('/dev/tty', 'wb')
        curses.setupterm(None, f.fileno())
        return f

    def set_width(self, actual_width):
        self.width = actual_width - 1

    def _now(self):
        '''Return current time.'''
        # This is a wrapper around time.time(), for testing.
        return time.time()

    def _get_terminal_width(self):  # pragma: no cover
        '''Return width of terminal in characters.

        If this fails, assume 80.

        Borrowed and adapted from bzrlib.

        '''

        width = 80
        if self._fake_width:
            if hasattr(self, 'width'):
                width = self.width
        elif self.output is not None:
            # StringIO might not have fileno. We use StringIO for tests.
            fileno = getattr(self.output, 'fileno', None)
            if fileno is not None:
                try:
                    s = struct.pack('HHHH', 0, 0, 0, 0)
                    x = fcntl.ioctl(fileno(), termios.TIOCGWINSZ, s)
                    width = struct.unpack('HHHH', x)[1]
                except IOError:
                    pass
        return width

    def update_width(self):  # pragma: no cover
        self.set_width(self._get_terminal_width())

    def _raw_write(self, string):
        '''Write raw data if output is terminal.'''

        if self._enabled and self.output and self.output.isatty():
            try:
                self.output.write(string)
                self.output.flush()
            except IOError:  # pragma: no cover
                self._enabled = False

    def time_to_write(self):
        '''Is it time to write now?'''
        return self._now() - self._last_time >= self._period

    def write(self, string):
        '''Write raw data, always.'''
        self.update_width()
        rows = string.split('\n')

        raw_parts = []

        if self._first_output:
            raw_parts.append('\n' * (len(rows) - 1))
            self._first_output = False

        if rows:
            up = curses.tparm(curses.tigetstr('cuu'), 1)
            down = curses.tparm(curses.tigetstr('cud'), 1)
            cr = curses.tigetstr('cr')
            el = curses.tigetstr('el')

            raw_parts.extend([
                up * (len(rows) - 1),
                cr,
                el,
                rows[0][:self.width],
            ])
            for row in rows[1:]:
                raw_parts.extend([
                    down,
                    cr,
                    el,
                    row[:self.width],
                ])

        raw = ''.join(raw_parts)
        self._raw_write(raw)
        self._cached_msg = string
        self._last_time = self._now()

    def clear(self):
        '''Remove current message from terminal.'''

        if self._first_output:
            return

        rows = self._cached_msg.split('\n')

        raw_parts = []

        if rows:
            up = curses.tparm(curses.tigetstr('cuu'), 1)
            down = curses.tparm(curses.tigetstr('cud'), 1)
            cr = curses.tigetstr('cr')
            el = curses.tigetstr('el')

            raw_parts.extend([
                up * (len(rows) - 1),
                cr,
                el,
            ])
            for row in rows[1:]:
                raw_parts.extend([
                    down,
                    cr,
                    el,
                ])
            raw_parts.extend([
                up * (len(rows) - 1),
            ])

        raw = ''.join(raw_parts)
        self._raw_write(raw)

    def notify(self, string, f, force=False):
        '''Show a notification message string to the user.

        Notifications are meant for error messages and other things
        that do not belong in, say, progress bars. Whatever is currently
        on the terminal is wiped, then the notification message is shown,
        a new line is started, and the old message is restored.

        Notifications are written even when the output is not going
        to a terminal.

        '''

        if self._enabled or force:
            self.clear()
            try:
                f.write('%s\n' % string)
                f.flush()
            except IOError:
                # We ignore these. No point in crashing if terminal is bad.
                pass
            self._first_output = True
            self.write(self._cached_msg)

    def finish(self):
        '''Finalize output.'''
        if self._cached_msg:
            self.write(self._cached_msg)
            self._raw_write('\n')

    def disable(self):
        '''Disable all output.'''
        self._enabled = False

    def enable(self):
        '''Enable output to happen.'''
        self._enabled = True
