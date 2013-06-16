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


class DummyTerminal(StringIO.StringIO):

    def isatty(self):
        return True


class MessagerTests(unittest.TestCase):

    def setUp(self):
        self.output = DummyTerminal()
        self.messager = ttystatus.Messager(output=self.output, fake_width=True)

    def fast_time(self):
        return self.messager._last_time + self.messager._period
        
    def test_sets_output(self):
        self.assertEqual(self.messager.output, self.output)
        
    def test_handles_no_tty(self):
        def notty():
            raise IOError()
        m = ttystatus.Messager(open_tty=notty)
        self.assertEqual(m.output, None)
        
    def test_raw_writes_nothing_if_output_is_not_a_terminal(self):
        self.messager.output = StringIO.StringIO()
        self.messager._raw_write('foo')
        self.assertEqual(self.messager.output.getvalue(), '')
        
    def test_raw_writes_something_if_output_is_not_a_terminal(self):
        self.messager._raw_write('foo')
        self.assertEqual(self.output.getvalue(), 'foo')

    def test_knows_it_is_time_to_write_at_start(self):
        self.assert_(self.messager.time_to_write())

    def test_knows_it_is_not_time_to_write_right_after_previous_one(self):
        self.messager._last_time = self.messager._now()
        self.assertFalse(self.messager.time_to_write())

    def test_knows_it_is_time_to_write_after_a_period(self):
        self.messager._last_time = (self.messager._now() - 
                                    self.messager._period*2)
        self.assert_(self.messager.time_to_write())
        
    def test_cached_write_writes_first_thing(self):
        self.messager.write('foo')
        self.assertEqual(self.output.getvalue(), 'foo')

    def test_write_removes_old_message(self):
        self.messager._now = self.fast_time
        self.messager.write('foo')
        self.messager.write('bar')
        self.assertEqual(self.output.getvalue(), 'foo\r   \rbar')

    def test_clear_removes_message(self):
        self.messager._now = lambda: self.messager._period + 1
        self.messager.write('foo')
        self.messager.clear()
        self.assertEqual(self.output.getvalue(), 'foo\r   \r')

    def test_notify_removes_message_and_puts_it_back_afterwards(self):
        f = StringIO.StringIO()
        self.messager.write('foo')
        self.messager.notify('bar', f)
        self.assertEqual(self.output.getvalue(), 'foo\r   \rfoo')
        self.assertEqual(f.getvalue(), 'bar\n')

    def test_notify_does_not_mind_ioerror(self):
        f = open('/dev/full', 'w')
        self.messager.write('foo')
        self.messager.notify('bar', f)
        self.assertEqual(self.output.getvalue(), 'foo\r   \rfoo')
        f.close()

    def test_finish_flushes_unwritten_message(self):
        self.messager._now = lambda: 0
        self.messager.write('foo')
        self.messager.finish()
        self.assertEqual(self.output.getvalue(), 'foo\r   \rfoo\n')
        
    def test_has_width(self):
        self.assertEqual(self.messager.width, 79)
        
    def test_write_truncates_at_one_less_than_width(self):
        self.messager.set_width(4)
        self.messager.write('foobar')
        self.assertEqual(self.output.getvalue(), 'foo')

    def test_disables_output(self):
        self.messager.disable()
        self.messager.write('foo')
        self.assertEqual(self.output.getvalue(), '')

    def test_enables_output(self):
        self.messager.disable()
        self.messager.enable()
        self.messager.write('foo')
        self.assertEqual(self.output.getvalue(), 'foo')

