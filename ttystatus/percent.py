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
        self.done = 0
        self.total = 1
        
    def render(self):
        try:
            done = float(self.done)
            total = float(self.total)
        except ValueError:
            done = 0
            total = 1
        if total < 0.001:
            total = 1
        return '%.*f %%' % (self.decimals, 100.0 * done / total)
        
    def update(self, master):
        self.done = master[self.done_name]
        self.total = master[self.total_name]
