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


class ByteSizeTests(unittest.TestCase):

    def setUp(self):
        self.w = ttystatus.ByteSize('foo')

    def test_formats_zero_bytes_without_update(self):
        self.assertEqual(str(self.w), '0 B')

    def test_formats_zero_bytes_correctly(self):
        self.w.update({ 'foo': 0 }, 999)
        self.assertEqual(str(self.w), '0 B')

    def test_formats_one_bytes_correctly(self):
        self.w.update({ 'foo': 1 }, 999)
        self.assertEqual(str(self.w), '1 B')

    def test_formats_1023_bytes_correctly(self):
        self.w.update({ 'foo': 1023 }, 999)
        self.assertEqual(str(self.w), '1023 B')

    def test_formats_1024_bytes_correctly(self):
        self.w.update({ 'foo': 1024 }, 999)
        self.assertEqual(str(self.w), '1.0 KiB')

    def test_formats_1_MiB_bytes_correctly(self):
        self.w.update({ 'foo': 1024**2 }, 999)
        self.assertEqual(str(self.w), '1.00 MiB')

    def test_formats_1_GiB_bytes_correctly(self):
        self.w.update({ 'foo': 1024**3 }, 999)
        self.assertEqual(str(self.w), '1.00 GiB')

    def test_formats_1_TiB_bytes_correctly(self):
        self.w.update({ 'foo': 1024**4 }, 999)
        self.assertEqual(str(self.w), '1.00 TiB')
