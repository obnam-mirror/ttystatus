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


class Counter(ttystatus.Widget):

    '''Display a count of how many times a value has changed.'''
    
    def __init__(self, name):
        self.name = name
        self.prev = None
        self.count = 0
        self.interesting_keys = [name]

    def format(self):
        return str(self.count)
        
    def update(self, master, width):
        if master[self.name] != self.prev:
            self.prev = master[self.name]
            self.count += 1
