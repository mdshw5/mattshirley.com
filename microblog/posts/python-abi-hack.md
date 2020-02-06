# Properly resolving versioned Python shared object suffixes

So, the other day I was trying to call a C library from a Python script using `ctypes.cdll.LoadLibrary`, 
and the funniest thing happened: *it didn't work properly across multiple Python interpreter versions*. 
At this point I usually turn the the PEP documents, and found this in [PEP3149](https://www.python.org/dev/peps/pep-3149/):

> The following information MUST be included in the shared library file name:
> The Python implementation (e.g. cpython, pypy, jython, etc.)
> The interpreter's major and minor version numbers

So, how do we get this information? The PEP document stops short of telling us. However, I gathered a few 
bits of information along the way to finding out:

1. Python 2.6-3.1 do not implement this, so these version need no special suffix
2. Python >3.1 implements a `.cpython-vv.so` suffix where `vv` is major/minor version number
3. PyPy does something different.

The following code snippet is what I came up with for determining the suffix for the compiled shared library.

```python
import sys

try:
    from sysconfig import get_config_var as get
    # https://mail.gnome.org/archives/commits-list/2013-April/msg05415.html
    # https://www.python.org/dev/peps/pep-3149/
    SUFFIX = get('EXT_SUFFIX') or get('SO') or '.so'
except ImportError:
    SUFFIX = '.so'

# Check for pypy interpreter
if hasattr(sys, 'pypy_version_info'):
    if sys.version_info.major == 2:
        SUFFIX = ".pypy-{0}{1}.so".format(sys.pypy_version_info.major, sys.pypy_version_info.minor)
    elif sys.version_info.major == 3:
        SUFFIX = ".pypy3-{0}{1}.so".format(sys.pypy_version_info.major, sys.pypy_version_info.minor)
```