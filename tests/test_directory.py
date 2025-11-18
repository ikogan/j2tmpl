import os
import shutil
from j2tmpl import cli

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from tempfile import mkdtemp

    # Note, taken from Python 3's implementation
    # but simplified for just this use.
    class TemporaryDirectory:
        def __init__(self):
            self.name = mkdtemp()

        def __enter__(self):
            return self.name

        def __exit__(self, exc, value, tb):
            self.cleanup()

        def __del__(self):
            self.cleanup()

        def cleanup(self):
            shutil.rmtree(self.name)

TEST_TEMPLATE_PATH = os.path.join(os.getcwd(), "tests", "templates")


def assert_comparisons(tmpdir, tmpdestdir, comparisons):
    for srcpath, destpath in comparisons:
        with open(srcpath) as src, open(destpath) as dest:
            assert src.read() == dest.read()


def render_directory(srcdir, dstdir, context, directory, recursive=False):
    templatedir = os.path.join(TEST_TEMPLATE_PATH, directory, "templates")
    rendereddir = os.path.join(TEST_TEMPLATE_PATH, directory, "rendered")

    shutil.copytree(templatedir, srcdir, dirs_exist_ok=True)

    if recursive:
        args = cli.parse_arguments(['-r', '-o', srcdir, dstdir])
    else:
        args = cli.parse_arguments(['-o', srcdir, dstdir])

    cli.render(srcdir, dstdir,
               cli.build_template_context(context),
               args)

    return templatedir, rendereddir


def simple_directory(srcdir, dstdir, context):
    templatedir, rendereddir = render_directory(srcdir, dstdir, context, "simple-directory")

    assert_comparisons(srcdir, dstdir, [
        [os.path.join(templatedir, "test.conf.jinja"),
            os.path.join(srcdir, "test.conf.jinja")],
        [os.path.join(templatedir, "simple-subdirectory", "test.sub.jinja"),
         os.path.join(srcdir, "simple-subdirectory", "test.sub.jinja")],
        [os.path.join(rendereddir, "test.conf"), os.path.join(dstdir, "test.conf")]
    ])
    assert not os.path.exists(os.path.join(dstdir, "simple-subdirectory", "test.sub"))


def test_simple_directory(common_environment):
    tmpdir = TemporaryDirectory()
    tmpdestdir = TemporaryDirectory()

    simple_directory(tmpdir.name, tmpdestdir.name, common_environment)


def test_simple_directory_inplace(common_environment):
    tmpdir = TemporaryDirectory()

    simple_directory(tmpdir.name, tmpdir.name, common_environment)


def simple_directory_recursive(srcdir, dstdir, context):
    templatedir, rendereddir = render_directory(srcdir, dstdir, context, "simple-directory", recursive=True)

    assert_comparisons(srcdir, dstdir, [
        [os.path.join(templatedir, "test.conf.jinja"),
            os.path.join(srcdir, "test.conf.jinja")],
        [os.path.join(templatedir, "simple-subdirectory", "test.sub.jinja"),
         os.path.join(srcdir, "simple-subdirectory", "test.sub.jinja")],
        [os.path.join(rendereddir, "test.conf"), os.path.join(dstdir, "test.conf")],
        [os.path.join(rendereddir, "simple-subdirectory", "test.sub"),
         os.path.join(dstdir, "simple-subdirectory", "test.sub"), ],
    ])


def test_simple_directory_recursive(common_environment):
    tmpdir = TemporaryDirectory()
    tmpdestdir = TemporaryDirectory()

    simple_directory_recursive(tmpdir.name, tmpdestdir.name, common_environment)


def test_simple_directory_recursive_inplace(common_environment):
    tmpdir = TemporaryDirectory()

    simple_directory_recursive(tmpdir.name, tmpdir.name, common_environment)


def fragment_directory(srcdir, dstdir, context):
    templatedir, rendereddir = render_directory(srcdir, dstdir, context, "fragment-directory")

    assert_comparisons(srcdir, dstdir, [
        [os.path.join(templatedir, "test.conf.jinja"),
         os.path.join(srcdir, "test.conf.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub.conf.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub.conf.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub2.conf.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub2.conf.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment2.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment2.jinja")],
        [os.path.join(templatedir, "test.conf.jinja.d", "fragment.jinja"),
         os.path.join(srcdir, "test.conf.jinja.d", "fragment.jinja")],
        [os.path.join(templatedir, "test.conf.jinja.d", "fragment2.conf.jinja"),
         os.path.join(srcdir, "test.conf.jinja.d", "fragment2.conf.jinja")],
        [os.path.join(templatedir, "nobase.conf.jinja.d", "nobase.conf.jinja"),
         os.path.join(srcdir, "nobase.conf.jinja.d", "nobase.conf.jinja")],
        [os.path.join(rendereddir, "test.conf"), os.path.join(dstdir, "test.conf")],
        [os.path.join(rendereddir, "test2.conf"), os.path.join(dstdir, "test2.conf")],
        [os.path.join(rendereddir, "nobase.conf"), os.path.join(dstdir, "nobase.conf")]
    ])
    assert not os.path.exists(os.path.join(dstdir, "fragment-subdirectory", "sub.conf"))
    assert not os.path.exists(os.path.join(dstdir, "fragment-subdirectory", "sub2.conf"))


def test_fragment_directory(common_environment):
    tmpdir = TemporaryDirectory()
    tmpdestdir = TemporaryDirectory()

    fragment_directory(tmpdir.name, tmpdestdir.name, common_environment)


def test_fragment_directory_inplace(common_environment):
    tmpdir = TemporaryDirectory()

    fragment_directory(tmpdir.name, tmpdir.name, common_environment)


def fragment_directory_recursive(srcdir, dstdir, context):
    templatedir, rendereddir = render_directory(srcdir, dstdir, context, "fragment-directory", recursive=True)

    assert_comparisons(srcdir, dstdir, [
        [os.path.join(templatedir, "test.conf.jinja"),
         os.path.join(srcdir, "test.conf.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub.conf.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub.conf.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub2.conf.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub2.conf.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment.jinja")],
        [os.path.join(templatedir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment2.jinja"),
         os.path.join(srcdir, "fragment-subdirectory", "sub.conf.jinja.d", "subfragment2.jinja")],
        [os.path.join(templatedir, "test.conf.jinja.d", "fragment.jinja"),
         os.path.join(srcdir, "test.conf.jinja.d", "fragment.jinja")],
        [os.path.join(templatedir, "test.conf.jinja.d", "fragment2.conf.jinja"),
         os.path.join(srcdir, "test.conf.jinja.d", "fragment2.conf.jinja")],
        [os.path.join(templatedir, "nobase.conf.jinja.d", "nobase.conf.jinja"),
         os.path.join(srcdir, "nobase.conf.jinja.d", "nobase.conf.jinja")],
        [os.path.join(rendereddir, "test.conf"), os.path.join(dstdir, "test.conf")],
        [os.path.join(rendereddir, "test2.conf"), os.path.join(dstdir, "test2.conf")],
        [os.path.join(rendereddir, "nobase.conf"), os.path.join(dstdir, "nobase.conf")],
        [os.path.join(rendereddir, "fragment-subdirectory", "sub.conf"),
         os.path.join(dstdir, "fragment-subdirectory", "sub.conf")],
        [os.path.join(rendereddir, "fragment-subdirectory", "sub2.conf"),
         os.path.join(dstdir, "fragment-subdirectory", "sub2.conf")],
    ])


def test_fragment_directory_recursive(common_environment):
    tmpdir = TemporaryDirectory()
    tmpdestdir = TemporaryDirectory()

    fragment_directory_recursive(tmpdir.name, tmpdestdir.name, common_environment)


def test_fragment_directory_recursive_inplace(common_environment):
    tmpdir = TemporaryDirectory()

    fragment_directory_recursive(tmpdir.name, tmpdir.name, common_environment)
