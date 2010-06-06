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

    '''Show status and progress information on a terminal.'''
    
    def __init__(self):
        self.clear()
        
    def add(self, widget):
        '''Add a new widget to the status display.'''
        self._widgets.append(widget)
        
    def clear(self):
        '''Remove all widgets.'''
        self._widgets = []
