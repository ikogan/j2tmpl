# flake8: noqa E501
import pytest

from j2tmpl import cli


@pytest.fixture(scope="module")
def common_environment():
    '''
    A more common and complex environment with a variety of objects.
    '''
    return {
        'LANG': 'en_US.UTF-8',
        'TERM': 'xterm-256color',
        'TERM_PROGRAM': 'vscode',
        'TERM_PROGRAM_VERSION': '7',
        'SHELL': '/bin/bash',
        'SHLVL': '2',
        '_': 'whatisthis',
        'GCC_COLORS': 'error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01',
        '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0',
        'XPC_FLAGS': '0x0',
        'MANPATH': '/usr/local/share/man:/usr/share/man:/Library/Frameworks/Mono.framework/Versions/Current/share/man:/Library/Developer/CommandLineTools/SDKs/MacOSX10.14.sdk/usr/share/man:/Library/Developer/CommandLineTools/usr/share/man',
        'PATH': '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/share/dotnet:~/.dotnet/tools:/Library/Frameworks/Mono.framework/Versions/Current/Commands:/Applications/Wireshark.app/Contents/MacOS',
        'XPC_SERVICE_NAME': '0',
        'TMPDIR': '/var/folders/c8/q3fbdycd000gn/T/',
        'EDITOR': 'vim',
        'camelCaseVariable': 'handlethistoo',
        'JAVA_camelCaseVariable': 'thisshouldbefun',
        'ITERATION_TEST_2_VALUE': 'second',
        'ITERATION_TEST_1_VALUE': 'first'
    }
