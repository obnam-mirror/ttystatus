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


import unittest

import ttystatus


class ByteSpeedTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.ByteSpeed('foo')

    def test_is_not_static_width(self):
        self.assertFalse(self.w.static_width)

    def test_formats_zero_speed_without_update(self):
        self.assertEqual(self.w.render(0), '0 B/s')

    def test_formats_zero_bytes_correctly(self):
        self.w.now = lambda: 1
        self.w.update({'foo': 0})
        self.w.now = lambda: 2
        self.w.update({'foo': 0})
        self.assertEqual(self.w.render(0), '0 B/s')

    def test_formats_one_byte_per_second_correctly(self):
        self.w.now = lambda: 1
        self.w.update({'foo': 0})
        self.w.now = lambda: 2
        self.w.update({'foo': 1})
        self.assertEqual(self.w.render(0), '1 B/s')

    def test_formats_ten_bytes_per_second_correctly(self):
        self.w.now = lambda: 1
        self.w.update({'foo': 0})
        self.w.now = lambda: 11
        self.w.update({'foo': 100})
        self.assertEqual(self.w.render(0), '10 B/s')

    def test_formats_ten_tibs_per_second_correctly(self):
        self.w.now = lambda: 1
        self.w.update({'foo': 0})
        self.w.now = lambda: 2
        self.w.update({'foo': 10 * 1024**4})
        self.assertEqual(self.w.render(0), '10.00 TiB/s')

    def test_keeps_only_two_data_points_with_infinite_duration(self):
        for when in range(100):
            self.w.now = lambda: when
            self.w.update({'foo': 0})
        self.assertEqual(self.w.render(0), '0 B/s')

    def test_shows_current_speed_when_requested(self):
        items = [
            (0, 0),
            (1, 1024),
            (10, 1024),
            (11, 1024),
        ]

        w = ttystatus.ByteSpeed('foo', duration=5)
        for when, num_bytes in items:
            w.now = lambda: when
            w.update({'foo': num_bytes})
        self.assertEqual(w.render(0), '0 B/s')
