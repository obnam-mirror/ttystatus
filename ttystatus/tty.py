# Copyright 2010-2011,2015  Lars Wirzenius
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


class PhysicalTerminal(object):

    '''Handle interaction with the physical terminal.'''

    def __init__(self):
        self._terminal = None
        self._cuu = None
        self._cud = None
        self._cr = None
        self._el = None

    def open_tty(self):
        self._terminal = open('/dev/tty', 'wb')
        curses.setupterm(None, self._terminal.fileno())

        for name in ['cuu', 'cud']:
            s = curses.tigetstr(name)
            if s is not None:
                setattr(self, '_' + name, curses.tparm(s, 1))

        self._cr = curses.tigetstr('cr')
        self._el = curses.tigetstr('el')

    def has_capabilities(self):
        return (self._cuu is not None and
                self._cud is not None and
                self._cr is not None and
                self._el is not None)

    def get_up_sequence(self):
        assert self._cuu is not None
        return self._cuu

    def get_down_sequence(self):
        assert self._cud is not None
        return self._cud

    def get_carriage_return_sequence(self):
        assert self._cr is not None
        return self._cr

    def get_erase_line_sequence(self):
        assert self._el is not None
        return self._el

    def get_size(self):
        '''Return width, height of terminal in characters, rows.

        If this fails, assume 80 by 24.

        Borrowed and adapted from bzrlib.

        '''

        width = 80
        height = 24

        if self._terminal is not None:
            try:
                s = struct.pack('HHHH', 0, 0, 0, 0)
                x = fcntl.ioctl(
                    self._terminal.fileno(), termios.TIOCGWINSZ, s)
                height, width = struct.unpack('HHHH', x)[:2]
            except IOError:
                pass

        return width, height

    def write(self, raw_data):
        '''Write raw data to terminal.

        We ignore IOErrors for terminal output.

        '''

        if not isinstance(raw_data, bytes):
            raw_data = raw_data.encode()
        if self._terminal is not None:
            try:
                self._terminal.write(raw_data)
                self._terminal.flush()
            except IOError:
                pass
