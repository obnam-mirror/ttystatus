# Copyright 2011  Lars Wirzenius
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


import inspect
import re

import ttystatus


def _find_widgets():
    names = dir(ttystatus)
    objs = [getattr(ttystatus, x) for x in names]
    classes = [o for o in objs if inspect.isclass(o)]
    widget_classes = [c for c in classes if issubclass(c, ttystatus.Widget)]
    subclasses = [w for w in widget_classes if w != ttystatus.Widget]
    return subclasses

widgets = _find_widgets()


def parse(fmt):
    '''Parse format string.'''

    names = [x.__name__ for x in widgets]
    namespat = '|'.join(names)
    argspat = r'[0-9a-zA-Z,_-]*'
    pat = r'%%(?P<class>%s)\((?P<args>%s)\)' % (namespat, argspat)
    pat = re.compile(pat)

    result = []
    prefix = ''
    while fmt:
        m = pat.match(fmt)
        if m:
            if prefix:
                literal = ttystatus.Literal(prefix)
                literal.interested_in = []
                result.append(literal)
                prefix = ''
            klass = getattr(ttystatus, m.group('class'))
            argnames = m.group('args').split(',')
            argnames = [x for x in argnames if x]
            widget = klass(*argnames)
            widget.interested_in = argnames
            result.append(widget)
            fmt = fmt[m.end():]
        elif fmt.startswith('%%'):
            prefix += '%'
            fmt = fmt[2:]
        else:
            prefix += fmt[0]
            fmt = fmt[1:]

    if prefix:
        literal = ttystatus.Literal(prefix)
        literal.interested_in = []
        result.append(literal)
    return result
