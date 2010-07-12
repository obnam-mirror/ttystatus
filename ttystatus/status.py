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
        if widget.interesting_keys is None:
            self._wildcards += [widget]
        else:
            for key in widget.interesting_keys:
                self._interests[key] = self._interests.get(key, []) + [widget]
        
    def clear(self):
        '''Remove all widgets.'''
        self._widgets = []
        self._values = dict()
        self._interests = dict()
        self._wildcards = list()
        self._latest_width = None
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
        width = self._m.width
        if width != self._latest_width:
            widgets = self._widgets
            self._latest_width = width
        else:
            widgets = self._interests.get(key, []) + self._wildcards
        for w in widgets:
            w.update(self, width)
            width -= len(str(w))
        if self._m.time_to_write():
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
