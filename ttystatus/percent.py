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


class PercentDone(ttystatus.Widget):

    '''Display percent of task done.'''
    
    def __init__(self, done_name, total_name, decimals=0):
        self.done_name = done_name
        self.total_name = total_name
        self.decimals = decimals
        self.value = self.format(0, 1)
        self.interesting_keys = set([done_name, total_name])
        
    def format(self, done, total):
        try:
            done = float(done)
            total = float(total)
        except ValueError:
            return self.value
        else:
            return '%.*f %%' % (self.decimals, 100.0 * done / total)
        
    def update(self, master, width):
        self.value = self.format(master[self.done_name], 
                                 master[self.total_name])
