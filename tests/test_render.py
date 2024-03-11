'''
Test rendering templates and various filters.
'''
# pylint: disable=missing-function-docstring
import os

from tempfile import NamedTemporaryFile

import pytest

from jinja2.exceptions import TemplateSyntaxError
from j2tmpl import cli

TEST_TEMPLATE_PATH = os.path.join(os.getcwd(), "tests", "templates")


def test_simple_template(common_environment, common_rendered):
    # The tmp_path fixture is not relaible across Python versions.
    # Do this ourselves.
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, "simple.jinja")
        cli.render(template_file, tmpfile.name,
                cli.build_template_context(common_environment),
                cli.parse_arguments(['-o', tmpfile.name, template_file]))

        with open(tmpfile.name, encoding="utf-8") as output:
            assert output.read().strip() == common_rendered



def test_include(common_environment, common_rendered):
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, "include.jinja")
        cli.render(template_file, tmpfile.name,
                cli.build_template_context(common_environment),
                cli.parse_arguments(['-o', tmpfile.name,
                                        '-b', os.path.join(
                                            os.path.dirname(__file__), 'templates'),
                                        template_file]))

        with open(tmpfile.name, encoding="utf-8") as output:
            assert output.read().strip() == "top\n" + common_rendered


def test_extensions(common_environment):
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, "extensions.jinja")
        cli.render(template_file, tmpfile.name,
                cli.build_template_context(common_environment),
                cli.parse_arguments(['-o', tmpfile.name, template_file]))


        with open(tmpfile.name, encoding="utf-8") as output:
            assert output.read() == "en_US.UTF-8"


def test_filter_readfile(common_environment):
    with NamedTemporaryFile() as tmpfile:
        test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    'templates', 'test.data')
        context = cli.build_template_context(dict(common_environment,
                                                TEST_DATA_PATH=test_data_path))
        template_file = os.path.join(TEST_TEMPLATE_PATH, os.path.join("filters", "readfile.jinja"))

        cli.render(template_file, tmpfile.name, context,
                cli.parse_arguments(['-o', tmpfile.name, template_file]))

        with open(tmpfile.name, encoding="utf-8") as output:
            assert output.read() == "TEST DATA\n"


def test_filter_boolean(common_environment):
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, os.path.join("filters", "boolean.jinja"))

        cli.render(template_file, tmpfile.name,
                cli.build_template_context(common_environment),
                cli.parse_arguments(['-o', tmpfile.name, template_file]))

        with open(tmpfile.name, encoding="utf-8") as output:
            lines = output.readlines()

            for num, line in enumerate(lines, start=1):
                assert len(line) == 0 or line.strip() == 'cool', f"test {num} should have been truthy"


def test_filter_base64(common_environment):
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, os.path.join("filters", "base64.jinja"))

        cli.render(template_file, tmpfile.name,
                cli.build_template_context(common_environment),
                cli.parse_arguments(['-o', tmpfile.name, template_file]))

        with open(tmpfile.name, encoding="utf-8") as output:
            assert output.read().strip() == """CAMEL_CASE_VARIABLE_ENCODED=aGFuZGxldGhpc3Rvbw==
CAMEL_CASE_VARIABLE_DECODED=handlethistoo
CAMEL_CASE_VARIABLE=handlethistoo
UNDEFINED_VARIABLE="""


def test_undefined(common_environment):
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, "undefined.jinja")
        cli.render(template_file, tmpfile.name,
                cli.build_template_context(common_environment),
                cli.parse_arguments(['-o', tmpfile.name, template_file]))

        with open(tmpfile.name, encoding="utf-8") as output:
            assert """7
term -> program -> foo(X)
term -> foo(X) -> bar
foo(X) -> bar -> baz



term -> foo is not defined
term -> foo -> bar is not defined""" == output.read()


def test_error(common_environment, capsys):
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, "error.jinja")

        with pytest.raises(TemplateSyntaxError):
            cli.render(template_file, tmpfile.name,
                    cli.build_template_context(common_environment),
                    cli.parse_arguments(['-o', tmpfile.name, template_file]))

        captured = capsys.readouterr()
        assert "error.jinja" in captured.err
        assert " 9: >>" in captured.err


def test_single_line_error(common_environment, capsys):
    with NamedTemporaryFile() as tmpfile:
        template_file = os.path.join(TEST_TEMPLATE_PATH, "single-line-error.jinja")

        with pytest.raises(TemplateSyntaxError):
            cli.render(template_file, tmpfile.name,
                    cli.build_template_context(common_environment),
                    cli.parse_arguments(['-o', tmpfile.name, template_file]))

        captured = capsys.readouterr()
        assert "error.jinja" in captured.err
        assert "1: >>" in captured.err
        assert 3 == len(captured.err.split('\n'))
