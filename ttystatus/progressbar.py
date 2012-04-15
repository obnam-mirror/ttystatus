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

    static_width = False
    
    def __init__(self, done_name, total_name):
        self.done_name = done_name
        self.total_name = total_name
        self.done = 0
        self.total = 1

    def render(self, width):
        try:
            done = float(self.done)
            total = float(self.total)
        except ValueError:
            done = 0
            total = 1
        if total == 0:
            fraction = 0
        else:
            fraction = done / total
        n_stars = int(round(fraction * width))
        n_dashes = int(width - n_stars)
        return ('#' * n_stars) + ('-' * n_dashes)
        
    def update(self, master):
        self.done = master[self.done_name]
        self.total = master[self.total_name]
