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


class IndexTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.Index('foo', 'foos')

    def test_is_not_static_width(self):
        self.assertFalse(self.w.static_width)

    def test_is_zero_initially(self):
        self.assertEqual(self.w.render(0), '0/0')

    def test_gets_index_right(self):
        self.w.update({'foo': 'x', 'foos': ['a', 'x', 'b']})
        self.assertEqual(self.w.render(0), '2/3')

    def test_handles_value_not_in_list(self):
        self.w.update({'foo': 'xxx', 'foos': ['a', 'x', 'b']})
        self.assertEqual(self.w.render(0), '0/3')
