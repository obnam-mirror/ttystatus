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
        
    def notify(self, string, f):
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
        self.assertEqual(self.ts._widgets, [])
        
    def test_adds_widget(self):
        w = ttystatus.Literal('foo')
        self.ts.add(w)
        self.assertEqual(self.ts._widgets, [w])
        
    def test_adds_widget_as_interested_in_keys(self):
        class W(ttystatus.Widget):
            def __init__(self):
                self.interesting_keys = ['foo']
        w = W()
        self.ts.add(w)
        self.assert_(w in self.ts._interests['foo'])

    def test_adds_widget_to_wildcards(self):
        class W(ttystatus.Widget):
            def __init__(self):
                self.interesting_keys = None
        w = W()
        self.ts.add(w)
        self.assert_(w in self.ts._wildcards)

    def test_adds_widgets_from_format_string(self):
        self.ts.format('hello, %String(name)')
        self.assertEqual(len(self.ts._widgets), 2)
        self.assertEqual(type(self.ts._widgets[0]), ttystatus.Literal)
        self.assertEqual(type(self.ts._widgets[1]), ttystatus.String)
        
    def test_removes_all_widgets(self):
        self.ts.add(ttystatus.Literal('foo'))
        self.ts.clear()
        self.assertEqual(self.ts._widgets, [])
        
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
        self.assertEqual(str(w), '')
        self.ts['foo'] = 'bar'
        self.assertEqual(str(w), 'bar')

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

    def test_disable_calls_messager_disable(self):
        self.ts.disable()
        self.assertFalse(self.ts._m.enabled)

    def test_enable_calls_messager_enable(self):
        self.ts.disable()
        self.ts.enable()
        self.assert_(self.ts._m.enabled)

