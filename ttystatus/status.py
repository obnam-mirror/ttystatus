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


import sys

import ttystatus


class TerminalStatus(object):

    '''Show status and progress information on a terminal.

    All output is provided via widgets of various kinds. Many widgets
    format data that TerminalStatus stores. TerminalStatus provides a
    dict interface for setting and retrieving data items. Unlike a real
    dict, getting a value for a key that has not been set does not
    result in a KeyError exception, but in the empty string being
    returned.

    '''

    def __init__(self, output=None, period=None, messager=None):
        self._m = messager or ttystatus.Messager(output=output, period=period)
        self.clear()

    def add(self, widget):
        '''Add a new widget to the status display.'''
        self._widget_rows[-1].append(widget)

    def start_new_line(self):
        '''Start a new line of widgets.'''
        self._widget_rows.append([])

    def format(self, format_string):
        '''Add new widgets based on format string.

        The format string is taken literally, except that ``%%`` is a
        literal percent character, and ``%Foo(a,b,c)`` is a widget
        of type ``Foo`` with parameters a, b, and c. For example:
        ``format("hello, %String(name)")``.

        '''

        for i, line in enumerate(format_string.split('\n')):
            if i > 0:
                self.start_new_line()
            for widget in ttystatus.parse(line):
                self.add(widget)

    def clear(self):
        '''Remove all widgets.'''
        self._widget_rows = [[]]
        self._values = dict()
        self._m.clear()

    def __getitem__(self, key):
        '''Return value for key, or the empty string.'''
        return self._values.get(key, '')

    def get(self, key, default=None):
        '''Like dict.get.'''
        return self._values.get(key, default)

    def __setitem__(self, key, value):
        '''Set value for key.'''
        self._values[key] = value
        for row in self._widget_rows:
            for w in row:
                w.update(self)
        if self._m.time_to_write():
            self._write()

    def flush(self):
        '''Force an update of current state to the screen.

        This happens even if it is not yet time to output the screen.

        '''

        self._write()

    def _render(self):
        '''Render current state of all widgets.'''

        return '\n'.join(self._render_row(row) for row in self._widget_rows)

    def _render_row(self, widget_row):
        remaining = self._m.width

        texts = [None] * len(widget_row)

        for i, w in enumerate(widget_row):
            if w.static_width:
                texts[i] = w.render(0)
                remaining -= len(texts[i])

        for i, w in enumerate(widget_row):
            if not w.static_width:
                texts[i] = w.render(remaining)
                remaining -= len(texts[i])

        return (''.join(texts))[:self._m.width]

    def _write(self):
        '''Render and output current state of all widgets.'''
        self._m.write(self._render())

    def increase(self, key, delta):
        '''Increase value for a key by a given amount.'''
        self[key] = (self[key] or 0) + delta

    def notify(self, msg):
        '''Show a message.'''
        self._m.notify(msg, sys.stdout)

    def error(self, msg):
        '''Write an error message.'''
        self._m.notify(msg, sys.stderr, force=True)

    def finish(self):
        '''Finish status display.'''
        self._write()
        self._m.finish()

    def disable(self):
        '''Disable all output.'''
        self._m.disable()

    def enable(self):
        '''Enable output if it has been disabled.'''
        self._m.enable()
