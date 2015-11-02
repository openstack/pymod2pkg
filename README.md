#: pymod2pkg

`pymod2pkg` is a simple python module for translating python module names to
corresponding package names which is a common problem in the packaging world.

Note that [rdopkg](https://github.com/redhat-openstack/rdopkg) uses this
module to check whether packages corresponding to `requirements.txt` are
available across distros and more.


## Installation


### from source

If you want to hack `pymod2pkg` or just have the latest version without
waiting for next release, I suggest using the git repo directly a la

    git clone https://github.com/openstack/pymod2pkg
    cd pymod2pkg
    python setup.py develop --user


### from PyPI

For your convenience, `pymod2pkg` is also available from the Cheese
Shop:

    pip install pymod2pkg



## Usage

`module2package` is probably all you need, it accepts a module name to convert
and a linux distribution name as returned by `platform.linux_distribution()[0]`:

    import pymod2pkg
    
    pkg = pymod2pkg.module2package('six', 'Fedora')

There's not much more, really, so RTFS.



## Fixing/extending the map

Currently, only package maps for RPM-based systems are provided, but it'd be
nice to have all the distros covered and it's really easy to do.

See `*_PKG_MAP` and `get_pkg_map`, hack it to your liking and submit review by

    git review


## Running the testsuite

Run tests by:

   python tests.py
