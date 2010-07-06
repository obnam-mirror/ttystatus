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
    
    A widget's value may be derived from values stored in the TerminalStatus
    widget (called master). Each such value has a key. Computing a widget's
    value is a two-step process: when the values associated with keys
    are updated, the widget's update() method is called to notify it of
    this. update() may compute intermediate values, such as maintain a
    counter of the number of changes. It should avoid costly operations
    that are only needed when the widget's formatted value is needed.
    Those should go into the format() method instead. Thus, update() would
    update a counter, format() would create a string representing the
    counter.
    
    This is necessary because actual on-screen updates only happen
    every so often, not every time a value in the master changes, and
    often the string formatting part is expensive.
    
    Widgets must have an attribute 'interesting_keys', listing the
    keys it is interested in.
    
    '''

    def __str__(self):
        '''Return current value to be displayed for this widget.'''
        return self.format()

    def format(self):
        '''Format the current value.
        
        This will be called only when the value actually needs to be
        formatted.
        
        '''
        
        return ''

    def update(self, master, width):
        '''Update displayed value for widget, from values in master.
        
        'width' gives the width for which the widget should aim to fit.
        It is OK if it does not: for some widgets there is no way to
        adjust to a smaller size.
        
        '''
