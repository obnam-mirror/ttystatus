# Copyright 2010, 2011  Lars Wirzenius
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


class DummyMessager(object):

    width = 80

    def __init__(self):
        self.written = StringIO.StringIO()
        self.enabled = True

    def clear(self):
        pass

    def time_to_write(self):
        return True

    def write(self, string):
        self.written.write(string)

    def notify(self, string, f, force=False):
        pass

    def finish(self):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


class TerminalStatusTests(unittest.TestCase):

    def setUp(self):
        self.ts = ttystatus.TerminalStatus(messager=DummyMessager())

    def test_has_no_widgets(self):
        self.assertEqual(self.ts.widgets, [])

    def test_adds_widget(self):
        w = ttystatus.Literal('foo')
        self.ts.add(w)
        self.assertEqual(self.ts.widgets, [w])

    def test_adds_widgets_from_format_string(self):
        self.ts.format('hello, %String(name)')
        self.assertEqual(len(self.ts.widgets), 2)
        self.assertEqual(type(self.ts.widgets[0]), ttystatus.Literal)
        self.assertEqual(type(self.ts.widgets[1]), ttystatus.String)

    def test_removes_all_widgets(self):
        self.ts.add(ttystatus.Literal('foo'))
        self.ts.clear()
        self.assertEqual(self.ts.widgets, [])

    def test_returns_empty_string_for_unknown_value(self):
        self.assertEqual(self.ts['foo'], '')

    def test_sets_value(self):
        self.ts['foo'] = 'bar'
        self.assertEqual(self.ts['foo'], 'bar')

    def test_gets_value(self):
        self.ts['foo'] = 'bar'
        self.assertEqual(self.ts.get('foo'), 'bar')

    def test_gets_default_value_for_nonexistent_key(self):
        self.assertEqual(self.ts.get('foo', 'bar'), 'bar')

    def test_gets_None_for_nonexistent_key_without_default_value(self):
        self.assertEqual(self.ts.get('foo'), None)

    def test_updates_widgets_when_value_is_set(self):
        w = ttystatus.String('foo')
        self.ts.add(w)
        self.assertEqual(w.render(0), '')
        self.ts['foo'] = 'bar'
        self.assertEqual(w.render(0), 'bar')

    def test_increases_value(self):
        self.ts['foo'] = 10
        self.assertEqual(self.ts['foo'], 10)
        self.ts.increase('foo', 10)
        self.assertEqual(self.ts['foo'], 20)

    def test_has_notify_method(self):
        self.assertEqual(self.ts.notify('foo'), None)

    def test_has_error_method(self):
        self.assertEqual(self.ts.error('foo'), None)

    def test_has_finish_method(self):
        self.assertEqual(self.ts.finish(), None)

    def test_flushes(self):
        self.ts._m.time_to_write = lambda: False
        self.ts.format('%String(foo)')
        self.ts['foo'] = 'foo'
        self.assertEqual(self.ts._m.written.getvalue(), '')
        self.ts.flush()
        self.assertEqual(self.ts._m.written.getvalue(), 'foo')

    def test_disable_calls_messager_disable(self):
        self.ts.disable()
        self.assertFalse(self.ts._m.enabled)

    def test_enable_calls_messager_enable(self):
        self.ts.disable()
        self.ts.enable()
        self.assert_(self.ts._m.enabled)

    def test_counts_correctly_even_without_rendering(self):
        w = ttystatus.Counter('value')
        n = 42
        self.ts.add(w)
        for i in range(n):
            self.ts['value'] = i
        self.assertEqual(w.render(0), str(n))

    def test_renders_everything_when_there_is_space(self):
        w1 = ttystatus.Literal('foo')
        w2 = ttystatus.ProgressBar('done', 'total')
        self.ts.add(w1)
        self.ts.add(w2)
        text = self.ts._render()
        self.assertEqual(len(text), self.ts._m.width)

    def test_renders_from_beginning_if_there_is_not_enough_space(self):
        w1 = ttystatus.Literal('foo')
        w2 = ttystatus.Literal('bar')
        self.ts.add(w1)
        self.ts.add(w2)
        self.ts._m.width = 4
        text = self.ts._render()
        self.assertEqual(text, 'foob')

    def test_renders_variable_size_width_according_to_space_keep_static(self):
        w1 = ttystatus.Literal('foo')
        w2 = ttystatus.ProgressBar('done', 'total')
        w3 = ttystatus.Literal('bar')
        self.ts.add(w1)
        self.ts.add(w2)
        self.ts.add(w3)
        self.ts._m.width = 9
        text = self.ts._render()
        self.assertEqual(text, 'foo---bar')
