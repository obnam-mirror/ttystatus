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

    def open_tty(self):
        self._terminal = open('/dev/tty', 'wb')
        curses.setupterm(None, self._terminal.fileno())

    def get_up_sequence(self):
        return curses.tparm(curses.tigetstr('cuu'), 1)

    def get_down_sequence(self):
        return curses.tparm(curses.tigetstr('cud'), 1)

    def get_erase_line_sequence(self):
        cr = curses.tigetstr('cr')
        el = curses.tigetstr('el')
        return cr + el

    def get_width(self):
        '''Return width of terminal in characters.

        If this fails, assume 80.

        Borrowed and adapted from bzrlib.

        '''

        width = 80

        try:
            s = struct.pack('HHHH', 0, 0, 0, 0)
            x = fcntl.ioctl(self._terminal.fileno(), termios.TIOCGWINSZ, s)
            width = struct.unpack('HHHH', x)[1]
        except IOError:
            pass

        return width

    def write(self, raw_data):
        '''Write raw data to terminal.

        We ignore IOErrors for terminal output.

        '''

        try:
            self._terminal.write(raw_data)
            self._terminal.flush()
        except IOError:
            pass
