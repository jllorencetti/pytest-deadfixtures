from collections import namedtuple

import _pytest.config
import py
from _pytest.compat import getlocation
from _pytest.python import write_docstring

AvailableFixture = namedtuple(
    'AvailableFixture',
    'relpath, argname, fixturedef'
)


def pytest_addoption(parser):
    group = parser.getgroup('deadfixtures')
    group.addoption(
        '--dead-fixtures',
        action='store_true',
        dest='deadfixtures',
        default=False,
        help='Show fixtures not being used'
    )


def pytest_cmdline_main(config):
    if config.option.deadfixtures:
        _show_dead_fixtures(config)
        return 0


def _show_dead_fixtures(config):
    from _pytest.main import wrap_session
    return wrap_session(config, show_dead_fixtures)


def get_best_relpath(func, curdir):
    loc = getlocation(func, curdir)
    return curdir.bestrelpath(loc)


def get_fixtures(session):
    available = []
    seen = set()
    fm = session._fixturemanager
    curdir = py.path.local()

    for argname, fixturedefs in fm._arg2fixturedefs.items():
        assert fixturedefs is not None
        if not fixturedefs:
            continue
        for fixturedef in fixturedefs:
            loc = getlocation(fixturedef.func, curdir)
            if (fixturedef.argname, loc) in seen:
                continue
            seen.add((fixturedef.argname, loc))

            module = fixturedef.func.__module__
            if not module.startswith("_pytest.") \
                    and not module.startswith("pytest_"):
                available.append(AvailableFixture(
                    curdir.bestrelpath(loc),
                    fixturedef.argname,
                    fixturedef
                ))

    available.sort()
    return available


def get_used_fixturesdefs(session):
    fixturesdefs = []
    for test_function in session.items:
        try:
            info = test_function._fixtureinfo
        except AttributeError:
            # doctests items have no _fixtureinfo attribute
            return fixturesdefs
        if not info.name2fixturedefs:
            # this test item does not use any fixtures
            return fixturesdefs

        for _, fixturedefs in sorted(info.name2fixturedefs.items()):
            if fixturedefs is None:
                continue
            fixturesdefs.append(fixturedefs[-1])
    return fixturesdefs


def write_fixtures(tw, fixtures):
    for fixture in fixtures:
        tplt = 'Fixture name: {}, location: {}'
        tw.line(tplt.format(fixture.argname, fixture.relpath), green=True)
        doc = fixture.fixturedef.func.__doc__ or ''
        if doc:
            write_docstring(tw, doc)


def show_dead_fixtures(config, session):
    session.perform_collect()
    tw = _pytest.config.create_terminal_writer(config)

    used_fixtures = get_used_fixturesdefs(session)
    available_fixtures = get_fixtures(session)

    unused_fixtures = [fixture for fixture in available_fixtures
                       if fixture.fixturedef not in used_fixtures]

    tw.line()
    if unused_fixtures:
        tw.line(
            'Hey there, I believe the following fixture(s) are not being used:',
            red=True
        )
        write_fixtures(tw, unused_fixtures)
    else:
        tw.line('Cool, every declared fixture are being used.', green=True)
