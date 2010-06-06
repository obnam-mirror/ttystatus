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


class TerminalStatusTests(unittest.TestCase):

    def setUp(self):
        self.ts = ttystatus.TerminalStatus()
        
    def test_has_no_widgets(self):
        self.assertEqual(self.ts._widgets, [])
        
    def test_adds_widget(self):
        w = ttystatus.Literal('foo')
        self.ts.add(w)
        self.assertEqual(self.ts._widgets, [w])
