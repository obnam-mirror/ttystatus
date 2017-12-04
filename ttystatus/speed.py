# Copyright 2010, 2012  Lars Wirzenius
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


class Speed(ttystatus.Widget):

    '''Display speed of changes.'''

    static_width = False

    def __init__(self, name, duration=None):
        self.name = name
        self._duration = None if duration is None else float(duration)
        self._data_points = []
        self._changes = 0

    def now(self):  # pragma: no cover
        '''Wrapper around time.time for unit tests to overrride.'''
        return time.time()

    def render(self, width):
        if len(self._data_points) < 2:
            speed = 0.0
        else:  # pragma: no cover
            oldest, started = self._data_points[0]
            latest, _ = self._data_points[-1]
            delta = latest - oldest
            now = self.now()
            duration = now - started
            speed = float(delta) / float(duration)

        return '%.2f/s' % float(speed)

    def update(self, master):  # pragma: no cover
        self._changes += 1
        now = self.now()
        self._data_points.append((self._changes, now))
        if self._duration is None:
            if len(self._data_points) > 2:
                del self._data_points[1:-1]
        else:
            cutoff = now - self._duration
            while self._data_points[0][1] < cutoff:
                del self._data_points[0]
