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


import fcntl
import signal
import struct
import sys
import time


class Messager(object):

    '''Write messages to the terminal.'''
    
    def __init__(self, output=None):
        self.output = output or sys.stderr
        self._last_msg = '' # What did we write last?
        self._last_time = 0 # When did we write last?
        self._period = 1 # How long between updates?
        self._cached_msg = '' # Last message from user, to write() method.
        self.width = self._get_terminal_width() # Width of terminal
        signal.signal(signal.SIGWINCH, self._sigwinch_handler)
        
    def _now(self):
        '''Return current time.'''
        # This is a wrapper around time.time(), for testing.
        return time.time()
        
    def _get_terminal_width(self): # pragma: no cover
        '''Return width of terminal in characters.

        If this fails, assume 80.
        
        Borrowed and adapted from bzrlib.
        
        '''
        
        default_width = 80
        try:
            s = struct.pack('HHHH', 0, 0, 0, 0)
            x = fcntl.ioctl(self.output.fileno(), termios.TIOCGWINSZ, s)
            return struct.unpack('HHHH', x)[1]
        except IOError:
            return default_width
        except AttributeError:
            if not hasattr(self.output, 'fileno'):
                return default_width
            raise

    def _sigwinch_handler(self, signum, frame): # pragma: no cover
        # Clear the terminal from old stuff, using the old width.
        self.clear()
        # Get new width.
        self.width = self.get_terminal_width()

    def _raw_write(self, string):
        '''Write raw data if output is terminal.'''
        if self.output.isatty():
            self.output.write(string)

    def _overwrite(self, string):
        '''Overwrite current message on terminal.'''
        if self._last_msg:
            self._raw_write('\r' + (' ' * len(self._last_msg)) + '\r')
        self._raw_write(string)
        self._last_msg = string
            
    def write(self, string):
        '''Write raw data, but only once per period.'''
        string = string[:self.width - 1]
        now = self._now()
        if now - self._last_time >= self._period:
            self._overwrite(string)
            self._last_time = now
        self._cached_msg = string
            
    def clear(self):
        '''Remove current message from terminal.'''
        self._overwrite('')
        
    def notify(self, string):
        '''Show a notification message string to the user.
        
        Notifications are meant for error messages and other things
        that do not belong in, say, progress bars. Whatever is currently
        on the terminal is wiped, then the notification message is shown,
        a new line is started, and the old message is restored.
        
        Notifications are written even when the output is not going
        to a terminal.
        
        '''
        
        old = self._last_msg
        self.clear()
        self.output.write('%s\n' % string)
        self._overwrite(old)
        
    def finish(self):
        '''Finalize output.'''
        self._overwrite(self._cached_msg)
        self._raw_write('\n')
