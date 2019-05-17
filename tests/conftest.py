# flake8: noqa E501
import pytest

from j2tmpl import cli


@pytest.fixture(scope="module")
def simple_list():
    '''
    Simple set of 3 one level environment variables.
    '''
    return cli.build_template_context({'A': 1, 'B': 2, 'C': 3})


@pytest.fixture(scope="module")
def simple_object():
    '''
    A single 3 level environment variable.
    '''
    return cli.build_template_context({'ONE_TWO_THREE': 4})


@pytest.fixture(scope="module")
def single_underscore():
    '''
    An environment with a single underscore variable.
    '''
    return cli.build_template_context({'_': 'underscore'})


@pytest.fixture(scope="module")
def many_underscores():
    '''
    An environment with a single variable with lots of
    underscores.
    '''
    return cli.build_template_context({'__TEST_VARIABLE__SEVEN__': 'weee'})


@pytest.fixture(scope="module")
def common_environment():
    '''
    A more common and complex environment with a variety of objects.
    '''
    return {
        'LANG': 'en_US.UTF-8',
        'TERM': 'xterm-256color',
        'SHELL': '/bin/bash',
        'SHLVL': '2',
        'GCC_COLORS': 'error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01',
        '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0',
        'XPC_FLAGS': '0x0',
        'MANPATH': '/usr/local/share/man:/usr/share/man:/Library/Frameworks/Mono.framework/Versions/Current/share/man:/Library/Developer/CommandLineTools/SDKs/MacOSX10.14.sdk/usr/share/man:/Library/Developer/CommandLineTools/usr/share/man',
        'PATH': '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/share/dotnet:~/.dotnet/tools:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/Applications/Wireshark.app/Contents/MacOS',
        'XPC_SERVICE_NAME': '0',
        'TMPDIR': '/var/folders/c8/q3fbdycd000gn/T/',
        'EDITOR': 'vim',
        'camelCaseVariable': 'handlethistoo',
        'JAVA_camelCaseVariable': 'thisshouldbefun'}
