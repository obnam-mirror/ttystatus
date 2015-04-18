# Copyright 2011  Lars Wirzenius
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


class FormatTests(unittest.TestCase):

    def test_knows_widgets(self):
        self.assertEqual(type(ttystatus.fmt.widgets), list)
        self.assert_(len(ttystatus.fmt.widgets) > 0)
        for widget in ttystatus.fmt.widgets:
            self.assert_(issubclass(widget, ttystatus.Widget))
            self.assertNotEqual(widget, ttystatus.Widget)

    def test_parses_string_without_widgets(self):
        x = ttystatus.fmt.parse('hello, world')
        self.assertEqual(len(x), 1)
        self.assertEqual(type(x[0]), ttystatus.Literal)
        self.assertEqual(x[0].render(0), 'hello, world')

    def test_parses_escaped_pecent(self):
        x = ttystatus.fmt.parse('%%')
        self.assertEqual(len(x), 1)
        self.assertEqual(type(x[0]), ttystatus.Literal)
        self.assertEqual(x[0].render(0), '%')

    def test_parses_parameterless_widget(self):
        x = ttystatus.fmt.parse('%ElapsedTime()')

        self.assertEqual(len(x), 1)
        self.assertEqual(type(x[0]), ttystatus.ElapsedTime)

    def test_parses_widget_with_one_parameter(self):
        x = ttystatus.fmt.parse('%String(name)')

        self.assertEqual(len(x), 1)

        self.assertEqual(type(x[0]), ttystatus.String)
        self.assertEqual(x[0]._key, 'name')

    def test_parses_some_widgets(self):
        x = ttystatus.fmt.parse('hello, %String(name): %ElapsedTime()')

        self.assertEqual(len(x), 4)

        self.assertEqual(type(x[0]), ttystatus.Literal)
        self.assertEqual(x[0].render(0), 'hello, ')

        self.assertEqual(type(x[1]), ttystatus.String)

        self.assertEqual(type(x[2]), ttystatus.Literal)
        self.assertEqual(x[2].render(0), ': ')

        self.assertEqual(type(x[3]), ttystatus.ElapsedTime)
