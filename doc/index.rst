`ttystatus` -- a terminal status library
========================================

``ttystatus`` is a Python library for showing progress reporting and status
updates on terminals, for (Unix) command line programs. Output is 
automatically adapted to the width of the terminal: truncated if it does
not fit, and re-sized if the terminal size changes.

Output is provided via widgets. Each widgets formats some data into
a suitable form for output. It gets the data either via its initializer,
or from key/value pairs maintained by the master object. The values are
set by the user. Every time a value is updated, widgets get updated
(although the terminal is only updated every so often to give user time
to actually read the output).


Example
-------

Here's an example program that searches for symlinks in a directory tree::

    import os
    import sys

    import ttystatus

    ts = ttystatus.TerminalStatus(period=0.1)
    ts.add(ttystatus.ElapsedTime())
    ts.add(ttystatus.Literal(' Looking for files: '))
    ts.add(ttystatus.Counter('pathname'))
    ts.add(ttystatus.Literal(' found, currently in '))
    ts.add(ttystatus.Pathname('dirname'))
    
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
        ts['done'] += 1

    ts.finish()

(See also the file ``example.py`` in the source distribution.)

Reference manual
================

.. automodule:: ttystatus
   :members:
   :undoc-members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

