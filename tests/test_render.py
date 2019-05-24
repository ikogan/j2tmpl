import os
from j2tmpl import cli
from tempfile import NamedTemporaryFile

TEST_TEMPLATE_PATH = os.path.join(os.getcwd(), "tests", "templates")


def test_simple_template(common_environment):
    # The tmp_path fixture is not relaible across Python versions.
    # Do this ourselves.
    tmpfile = NamedTemporaryFile()
    templateFile = os.path.join(TEST_TEMPLATE_PATH, "simple.jinja")
    cli.render(templateFile, tmpfile.name,
               cli.build_template_context(common_environment),
               cli.parse_arguments(['-o', tmpfile.name, templateFile]))

    output = open(tmpfile.name)
    assert output.read() == """_=whatisthis
LANG=en_US.UTF-8
TERM_PROGRAM=vscode
TERM_PROGRAM_VERSION=7
XPC_FLAGS=0x0
CAMEL_CASE_VARIABLE=handlethistoo
JAVA_camelCaseVariable=thisshouldbefun"""
    output.close()
    tmpfile.close()


def test_extensions(common_environment):
    tmpfile = NamedTemporaryFile()
    templateFile = os.path.join(TEST_TEMPLATE_PATH, "extensions.jinja")
    cli.render(templateFile, tmpfile.name,
               cli.build_template_context(common_environment),
               cli.parse_arguments(['-o', tmpfile.name, templateFile]))

    output = open(tmpfile.name)
    assert output.read() == "en_US.UTF-8"
    output.close()
    tmpfile.close()


def test_filters(common_environment):
    tmpfile = NamedTemporaryFile()
    test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'templates', 'test.data')
    context = cli.build_template_context(dict(common_environment,
                                              TEST_DATA_PATH=test_data_path))
    templateFile = os.path.join(TEST_TEMPLATE_PATH, "filters.jinja")

    cli.render(templateFile, tmpfile.name, context,
               cli.parse_arguments(['-o', tmpfile.name, templateFile]))

    output = open(tmpfile.name)
    assert output.read() == "TEST DATA"


def test_undefined(common_environment):
    tmpfile = NamedTemporaryFile()
    templateFile = os.path.join(TEST_TEMPLATE_PATH, "undefined.jinja")
    cli.render(templateFile, tmpfile.name,
               cli.build_template_context(common_environment),
               cli.parse_arguments(['-o', tmpfile.name, templateFile]))

    output = open(tmpfile.name)
    assert """7
term -> program -> foo(X)
term -> foo(X) -> bar
foo(X) -> bar -> baz



term -> foo is not defined
term -> foo -> bar is not defined""" == output.read()
