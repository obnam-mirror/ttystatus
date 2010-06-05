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


import StringIO
import unittest

import ttystatus


class DummyTerminal(StringIO.StringIO):

    def isatty(self):
        return True


class MessagerTests(unittest.TestCase):

    def setUp(self):
        self.output = DummyTerminal()
        self.messager = ttystatus.Messager(output=self.output)
        
    def test_sets_output(self):
        self.assertEqual(self.messager.output, self.output)
        
    def test_writes_nothing_if_output_is_not_a_terminal(self):
        self.messager.output = StringIO.StringIO()
        self.messager.raw_write('foo')
        self.assertEqual(self.output.getvalue(), '')
