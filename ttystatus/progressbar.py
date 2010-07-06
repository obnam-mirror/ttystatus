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


class ProgressBar(ttystatus.Widget):

    '''Display a progress bar.'''
    
    def __init__(self, done_name, total_name):
        self.done_name = done_name
        self.total_name = total_name
        self.interesting_keys = [done_name, total_name]
        
    def update(self, master, width):
        done = float(master.get(self.done_name, 0))
        total = float(master.get(self.total_name, 1) or 0)
        if total == 0:
            fraction = 0
        else:
            fraction = done / total
        n_stars = int(round(fraction * width))
        n_dashes = int(width - n_stars)
        self.value = ('#' * n_stars) + ('-' * n_dashes)

