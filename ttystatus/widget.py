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
      
    Widgets may have a static size, or their size may vary. The
    ``static_width`` property reveals this. This affects rendering:
    static sized widgets are rendered at their one static size; variable
    sized widgets are shrunk, if necessary, to make everything fit into
    the available space. If it's not possible to shrink enough, widgets
    are rendered from beginning until the space is full: variable sized
    widgets are rendered as small as possible in this case.

    '''
    
    static_width = True
    
    def __str__(self):
        raise NotImplementedError()
    
    def render(self, width):
        '''Format the current value.

        ``width`` is the available width for the widget. It need not use
        all of it. If it's not possible for the widget to render itself
        small enough to fit into the given width, it may return a larger
        string, but the caller will probably truncate it.
        
        This will be called only when the value actually needs to be
        formatted.
        
        '''
        
        return ''

    def update(self, terminal_status):
        '''React to changes in values stored in a TerminalStatus.'''

