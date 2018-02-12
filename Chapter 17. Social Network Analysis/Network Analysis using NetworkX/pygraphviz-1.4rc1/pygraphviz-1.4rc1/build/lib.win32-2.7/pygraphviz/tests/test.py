#!/usr/bin/env python
import sys
from os import path,getcwd

def run(verbosity=1,doctest=False,numpy=True):
    """Run PyGraphviz tests.

    Parameters
    ----------
    verbosity: integer, optional
      Level of detail in test reports.  Higher numbers provide  more detail.

    doctest: bool, optional
      True to run doctests in code modules
    """
    try:
        import nose
    except ImportError:
        raise ImportError(\
            "The nose package is needed to run the tests.")

    sys.stderr.write("Running PyGraphiz tests:")
    nx_install_dir=path.join(path.dirname(__file__), path.pardir)
    # stop if running from source directory
    if getcwd() == path.abspath(path.join(nx_install_dir,path.pardir)):
        raise RuntimeError("Can't run tests from source directory.\n"
                           "Run 'nosetests' from the command line.")

    argv=[' ','--verbosity=%d'%verbosity,
          '-w',nx_install_dir,
          '-exe']
    if doctest:
        argv.extend(['--with-doctest','--doctest-extension=txt'])
    nose.run(argv=argv)

if __name__=="__main__":
    run()

