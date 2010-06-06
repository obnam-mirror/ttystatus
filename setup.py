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


from distutils.core import setup

import ttystatus

setup(
    name='ttystatus',
    version=ttystatus.version,
    description='terminal progress bar and status output for command line',
    author='Lars Wirzenius',
    author_email='liw@liw.fi',
#    url='http://liw.fi/ttystatus/',
    packages=['ttystatus'],
)
