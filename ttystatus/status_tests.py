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


class DummyMessager(object):

    width = 80

    def clear(self):
        pass

    def time_to_write(self):
        return True
        
    def write(self, string):
        pass
        
    def notify(self, string):
        pass
        
    def finish(self):
        pass


class TerminalStatusTests(unittest.TestCase):

    def setUp(self):
        self.ts = ttystatus.TerminalStatus(messager=DummyMessager())
        
    def test_has_no_widgets(self):
        self.assertEqual(self.ts._widgets, [])
        
    def test_adds_widget(self):
        w = ttystatus.Literal('foo')
        self.ts.add(w)
        self.assertEqual(self.ts._widgets, [w])
        
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
        
    def test_has_finish_method(self):
        self.assertEqual(self.ts.finish(), None)

