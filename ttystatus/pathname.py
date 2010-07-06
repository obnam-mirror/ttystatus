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


class Pathname(ttystatus.Widget):

    '''Display a pathname.
    
    If it won't fit completely, truncate from the beginning of the string.
    
    '''
    
    def __init__(self, key):
        self._key = key
        self.interesting_keys = set([key])
        
    def update(self, master, width):
        v = master.get(self._key, '')
        if len(v) > width:
            ellipsis = '...'
            if len(ellipsis) < width:
                v = ellipsis + v[-(width - len(ellipsis)):]
            else:
                v = v[-width:]
        self.value = v
