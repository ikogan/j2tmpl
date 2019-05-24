import os
from j2tmpl import cli
from tempfile import TemporaryDirectory
from distutils.dir_util import copy_tree

TEST_TEMPLATE_PATH = os.path.join(os.getcwd(), "tests", "templates")


def assert_comparisons(tmpdir, tmpdestdir, comparisons):
    for srcpath, destpath in comparisons:
        srcpath = os.path.join(tmpdir, srcpath)

        with open(srcpath) as src, open(destpath) as dest:
            assert src.read() == dest.read()


def render_directory(srcdir, dstdir, context, directory, recursive=False):
    templatedir = os.path.join(TEST_TEMPLATE_PATH, directory, "templates")
    rendereddir = os.path.join(TEST_TEMPLATE_PATH, directory, "rendered")

    copy_tree(templatedir, srcdir)

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
        ["test.conf.jinja", os.path.join(srcdir, "test.conf.jinja")],
        [os.path.join("simple-subdirectory", "test.sub.jinja"),
        os.path.join(srcdir, "simple-subdirectory", "test.sub.jinja")],
        ["test.conf", os.path.join(rendereddir, "test.conf")]
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
        ["test.conf.jinja", os.path.join(srcdir, "test.conf.jinja")],
        [os.path.join("simple-subdirectory", "test.sub.jinja"),
         os.path.join(srcdir, "simple-subdirectory", "test.sub.jinja")],
        ["test.conf", os.path.join(rendereddir, "test.conf")],
        [os.path.join("simple-subdirectory", "test.sub"),
         os.path.join(srcdir, "simple-subdirectory", "test.sub")],
    ])


def test_simple_directory_recursive(common_environment):
    tmpdir = TemporaryDirectory()
    tmpdestdir = TemporaryDirectory()

    simple_directory_recursive(tmpdir.name, tmpdestdir.name, common_environment)


def test_simple_directory_recursive_inplace(common_environment):
    tmpdir = TemporaryDirectory()

    simple_directory_recursive(tmpdir.name, tmpdir.name, common_environment)
