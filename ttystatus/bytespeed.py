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


class ByteSpeed(ttystatus.Widget):

    '''Display data size in bytes, KiB, etc.'''

    static_width = False

    def __init__(self, name, duration=None):
        self.name = name
        self._duration = None if duration is None else float(duration)
        self._data_points = []

    def now(self):  # pragma: no cover
        '''Wrapper around time.time for unit tests to overrride.'''
        return time.time()

    def render(self, width):
        units = (
            (1024 ** 4, 2, 'TiB/s'),
            (1024 ** 3, 2, 'GiB/s'),
            (1024 ** 2, 2, 'MiB/s'),
            (1024 ** 1, 1, 'KiB/s'),
        )

        if len(self._data_points) < 2:
            return '0 B/s'

        oldest_bytes, started = self._data_points[0]
        latest_bytes, dummy = self._data_points[-1]
        num_bytes = latest_bytes - oldest_bytes
        duration = self.now() - started
        speed = num_bytes / duration

        for factor, decimals, unit in units:
            if speed >= factor:
                return '%.*f %s' % (decimals,
                                    float(speed) / float(factor),
                                    unit)
        return '%.0f B/s' % speed

    def update(self, master):
        num_bytes = master[self.name]
        now = self.now()
        self._data_points.append((num_bytes, now))
        if self._duration is None:
            if len(self._data_points) > 2:
                del self._data_points[1:-1]
        else:
            cutoff = now - self._duration
            while self._data_points[0][1] < cutoff:
                del self._data_points[0]
