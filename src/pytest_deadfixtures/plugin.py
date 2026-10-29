"""
Some functions are basically copy n' paste version of code already in pytest.
Precisely the get_fixtures, get_used_fixturesdefs and write_docstring functions.
"""

import os.path
from itertools import combinations
from pathlib import Path
from textwrap import dedent
from types import FunctionType
from typing import Any, Iterable, NamedTuple

import _pytest.config
import _pytest.main
import pytest
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


class AvailableFixture(NamedTuple):
    relpath: str
    argname: str
    fixturedef: Any


class CachedFixture(NamedTuple):
    fixturedef: Any
    relpath: str
    result: Any


def pytest_addoption(parser: pytest.Parser) -> None:
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


def pytest_cmdline_main(config: pytest.Config) -> int | None:
    if config.option.deadfixtures:
        config.option.show_fixture_doc = config.option.verbose
        config.option.verbose = -1
        return _show_dead_fixtures(config)
    return None


def _show_dead_fixtures(config: pytest.Config) -> int | pytest.ExitCode:
    return _pytest.main.wrap_session(config, show_dead_fixtures)


def commonpath(path1: Path, path2: Path) -> Path | None:
    """Return the common part shared with the other path, or None if there is
    no common part.

    If one path is relative and one is absolute, returns None.
    """
    try:
        return Path(os.path.commonpath((str(path1), str(path2))))
    except ValueError:
        return None


def bestrelpath(directory: Path, dest: Path) -> str:
    """Return a string which is a relative path from directory to dest such
    that directory/bestrelpath == dest.

    The paths must be either both absolute or both relative.

    If no such path can be determined, returns dest.
    """
    assert isinstance(directory, Path)
    assert isinstance(dest, Path)
    if dest == directory:
        return os.curdir
    # Find the longest common directory.
    base = commonpath(directory, dest)
    # Can be the case on Windows for two absolute paths on different drives.
    # Can be the case for two relative paths without common prefix.
    # Can be the case for a relative path and an absolute path.
    if not base:
        return str(dest)
    reldirectory = directory.relative_to(base)
    reldest = dest.relative_to(base)
    return str(Path(*([os.pardir] * len(reldirectory.parts))).joinpath(*reldest.parts))


def get_best_relpath(func, curdir: Path) -> str:
    loc = getlocation(func, str(curdir))
    return bestrelpath(curdir, Path(loc))


def deadfixtures_ignore(func):
    """Decorator to mark fixtures that should be ignored by the plugin."""
    setattr(func, IGNORED_FIXTURES_ATTR, True)
    return func


def is_ignored_fixture(fixturedef) -> bool:
    """Check if a fixture is marked as ignored."""
    return getattr(fixturedef.func, IGNORED_FIXTURES_ATTR, False)


if pytest.version_tuple < (9, 2, 0):

    def get_all_fixture_defs(session: pytest.Session) -> Iterable[Any]:
        fm = session._fixturemanager
        for fixturedefs in fm._arg2fixturedefs.values():
            yield from fixturedefs
else:

    def get_all_fixture_defs(session: pytest.Session) -> Iterable[Any]:
        fm = session._fixturemanager
        return fm._get_all_fixture_defs()


def get_fixtures(session: pytest.Session) -> list[AvailableFixture]:
    available = []
    seen = set()
    curdir = Path.cwd()

    for fixturedef in get_all_fixture_defs(session):
        loc = getlocation(fixturedef.func, str(curdir))
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
                    bestrelpath(curdir, Path(loc)), fixturedef.argname, fixturedef
                )
            )

    available.sort(key=lambda a: a.relpath)
    return available


def get_used_fixturesdefs(session: pytest.Session):
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


def get_parametrized_fixtures(
    session: pytest.Session, available_fixtures: list[AvailableFixture]
):
    params_values = []
    for test_function in session.items:
        try:
            for v in test_function.callspec.params.values():
                if isinstance(v, str):
                    params_values.append(v)
        except AttributeError:
            continue

    return [
        available.fixturedef
        for available in available_fixtures
        if available.fixturedef.argname in params_values
    ]


def write_docstring(tw, doc: str) -> None:
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


def write_fixtures(tw, fixtures, write_docs: bool) -> None:
    for fixture in fixtures:
        tplt = "Fixture name: {}, location: {}"
        tw.line(tplt.format(fixture.argname, fixture.relpath))
        doc = fixture.fixturedef.func.__doc__ or ""
        if write_docs and doc:
            write_docstring(tw, doc)


cached_fixtures: list[CachedFixture] = []


def pytest_sessionstart(session: pytest.Session) -> None:
    cached_fixtures.clear()


def pytest_fixture_post_finalizer(fixturedef, request):
    if not request.config.getvalue("showrepeated"):
        return

    if getattr(fixturedef, "cached_result", None):
        curdir = Path.cwd()
        loc = getlocation(fixturedef.func, str(curdir))

        cached_fixtures.append(
            CachedFixture(
                fixturedef, bestrelpath(curdir, Path(loc)), fixturedef.cached_result[0]
            )
        )


def same_fixture(one, two) -> bool:
    def result_same_type(a, b):
        return isinstance(a.result, type(b.result))

    def same_result(a, b) -> bool:
        if not a.result or not b.result:
            return False
        if isinstance(a.result, FunctionType):
            return a.result == b.result
        a_result_dict = getattr(a.result, "__dict__", None)
        b_result_dict = getattr(b.result, "__dict__", None)
        if a_result_dict is not None and b_result_dict is not None:
            return a_result_dict == b_result_dict
        return a.result == b.result

    def same_loc(a, b) -> bool:
        return a.relpath == b.relpath

    return result_same_type(one, two) and same_result(one, two) and not same_loc(one, two)


def pytest_sessionfinish(
    session: pytest.Session, exitstatus: int | pytest.ExitCode
) -> None:
    if exitstatus or not session.config.getvalue("showrepeated"):
        return

    tw = _pytest.config.create_terminal_writer(session.config)

    duplicated_fixtures = [
        (a, b) for a, b in combinations(cached_fixtures, 2) if same_fixture(a, b)
    ]

    if duplicated_fixtures:
        tw.line(DUPLICATE_FIXTURES_HEADLINE, red=True)
        msg = "Fixture name: {}, location: {}"
        for a, b in duplicated_fixtures:
            tw.line(msg.format(a.fixturedef.argname, a.relpath))
            tw.line(msg.format(b.fixturedef.argname, b.relpath))


def show_dead_fixtures(
    config: pytest.Config, session: pytest.Session
) -> int | pytest.ExitCode | None:
    session.perform_collect()
    tw = _pytest.config.create_terminal_writer(config)
    show_fixture_doc = config.getvalue("show_fixture_doc")
    show_ignored = config.getvalue("show_ignored_fixtures")

    used_fixtures = get_used_fixturesdefs(session)
    available_fixtures = get_fixtures(session)
    param_fixtures = get_parametrized_fixtures(session, available_fixtures)

    curdir = Path.cwd()

    def _fixture_key(fixturedef):
        return fixturedef.argname, getlocation(fixturedef.func, curdir)

    used_keys = {_fixture_key(fixturedef) for fixturedef in used_fixtures}
    param_keys = {_fixture_key(fixturedef) for fixturedef in param_fixtures}

    # Separate ignored and unused fixtures
    ignored_fixtures = [
        fixture
        for fixture in available_fixtures
        if is_ignored_fixture(fixture.fixturedef)
    ]

    unused_fixtures = [
        fixture
        for fixture in available_fixtures
        if _fixture_key(fixture.fixturedef) not in used_keys
        and _fixture_key(fixture.fixturedef) not in param_keys
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

    if unused_fixtures:
        return EXIT_CODE_ERROR
    else:
        return EXIT_CODE_SUCCESS
