from j2tmpl import cli

import pytest


def test_parse_simple(simple_list):
    assert len(simple_list.keys()) == 3
    assert simple_list['a'] == 1
    assert simple_list['b'] == 2
    assert simple_list['c'] == 3


def test_parse_object(simple_object):
    assert len(simple_object.keys()) == 1
    assert 'two' in simple_object['one'].keys()
    assert 'three' in simple_object['one']['two'].keys()
    assert simple_object['one']['two']['three'] == 4


def test_single_underscore(single_underscore):
    assert len(single_underscore.keys()) == 1
    assert single_underscore['_'] == 'underscore'


def test_many_underscores(many_underscores):
    assert len(many_underscores.keys()) == 1
    assert many_underscores['_']['test']['variable']['seven']['_'] == 'weee'


def test_duplicate_keys_error():
    with pytest.raises(ValueError) as excinfo:
        cli.build_template_context({
            'ONE_TWO_THREE': 'one',
            'ONE_TWO': 'two',
            'oneTwoThree': 'failure'
        })

    assert 'ONE_TWO is defined multiple times' in str(excinfo.value)
