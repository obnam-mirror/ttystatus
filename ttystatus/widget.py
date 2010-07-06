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
    
    Widgets are responsible for formatting part of the output. They
    get a value or values either directly from the user, or from the
    master TerminalStatus widget. They return the formatted string
    via __str__.
    
    Widgets must have an attribute 'interesting_keys', listing the
    keys it is interested in, and 'value', for the formatted value.
    
    '''

    def __str__(self):
        '''Return current value to be displayed for this widget.'''
        return self.value

    def update(self, master, width):
        '''Update displayed value for widget, from values in master.
        
        'width' gives the width for which the widget should aim to fit.
        It is OK if it does not: for some widgets there is no way to
        adjust to a smaller size.
        
        '''
