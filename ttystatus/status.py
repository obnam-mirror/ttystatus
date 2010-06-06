# Copyright 2010  Lars Wirzenius
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
        
    def clear(self):
        '''Remove all widgets.'''
        self._widgets = []
        self._values = dict()
        self._m.clear()
        
    def __getitem__(self, key):
        '''Return value for key, or the empty string.'''
        return self._values.get(key, '')
        
    def __setitem__(self, key, value):
        '''Set value for key.'''
        self._values[key] = value
        for w in self._widgets:
            w.update(self, 999)
        self._m.write(''.join(str(w) for w in self._widgets))
    
    def increase(self, key, delta):
        '''Increase value for a key by a given amount.'''
        self[key] = (self[key] or 0) + delta
    
    def notify(self, msg):
        '''Show a message.'''
        self._m.notify(msg)
    
    def finish(self):
        '''Finish status display.'''
        self._m.finish()
