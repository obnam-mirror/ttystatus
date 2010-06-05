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


import sys
import time


class Messager(object):

    '''Write messages to the terminal.'''
    
    def __init__(self, output=None):
        self.output = output or sys.stderr
        self._last_msg = '' # What did we write last?
        self._last_time = 0 # When did we write last?
        self._period = 1 # How long between updates?
        
    def _now(self):
        '''Return current time.'''
        # This is a wrapper around time.time(), for testing.
        return time.time()
        
    def _raw_write(self, string):
        '''Write raw data if output is terminal.'''
        if self.output.isatty():
            if self._last_msg:
                self.output.write('\r' + (' ' * len(self._last_msg)) + '\r')
            self.output.write(string)
            self._last_msg = string
            
    def write(self, string):
        '''Write raw data, but only once per period.'''
        now = self._now()
        if now - self._last_time >= self._period:
            self._raw_write(string)
            self._last_time = now
