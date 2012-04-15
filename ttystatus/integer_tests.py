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


class IntegerTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.Integer('foo')

    def test_is_error_initially(self):
        self.assertEqual(str(self.w), '#')
        
    def test_updates(self):
        self.w.update({'foo': 123})
        self.assertEqual(str(self.w), '123')
        
    def test_becomes_error_symbol_if_value_is_not_integer(self):
        self.w.update({'foo': 'bar'})
        self.assertEqual(str(self.w), '#')

