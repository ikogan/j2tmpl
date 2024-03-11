'''
Init shim for pyinstaller to launch j2tmpl
'''
from j2tmpl.cli import main, __doc__  # noqa: F401


def entrypoint():
    '''
    Pyinstaller entrypoint
    '''
    import sys # pylint: disable=import-outside-toplevel

    main(sys.argv[1:])
