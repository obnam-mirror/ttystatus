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
        self.w.get_time = lambda: 0.0

    def test_is_static_width(self):
        self.assertTrue(self.w.static_width)

    def test_is_dashes_initially(self):
        self.assertEqual(self.w.render(0), '--h--m--s')

    def test_estimates_and_formats_correctly(self):
        self.assertEqual(self.w.render(0), '--h--m--s')
        self.w.update({'done': 0, 'total': 100})
        self.w.get_time = lambda: 5.0
        self.w.update({'done': 5, 'total': 100})
        self.assertEqual(self.w.render(0), '00h01m35s')
        self.w.get_time = lambda: 10.0
        self.w.update({'done': 5, 'total': 100})
        self.assertEqual(self.w.render(0), '00h03m10s')
        self.w.get_time = lambda: 20.0
        self.w.update({'done': 80, 'total': 100})
        self.assertEqual(self.w.render(0), '00h00m05s')

    def test_handles_zero_speed(self):
        self.w.update({'done': 0, 'total': 100})
        self.w.get_time = lambda: 5.0
        self.w.update({'done': 0, 'total': 100})
        self.assertEqual(self.w.render(0), '--h--m--s')

    def test_handles_empty_strings_for_done_and_total(self):
        self.w.update({'done': '', 'total': ''})
        self.w.get_time = lambda: 5.0
        self.w.update({'done': '', 'total': ''})
        self.assertEqual(self.w.render(0), '--h--m--s')
