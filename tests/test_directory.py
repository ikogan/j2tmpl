import os
from j2tmpl import cli
from tempfile import TemporaryDirectory
from distutils.dir_util import copy_tree

TEST_TEMPLATE_PATH = os.path.join(os.getcwd(), "tests", "templates")


def assert_comparisons(tmpdir, comparisons):
    for srcpath, destpath in comparisons:
        srcpath = os.path.join(tmpdir, srcpath)

        with open(srcpath) as src, open(destpath) as dest:
            assert src.read() == dest.read()


def test_simple_directory_inplace(common_environment):
    tmpdir = TemporaryDirectory()
    srcdir = os.path.join(TEST_TEMPLATE_PATH, "simple-directory", "templates")

    copy_tree(srcdir, tmpdir.name)

    args = cli.parse_arguments(['-o', tmpdir.name, tmpdir.name])

    cli.render(tmpdir.name, tmpdir.name,
               cli.build_template_context(common_environment),
               args)

    rendereddir = os.path.join(TEST_TEMPLATE_PATH, "simple-directory", "rendered")

    print(os.listdir(tmpdir.name))

    assert_comparisons(tmpdir.name, [
        ["test.conf.jinja", os.path.join(srcdir, "test.conf.jinja")],
        [os.path.join("simple-subdirectory", "test.sub.jinja"),
            os.path.join(srcdir, "simple-subdirectory", "test.sub.jinja")],
        ["test.conf", os.path.join(rendereddir, "test.conf")],
        [os.path.join("simple-subdirectory", "test.conf"),
            os.path.join(rendereddir, "simple-subdirectory", "test.sub")]
    ])

    tmpdir.close()
