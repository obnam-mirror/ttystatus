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


class ByteSize(ttystatus.Widget):

    '''Display data size in bytes, KiB, etc.'''
    
    def __init__(self, name):
        self.name = name
        self.value = self.format(0)
        
    def format(self, bytes):
        units = (
            (1024**4, 2, 'TiB'),
            (1024**3, 2, 'GiB'),
            (1024**2, 2, 'MiB'),
            (1024**1, 1, 'KiB'),
        )
        
        for factor, decimals, unit in units:
            if bytes >= factor:
                return '%.*f %s' % (decimals,
                                    float(bytes) / float(factor), 
                                    unit)
        return '%d B' % bytes
        
    def update(self, master, width):
        self.value = self.format(master[self.name])
