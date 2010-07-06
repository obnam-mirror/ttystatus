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


class RemainingTime(ttystatus.Widget):

    '''Display an estimate of the remaining time.'''
    
    def __init__(self, done_name, total_name):
        self.done_name = done_name
        self.total_name = total_name
        self.started = None
        self.default = '--h--m--s'
        self.value = self.default
        self.interesting_keys = [done_name, total_name]
        
    def get_time(self): # pragma: no cover
        '''Return current time.
        
        This is just a wrapper around time.time() so that it is easier
        to override during unit tests.
        
        '''
        
        return time.time()
        
    def format(self, secs):
        hours = secs / (60 * 60)
        secs %= (60 * 60)
        mins = secs / 60
        secs %= 60
        return '%02dh%02dm%02ds' % (hours, mins, secs)
        
    def update(self, master, width):
        if self.started is None:
            self.started = self.get_time()
        duration = self.get_time() - self.started
        if duration >= 1.0:
            done = float(master.get(self.done_name, 0) or 0)
            total = float(master.get(self.total_name, 0) or 0)
            speed = done / duration
            remaining = total - done
            if speed > 0:
                secs = remaining / speed
                self.value = self.format(secs)
            else:
                self.value = self.default
