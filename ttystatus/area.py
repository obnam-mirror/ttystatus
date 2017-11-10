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


class AreaManager(object):

    '''Manage the area on the terminal for displaying messages.'''

    def __init__(self):
        self._terminal = None

    def set_terminal(self, terminal):
        self._terminal = terminal

    def get_max_line_length(self):
        width, _ = self._terminal.get_size()
        return width - 1

    def prepare_to_overwrite(self, displayed_message):
        '''Prepare to overwrite currently displayed message.

        This is like clear, but it only moves the cursor to the top of
        the message, but does not clear all the lines. This is helpful
        for avoiding flickering.

        The cursor is assumed to be on the last line of the displayed
        message.

        '''

        num_lines = len(displayed_message.split('\n'))
        up = self._terminal.get_up_sequence()
        cr = self._terminal.get_carriage_return_sequence()
        self._terminal.write(up * (num_lines - 1) + cr)

    def make_space(self, num_lines):
        '''Make space for a message needing a given number of lines.

        If the cursor is near the bottom of the terminal, scroll
        things up so that there's space. Otherwise, effectively
        nothing happens, except that the cursor is left at the last
        line reserved for the message.

        '''

        self._terminal.write('\n' * (num_lines - 1))

    def display(self, message):
        '''Display a message, which may be on multiple lines.

        The cursor is assumed to be at the last line of the message
        area. Long lines are chopped at terminal width - 1.

        '''

        max_chars = self.get_max_line_length()
        up = self._terminal.get_up_sequence()
        down = self._terminal.get_down_sequence()
        cr = self._terminal.get_carriage_return_sequence()
        erase = self._terminal.get_erase_line_sequence()
        lines = message.split('\n')

        parts = [up * (len(lines) - 1)]
        for i, line in enumerate(lines):
            if i > 0:
                parts.append(down)
            parts.append(cr)
            parts.append(line[:max_chars].encode())
            parts.append(erase)

        output = b''.join(parts)
        self._terminal.write(output)

    def clear_area(self, num_lines):
        '''Clear area reserved for message needing a given number of lines.

        The cursor is assumed to be at the last line of the message
        area and is left at the top.

        '''

        up = self._terminal.get_up_sequence()
        cr = self._terminal.get_carriage_return_sequence()
        erase = self._terminal.get_erase_line_sequence()
        self._terminal.write((cr + erase + up) * (num_lines - 1) + cr + erase)
