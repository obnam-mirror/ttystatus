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


class CounterTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.Counter('foo')

    def test_counts_zero_initially(self):
        self.assertEqual(self.w.render(), '0')

    def test_counts_one_change(self):
        self.w.update({ 'foo': 'a' })
        self.assertEqual(self.w.render(), '1')

    def test_counts_two_changes(self):
        self.w.update({ 'foo': 'a' })
        self.w.update({ 'foo': 'b' })
        self.assertEqual(self.w.render(), '2')

    def test_does_not_count_if_value_does_not_change(self):
        self.w.update({ 'foo': 'a' })
        self.w.update({ 'foo': 'a' })
        self.assertEqual(self.w.render(), '1')

