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
    ts.format('%ElapsedTime() Looking for files: %Counter(pathname) found, '
              'currently in %Pathname(dirname)')
    
    pathnames = []
    for dirname, subdirs, basenames in os.walk(sys.argv[1]):
        ts['dirname'] = dirname
        for basename in basenames:
            pathname = os.path.join(dirname, basename)
            ts['pathname'] = pathname
            pathnames.append(pathname)
        
    ts.clear()
    ts.add(ttystatus.ElapsedTime())
    ts.add(ttystatus.Literal(' Finding symlinks: '))
    ts.add(ttystatus.Counter('symlink'))
    ts.add(ttystatus.Literal(' found; now at '))
    ts.add(ttystatus.Index('pathname', 'pathnames'))
    ts.add(ttystatus.Literal(' ('))
    ts.add(ttystatus.PercentDone('done', 'total', decimals=2))
    ts.add(ttystatus.Literal(' done) '))
    ts.add(ttystatus.RemainingTime('done', 'total'))
    ts.add(ttystatus.Literal(' '))
    ts.add(ttystatus.ProgressBar('done', 'total'))
    ts['pathnames'] = pathnames
    ts['done'] = 0
    ts['total'] = len(pathnames)

    for pathname in pathnames:
        ts['pathname'] = pathname
        if os.path.islink(pathname):
            ts['symlink'] = pathname
            ts.notify('Symlink! %s' % pathname)
        elif 'error' in pathname:
            ts.error('Error in pathname: %s' % pathname)
        ts['done'] += 1

    ts.finish()


if __name__ == '__main__':
    main()
