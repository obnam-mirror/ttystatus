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


class PercentDoneTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.PercentDone('done', 'total', decimals=1)

    def test_shows_zero_value_initially(self):
        self.assertEqual(str(self.w), '0.0 %')

    def test_sets_value(self):
        self.w.update({ 'done': 50, 'total': 100 }, 999)
        self.assertEqual(str(self.w), '50.0 %')

    def test_handles_empty_strings_as_values(self):
        self.w.update({ 'done': '', 'total': '' }, 999)
        self.assertEqual(str(self.w), '0.0 %')

    def test_handles_zero_total(self):
        self.w.update({ 'done': '', 'total': 0 }, 999)
        self.assertEqual(str(self.w), '0.0 %')

