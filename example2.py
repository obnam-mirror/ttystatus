# Copyright 2015  Lars Wirzenius
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


'''An example program for ttystatus: compute checksums.'''


import hashlib
import os
import sys

import ttystatus


num_bytes = 1024**2


def main():
    ts = ttystatus.TerminalStatus(period=0.1)

    ts.format(
        'Elapsed time: %ElapsedTime()\n'
        'Current file: %Pathname(filename)\n'
        'File count: %Counter(filename)\n'
        'Combined size: %ByteSize(bytes-read)\n'
        'Checksum speed: %ByteSpeed(bytes-read)'
    )
    ts['bytes-read'] = 0

    for dirname, subdirs, basenames in os.walk(sys.argv[1]):
        for basename in basenames:
            filename = os.path.join(dirname, basename)
            if os.path.isfile(filename):
                ts['filename'] = filename
                checksum = hashlib.sha512()
                with open(filename, 'rb') as f:
                    data = f.read(num_bytes)
                    checksum.update(data)
                    ts['bytes-read'] += len(data)
                if checksum.hexdigest().startswith('0'):
                    ts.notify('%s %s' % (checksum.hexdigest(), filename))
        
    ts.finish()


if __name__ == '__main__':
    main()
