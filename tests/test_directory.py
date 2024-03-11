"""
Tests traversing and rendering templates in a
directory tree.
"""
# pylint: disable=missing-function-docstring
import os
from shutil import copytree
from tempfile import TemporaryDirectory
from j2tmpl import cli

TEST_TEMPLATE_PATH = os.path.join(os.getcwd(), "tests", "templates")

# pylint: disable=unused-argument
def assert_comparisons(tmpdir, tmpdestdir, comparisons):
    for srcpath, destpath in comparisons:
        with open(srcpath, encoding="utf-8") as src, open(destpath, encoding="utf-8") as dest:
            assert src.read() == dest.read()


def render_directory(srcdir, dstdir, context, directory, recursive=False):
    templatedir = os.path.join(TEST_TEMPLATE_PATH, directory, "templates")
    rendereddir = os.path.join(TEST_TEMPLATE_PATH, directory, "rendered")

    os.rmdir(srcdir)
    copytree(templatedir, srcdir)

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
    with TemporaryDirectory(suffix="source") as tmpdir:
        with TemporaryDirectory(suffix="dest") as tmpdestdir:
            simple_directory(tmpdir, tmpdestdir, common_environment)


def test_simple_directory_inplace(common_environment):
    with TemporaryDirectory() as tmpdir:
        simple_directory(tmpdir, tmpdir, common_environment)


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
    with TemporaryDirectory(suffix="source") as tmpdir:
        with TemporaryDirectory(suffix="dest") as tmpdestdir:
            simple_directory_recursive(tmpdir, tmpdestdir, common_environment)


def test_simple_directory_recursive_inplace(common_environment):
    with TemporaryDirectory() as tmpdir:
        simple_directory_recursive(tmpdir, tmpdir, common_environment)


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
    with TemporaryDirectory(suffix="source") as tmpdir:
        with TemporaryDirectory(suffix="dest") as tmpdestdir:
            fragment_directory(tmpdir, tmpdestdir, common_environment)


def test_fragment_directory_inplace(common_environment):
    with TemporaryDirectory() as tmpdir:
        fragment_directory(tmpdir, tmpdir, common_environment)


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
    with TemporaryDirectory(suffix="source") as tmpdir:
        with TemporaryDirectory(suffix="dest") as tmpdestdir:
            fragment_directory_recursive(tmpdir, tmpdestdir, common_environment)


def test_fragment_directory_recursive_inplace(common_environment):
    with TemporaryDirectory() as tmpdir:
        fragment_directory_recursive(tmpdir, tmpdir, common_environment)
