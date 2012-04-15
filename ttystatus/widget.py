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


class Widget(object):

    '''Base class for ttystatus widgets.
    
    Widgets display stuff on screen. The value may depend on data provided
    by the user (at creation time), or may be computed from one or more
    values in the TerminalStatus object to which the widget object belongs.
    
    There are two steps:
    
    * the widget `update` method is called by TerminalStatus whenever
      any of the values change
    * the widget `render` method is called by TerminalStatus when it is
      time to display things

    '''
    
    def __str__(self):
        raise NotImplementedError()
    
    def render(self):
        '''Format the current value.
        
        This will be called only when the value actually needs to be
        formatted.
        
        '''
        
        return ''

    def update(self, terminal_status):
        '''React to changes in values stored in a TerminalStatus.'''

