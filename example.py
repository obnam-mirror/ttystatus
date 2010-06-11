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


'''An example program for ttystatus.'''


import os
import sys

import ttystatus


def main():
    ts = ttystatus.TerminalStatus(period=0.1)
    ts.add(ttystatus.Literal('Finding symlinks: '))
    ts.add(ttystatus.String('pathname'))

    for dirname, subdirs, basenames in os.walk(sys.argv[1]):
        for pathname in [os.path.join(dirname, x) for x in basenames]:
            ts['pathname'] = pathname
            if os.path.islink(pathname):
                ts.notify('Symlink! %s' % pathname)

    ts.finish()


if __name__ == '__main__':
    main()