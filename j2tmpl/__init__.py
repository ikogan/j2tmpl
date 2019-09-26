from j2tmpl.cli import main, __doc__  # noqa: F401


def entrypoint():
    import sys

    main(sys.argv[1:])
