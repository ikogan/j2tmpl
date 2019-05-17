from j2tmpl import cli

import pytest


def test_parse_simple():
    context = cli.build_template_context({'A': 1, 'B': 2, 'C': 3})

    assert len(context.keys()) == 3
    assert context['a'] == 1
    assert context['b'] == 2
    assert context['c'] == 3


def test_parse_object():
    context = cli.build_template_context({'ONE_TWO_THREE': 4})

    assert len(context.keys()) == 1
    assert 'two' in context['one'].keys()
    assert 'three' in context['one']['two'].keys()
    assert context['one']['two']['three'] == 4


def test_single_underscore():
    context = cli.build_template_context({'_': 'underscore'})

    assert len(context.keys()) == 1
    assert context['_'] == 'underscore'

    context = cli.build_template_context({'______': 'underscore'})

    assert len(context.keys()) == 1
    assert context['_'] == 'underscore'


def test_many_underscores():
    context = cli.build_template_context({
        '__TEST_VARIABLE__SEVEN__': 'weee'
    })

    assert len(context.keys()) == 1
    assert context['test']['variable']['seven'] == 'weee'


def test_duplicate_keys_error():
    with pytest.raises(ValueError) as excinfo:
        cli.build_template_context({
            'ONE_TWO_THREE': 'one',
            'ONE_TWO': 'two',
            'oneTwoThree': 'failure'
        })

    assert (
        'oneTwoThree is defined multiple times' in str(excinfo.value) or
        'ONE_TWO_THREE is defined multiple times' in str(excinfo.value)
    )

    # This is a slightly different code path. If the duplication
    # is in the middle of the largest similar key, it's caught in
    # a different place.
    with pytest.raises(ValueError) as excinfo:
        cli.build_template_context({
            'ONE_TWO_THREE': 'one',
            'ONE_TWO': 'two',
            'oneTwo': 'failure'
        })

    assert (
        'oneTwo is defined multiple times' in str(excinfo.value) or
        'ONE_TWO is defined multiple times' in str(excinfo.value)
    )
