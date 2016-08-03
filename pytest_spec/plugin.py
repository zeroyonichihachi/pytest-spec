# -*- coding: utf-8 -*-
"""Module contains command line option definition and logic needed to enable new formatting.

:author: Pawel Chomicki
"""
from .replacer import logstart_replacer, report_replacer
from .formatter import format_in_safe


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--spec',
        action='store_true',
        dest='spec',
        help='Print test result in specification format'
    )

    group.addoption(
        '--spec-docstr',
        action='store_true',
        dest='spec_docstr',
        default=False,
        help='Print test result in specification format with docstring (if it is available)'
    )


def pytest_configure(config):
    if config.option.spec or config.option.spec_docstr:
        import imp
        import _pytest
        _pytest.terminal.TerminalReporter.pytest_runtest_logstart = logstart_replacer
        _pytest.terminal.TerminalReporter.pytest_runtest_logreport = report_replacer
        imp.reload(_pytest)


def pytest_runtest_makereport(__multicall__, item, call):
    """return a :py:class:`_pytest.runner.TestReport` object
    for the given :py:class:`pytest.Item` and
    :py:class:`_pytest.runner.CallInfo`.

    Using this hook to capture and set the docstring to report object.
    """
    if not item.config.option.spec_docstr:
        return

    if not _should_capture(call):
        return

    return _makereport_from_docstring(__multicall__, item)


def _should_capture(call):
    return call.when == 'call' or \
        (call.when == 'setup' and call.excinfo is not None)


def _makereport_from_docstring(__multicall__, item):
    report = __multicall__.execute()

    if item.obj.func_doc:
        report._docstring = _formatted_docstring(item)

    return report


def _formatted_docstring(item):
    """
    Retrieve the docstring of test function and format it:
        * Remove heading & trainling space and CR/LF.
        * Replace fixture name which surrounded with curly bracket with real value.
            * i.e.) 'If "{arg}" is given, "{expect}" should be returned.'
                ->  'If "spam" is given, "spam,spam,spam" should be returned.'
                (arg and expect are the fixtures of target function)

    FIXME:
        Because we can't get the fixture values ('funcargs' is None) when the
        function is skipped by 'pytest.mark.skip', the fixture names are not
        be replaced.
    """
    return format_in_safe(item.obj.func_doc.strip(), **item.funcargs)

