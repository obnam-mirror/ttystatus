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


class RemainingTimeTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.RemainingTime('done', 'total')
        self.w.get_time = lambda: 0

    def test_is_zero_initially(self):
        self.assertEqual(str(self.w), '00h00m00s')

    def test_formats_zero_correctly(self):
        self.w.update({ 'done': 0, 'total': 0 }, 999)
        self.assertEqual(str(self.w), '00h00m00s')

    def test_formats_nonzero_correctly(self):
        self.w.update({ 'done': 0, 'total': 100 }, 999)
        self.w.get_time = lambda: 5
        self.w.update({ 'done': 5, 'total': 100 }, 999)
        self.assertEqual(str(self.w), '00h01m35s')

