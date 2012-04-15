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


import time

import ttystatus


class ElapsedTime(ttystatus.Widget):

    '''Display elapsed time since widget was first updated.'''
    
    def __init__(self):
        self.started = None
        self.secs = 0
        
    def get_time(self): # pragma: no cover
        '''Wrapper around time.time() for unit tests to override.'''
        return time.time()

    def __str__(self):
        secs = self.secs
        hours = secs / 3600
        secs %= 3600
        mins = secs / 60
        secs %= 60
        return '%02dh%02dm%02ds' % (hours, mins, secs)
        
    def update(self, master):
        if self.started is None:
            self.started = self.get_time()
        self.secs = self.get_time() - self.started
