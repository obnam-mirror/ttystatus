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


class ProgressBarTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.ProgressBar('done', 'total')
        self.width = 10

    def test_is_not_static_width(self):
        self.assertFalse(self.w.static_width)

    def test_sets_initial_value_to_empty(self):
        self.assertEqual(self.w.render(self.width), '-' * 10)

    def test_shows_zero_percent_for_empty_string_total(self):
        self.w.update({'done': 1, 'total': ''})
        self.assertEqual(self.w.render(self.width), '-' * 10)

    def test_shows_zero_percent_for_zero_total(self):
        self.w.update({'done': 1, 'total': 0})
        self.assertEqual(self.w.render(self.width), '-' * 10)

    def test_shows_zero_percent_correctly(self):
        self.w.update({'done': 0, 'total': 100})
        self.assertEqual(self.w.render(self.width), '-' * 10)

    def test_shows_one_percent_correctly(self):
        self.w.update({'done': 1, 'total': 100})
        self.assertEqual(self.w.render(self.width), '-' * 10)

    def test_shows_ten_percent_correctly(self):
        self.w.update({'done': 10, 'total': 100})
        self.assertEqual(self.w.render(self.width), '#' + '-' * 9)

    def test_shows_ninety_percent_correctly(self):
        self.w.update({'done': 90, 'total': 100})
        self.assertEqual(self.w.render(self.width), '#' * 9 + '-')

    def test_shows_ninety_ine_percent_correctly(self):
        self.w.update({'done': 99, 'total': 100})
        self.assertEqual(self.w.render(self.width), '#' * 10)

    def test_shows_one_hundred_percent_correctly(self):
        self.w.update({'done': 100, 'total': 100})
        self.assertEqual(self.w.render(self.width), '#' * 10)
