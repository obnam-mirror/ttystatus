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


import time

import ttystatus


class Messager(object):

    '''Manages messages to the terminal.

    This includes disabling messages, allowing notifications, and
    becalming the flow of messages to avoid writing too fast. The
    speed is a performance thing: writing too much message text can
    slow an application down a lot (too much work for terminal
    emulators), and doesn't actually help the user in any way.

    '''

    def __init__(self, period=None, _terminal=None):
        self._period = 1.0 if period is None else period

        self._enabled = True

        self._cached_message = None  # The latest message from caller.
        self._displayed_message = None  # The latest message displayed.
        self._previous_write_at = 0  # When the latest message was written.

        self._terminal = _terminal or ttystatus.PhysicalTerminal()
        try:
            self._terminal.open_tty()
        except IOError:
            self._enabled = False

        if not self._terminal.has_capabilities():
            self._enabled = False

        self._area = ttystatus.AreaManager()
        self._area.set_terminal(self._terminal)

    def disable(self):
        '''Disable all output except notifications.'''
        self._enabled = False

    def enable(self):
        '''Enable output to happen.'''
        self._enabled = True

    def time_to_write(self):
        '''Is it time to write now?'''
        return self._now() - self._previous_write_at >= self._period

    def _now(self):
        '''Return current time.'''
        # This is a wrapper around time.time(), for testing.
        return time.time()

    def get_max_line_length(self):
        return self._area.get_max_line_length()

    def write(self, message):
        '''Write message to terminal.

        Message may be multiple lines.

        '''

        if self._enabled and self.time_to_write():
            self.clear()
            num_lines = len(message.split('\n'))
            self._area.make_space(num_lines)
            self._area.display(message)
            self._displayed_message = message
            self._previous_write_at = self._now()
        self._cached_message = message

    def clear(self):
        '''Remove currently displayed message from terminal, if any.'''

        if self._displayed_message is not None:
            num_lines = len(self._displayed_message.split('\n'))
            self._area.clear_area(num_lines)
            self._displayed_message = None
            self._cached_message = None
            self._previous_write_at = 0  # Next .write() should display.

    def notify(self, message, f, force=False):
        '''Show a notification message string to the user.

        Notifications are meant for error messages and other things
        that do not belong in, say, progress bars. Whatever is currently
        on the terminal is wiped, then the notification message is shown,
        a new line is started, and the old message is restored.

        Notifications are written even when the output is not going
        to a terminal.

        '''

        if self._enabled or force:
            self.clear()
            try:
                f.write(message)
                f.write('\n')
                f.flush()
            except IOError:
                # We ignore these. No point in crashing if terminal is bad.
                pass
            if self._cached_message is not None:
                self.write(self._cached_message)

    def finish(self):
        '''Finalize output.'''
        if self._enabled and self._cached_message is not None:
            self.write(self._cached_message)
            self._terminal.write('\n')
