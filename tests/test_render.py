import os
from j2tmpl import cli
from argparse import Namespace

TEST_TEMPLATE_PATH = os.path.join(os.getcwd(), "tests", "templates")


def test_simple_template(tmp_path, common_environment):
    output = os.path.join(tmp_path, "unit.output")
    args = Namespace(
        template=os.path.join(TEST_TEMPLATE_PATH, "simple.jinja"),
        output=output,
        encoding='utf-8')

    cli.render(args, raw_context=common_environment)

    output = open(output)
    assert output.read() == """_=whatisthis
LANG=en_US.UTF-8
TERM_PROGRAM=vscode
TERM_PROGRAM_VERSION=7
XPC_FLAGS=0x0
CAMEL_CASE_VARIABLE=handlethistoo
JAVA_camelCaseVariable=thisshouldbefun"""
    output.close()
