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


class ElapsedtimeTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.ElapsedTime()

    def test_is_static_width(self):
        self.assertTrue(self.w.static_width)

    def test_shows_zero_initially(self):
        self.assertEqual(self.w.render(0), '00h00m00s')

    def test_shows_zero_after_first_update(self):
        self.w.get_time = lambda: 1
        self.w.update({})
        self.assertEqual(self.w.render(0), '00h00m00s')

    def test_shows_one_one_one_after_second_update(self):
        self.w.get_time = lambda: 0
        self.w.update({})
        self.w.get_time = lambda: 60 * 60 + 60 + 1
        self.w.update({})
        self.assertEqual(self.w.render(0), '01h01m01s')
