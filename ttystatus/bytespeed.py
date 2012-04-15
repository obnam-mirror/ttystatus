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


class ByteSpeed(ttystatus.Widget):

    '''Display data size in bytes, KiB, etc.'''
    
    def __init__(self, name):
        self.name = name
        self._bytes = 0
        self._started = None
        
    def now(self):
        '''Wrapper around time.time for unit tests to overrride.'''
        
        return time.time()
        
    def __str__(self):
        units = (
            (1024**4, 2, 'TiB/s'),
            (1024**3, 2, 'GiB/s'),
            (1024**2, 2, 'MiB/s'),
            (1024**1, 1, 'KiB/s'),
        )
        
        if self._started is None:
            return '0 B/s'
        
        duration = self.now() - self._started
        speed = self._bytes / duration
        
        for factor, decimals, unit in units:
            if speed >= factor:
                return '%.*f %s' % (decimals,
                                    float(speed) / float(factor), 
                                    unit)
        return '%.0f B/s' % speed
        
    def update(self, master):
        if self._started is None:
            self._started = self.now()
        self._bytes = master[self.name]
