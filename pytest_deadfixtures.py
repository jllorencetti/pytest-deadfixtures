"""
Some functions are basically copy n' paste version of code already in pytest.
Precisely the get_fixtures, get_used_fixturesdefs and write_docstring functions.
"""

from collections import namedtuple
from itertools import combinations
from textwrap import dedent

import _pytest.config
import py
from _pytest.compat import getlocation

DUPLICATE_FIXTURES_HEADLINE = "\n\nYou may have some duplicate fixtures:"
UNUSED_FIXTURES_FOUND_HEADLINE = (
    "Hey there, I believe the following {count} fixture(s) are not being used:"
)
UNUSED_FIXTURES_NOT_FOUND_HEADLINE = "Cool, every declared fixture is being used."

IGNORED_FIXTURES_HEADLINE = "Ignored fixture(s) {count}:"
IGNORED_FIXTURES_ATTR = "_deadfixtures_ignore"

EXIT_CODE_ERROR = 11
EXIT_CODE_SUCCESS = 0

AvailableFixture = namedtuple("AvailableFixture", "relpath, argname, fixturedef")

CachedFixture = namedtuple("CachedFixture", "fixturedef, relpath, result")


def pytest_addoption(parser):
    group = parser.getgroup("deadfixtures")
    group.addoption(
        "--dead-fixtures",
        action="store_true",
        dest="deadfixtures",
        default=False,
        help="Show fixtures not being used",
    )
    group.addoption(
        "--dup-fixtures",
        action="store_true",
        dest="showrepeated",
        default=False,
        help="Show duplicated fixtures",
    )
    group.addoption(
        "--show-ignored-fixtures",
        action="store_true",
        default=False,
        help="Show fixtures ignored with `deadfixtures_ignore` mark",
    )


def pytest_cmdline_main(config):
    if config.option.deadfixtures:
        config.option.show_fixture_doc = config.option.verbose
        config.option.verbose = -1
        if _show_dead_fixtures(config):
            return EXIT_CODE_ERROR
        return EXIT_CODE_SUCCESS


def _show_dead_fixtures(config):
    from _pytest.main import wrap_session

    return wrap_session(config, show_dead_fixtures)


def get_best_relpath(func, curdir):
    loc = getlocation(func, curdir)
    return curdir.bestrelpath(loc)


def deadfixtures_ignore(func):
    """Decorator to mark fixtures that should be ignored by the plugin."""
    setattr(func, IGNORED_FIXTURES_ATTR, True)
    return func


def is_ignored_fixture(fixturedef):
    """Check if a fixture is marked as ignored."""
    return getattr(fixturedef.func, IGNORED_FIXTURES_ATTR, False)


def get_fixtures(session):
    available = []
    seen = set()
    fm = session._fixturemanager
    curdir = py.path.local()

    for fixturedefs in fm._arg2fixturedefs.values():
        assert fixturedefs is not None
        if not fixturedefs:
            continue
        for fixturedef in fixturedefs:
            loc = getlocation(fixturedef.func, curdir)
            if (fixturedef.argname, loc) in seen:
                continue

            seen.add((fixturedef.argname, loc))

            module = fixturedef.func.__module__

            if (
                not module.startswith("_pytest.")
                and not module.startswith("pytest_")
                and "site-packages" not in loc
                and "dist-packages" not in loc
                and "<string>" not in loc
            ):
                available.append(
                    AvailableFixture(
                        curdir.bestrelpath(loc), fixturedef.argname, fixturedef
                    )
                )

    available.sort(key=lambda a: a.relpath)
    return available


def get_used_fixturesdefs(session):
    fixturesdefs = []
    for test_function in session.items:
        try:
            info = test_function._fixtureinfo
        except AttributeError:
            # doctests items have no _fixtureinfo attribute
            continue
        if not info.name2fixturedefs:
            # this test item does not use any fixtures
            continue

        for _, fixturedefs in sorted(info.name2fixturedefs.items()):
            if fixturedefs is None:
                continue
            fixturesdefs.append(fixturedefs[-1])
    return fixturesdefs


def get_parametrized_fixtures(session, available_fixtures):
    params_values = []
    for test_function in session.items:
        try:
            for v in test_function.callspec.params.values():
                params_values.append(v)
        except AttributeError:
            continue
    return [
        available.fixturedef
        for available in filter(
            lambda x: x.fixturedef.argname in params_values, available_fixtures
        )
    ]


def write_docstring(tw, doc):
    INDENT = "    "
    doc = doc.rstrip()
    if "\n" in doc:
        firstline, rest = doc.split("\n", 1)
    else:
        firstline, rest = doc, ""

    if firstline.strip():
        tw.line(INDENT + firstline.strip())

    if rest:
        for line in dedent(rest).split("\n"):
            tw.write(INDENT + line + "\n")


def write_fixtures(tw, fixtures, write_docs):
    for fixture in fixtures:
        tplt = "Fixture name: {}, location: {}"
        tw.line(tplt.format(fixture.argname, fixture.relpath))
        doc = fixture.fixturedef.func.__doc__ or ""
        if write_docs and doc:
            write_docstring(tw, doc)


cached_fixtures = []


def pytest_fixture_post_finalizer(fixturedef):
    if getattr(fixturedef, "cached_result", None):
        curdir = py.path.local()
        loc = getlocation(fixturedef.func, curdir)

        cached_fixtures.append(
            CachedFixture(
                fixturedef, curdir.bestrelpath(loc), fixturedef.cached_result[0]
            )
        )


def same_fixture(one, two):
    def result_same_type(a, b):
        return isinstance(a.result, type(b.result))

    def same_result(a, b):
        if not a.result or not b.result:
            return False
        if hasattr(a.result, "__dict__") or hasattr(b.result, "__dict__"):
            return a.result.__dict__ == b.result.__dict__
        return a.result == b.result

    def same_loc(a, b):
        return a.relpath == b.relpath

    return (
        result_same_type(one, two) and same_result(one, two) and not same_loc(one, two)
    )


def pytest_sessionfinish(session, exitstatus):
    if exitstatus or not session.config.getvalue("showrepeated"):
        return exitstatus

    tw = _pytest.config.create_terminal_writer(session.config)

    duplicated_fixtures = []
    for a, b in combinations(cached_fixtures, 2):
        if same_fixture(a, b):
            duplicated_fixtures.append((a, b))

    if duplicated_fixtures:
        tw.line(DUPLICATE_FIXTURES_HEADLINE, red=True)
        msg = "Fixture name: {}, location: {}"
        for a, b in duplicated_fixtures:
            tw.line(msg.format(a.fixturedef.argname, a.relpath))
            tw.line(msg.format(b.fixturedef.argname, b.relpath))


def show_dead_fixtures(config, session):
    session.perform_collect()
    tw = _pytest.config.create_terminal_writer(config)
    show_fixture_doc = config.getvalue("show_fixture_doc")
    show_ignored = config.getvalue("show_ignored_fixtures")

    used_fixtures = get_used_fixturesdefs(session)
    available_fixtures = get_fixtures(session)
    param_fixtures = get_parametrized_fixtures(session, available_fixtures)

    # Separate ignored and unused fixtures
    ignored_fixtures = [
        fixture
        for fixture in available_fixtures
        if is_ignored_fixture(fixture.fixturedef)
    ]

    unused_fixtures = [
        fixture
        for fixture in available_fixtures
        if fixture.fixturedef not in used_fixtures
        and fixture.fixturedef not in param_fixtures
        and not is_ignored_fixture(fixture.fixturedef)
    ]

    tw.line()
    if unused_fixtures:
        tw.line(
            UNUSED_FIXTURES_FOUND_HEADLINE.format(count=len(unused_fixtures)), red=True
        )
        write_fixtures(tw, unused_fixtures, show_fixture_doc)
    else:
        tw.line(UNUSED_FIXTURES_NOT_FOUND_HEADLINE, green=True)

    # Show ignored fixtures if requested
    if show_ignored and ignored_fixtures:
        tw.line()
        tw.line(
            IGNORED_FIXTURES_HEADLINE.format(count=len(ignored_fixtures)), yellow=True
        )
        write_fixtures(tw, ignored_fixtures, show_fixture_doc)

    return unused_fixtures
