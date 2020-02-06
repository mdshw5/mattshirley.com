# Compiling matplotlib with custom freetype and png libraries

When developing software and pipelines on my personal laptop I have no trouble
installing any development libraries I may need - they're just a "sudo" away.

However, when I'm running what I've developed on a shared cluster where I have
no admin privileges and don't want to bug the sysadmin (my boss) too much, I
tend to install things in my home directory. This works well for most software,
but one common annoyance is the matplotlib Python module.

## Dependency hell

Matplotlib requires the development versions of both freetype2 and libpng. These
compile and install in a custom prefix (for me `/home/matt/.local`) cleanly,
however the include path is difficult to pass to the matplotlib
setupext.py script. One easier way to make matplotlib aware of these dependencies
is to create pkg-config definitions for our custom development library installs:

<script src="https://gist.github.com/mdshw5/9812062.js"></script>

Simply place these files in `/home/matt/.local` and
`export PKG_CONFIG_PATH=/home/matt/.local` and `python setup.py install--user`
and you're ready to go.
