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


class PathnameTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.Pathname('foo')

    def test_is_empty_initially(self):
        self.assertEqual(str(self.w), '')
        
    def test_updates(self):
        self.w.update({'foo': 'bar'}, 999)
        self.assertEqual(str(self.w), 'bar')

    def test_handles_update_to_other_value(self):
        self.w.update({'other': 1}, 999)
        self.assertEqual(str(self.w), '')
        
    def test_truncates_from_beginning(self):
        self.w.update({'foo': 'foobar'}, 5)
        self.assertEqual(str(self.w), '...ar')
        
    def test_does_not_truncate_for_exact_fit(self):
        self.w.update({'foo': 'foobar'}, 6)
        self.assertEqual(str(self.w), 'foobar')
        
    def test_does_not_add_ellipsis_if_it_will_not_fit(self):
        self.w.update({'foo': 'foobar'}, 3)
        self.assertEqual(str(self.w), 'bar')
        
    def test_adds_ellipsis_if_it_just_fits(self):
        self.w.update({'foo': 'foobar'}, 4)
        self.assertEqual(str(self.w), '...r')

