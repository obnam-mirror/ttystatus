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
        self._widgets.append(widget)

    def format(self, format_string):
        '''Add new widgets based on format string.
        
        The format string is taken literally, except that ``%%`` is a
        literal percent character, and ``%Foo(a,b,c)`` is a widget
        of type ``Foo`` with parameters a, b, and c. For example:
        ``format("hello, %String(name)")``.
        
        '''
        for widget in ttystatus.fmt.parse(format_string):
            self.add(widget)
        
    def clear(self):
        '''Remove all widgets.'''
        self._widgets = []
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
        for w in self._widgets:
            w.update(self)
        if self._m.time_to_write():
            self._render()

    def _render(self):
        '''Format and output all widgets.'''
        self._m.write(''.join(w.render() for w in self._widgets))
    
    def increase(self, key, delta):
        '''Increase value for a key by a given amount.'''
        self[key] = (self[key] or 0) + delta
    
    def notify(self, msg):
        '''Show a message.'''
        self._m.notify(msg, sys.stdout)

    def error(self, msg):
        '''Write an error message.'''
        self._m.notify(msg, sys.stderr)
    
    def finish(self):
        '''Finish status display.'''
        self._render()
        self._m.finish()
        
    def disable(self):
        '''Disable all output.'''
        self._m.disable()
        
    def enable(self):
        '''Enable output if it has been disabled.'''
        self._m.enable()

