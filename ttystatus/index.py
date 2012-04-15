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


class Index(ttystatus.Widget):

    '''Display the position of a value in a list of values.'''
    
    static_width = False

    def __init__(self, name, listname):
        self.name = name
        self.listname = listname
        self.value = None
        self.listvalue = []
        
    def render(self, render):
        try:
            index = self.listvalue.index(self.value) + 1
        except ValueError:
            index = 0
        return '%d/%d' % (index, len(self.listvalue))
        
    def update(self, master):
        self.value = master[self.name]
        self.listvalue = master[self.listname]

