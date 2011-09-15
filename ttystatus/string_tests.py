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


class StringTests(unittest.TestCase):

    def setUp(self):
        self.s = ttystatus.String('foo')

    def test_is_empty_initially(self):
        self.assertEqual(str(self.s), '')
        
    def test_updates(self):
        self.s.update({'foo': 'bar'}, 999)
        self.assertEqual(str(self.s), 'bar')
        
    def test_handles_non_string_value(self):
        self.s.update({'foo': 123}, 999)
        self.assertEqual(str(self.s), '123')
