def test_dont_list_autouse_fixture(testdir, message_template):
    testdir.makepyfile("""
        import pytest


        @pytest.fixture(autouse=True)
        def autouse_fixture():
            return 1


        def test_simple():
            assert 1 == 1
    """)

    result = testdir.runpytest('--dead-fixtures')
    message = message_template.format(
        'autouse_fixture',
        'test_dont_list_autouse_fixture'
    )

    assert result.ret == 0
    assert message not in result.stdout.str()


def test_dont_list_same_file_fixture(testdir, message_template):
    testdir.makepyfile("""
        import pytest


        @pytest.fixture()
        def same_file_fixture():
            return 1


        def test_simple(same_file_fixture):
            assert 1 == same_file_fixture
    """)

    result = testdir.runpytest('--dead-fixtures')
    message = message_template.format(
        'same_file_fixture',
        'test_dont_list_same_file_fixture'
    )

    assert result.ret == 0
    assert message not in result.stdout.str()


def test_list_same_file_unused_fixture(testdir, message_template):
    testdir.makepyfile("""
        import pytest


        @pytest.fixture()
        def same_file_fixture():
            return 1


        def test_simple():
            assert 1 == 1
    """)

    result = testdir.runpytest('--dead-fixtures')
    message = message_template.format(
        'same_file_fixture',
        'test_list_same_file_unused_fixture'
    )

    assert result.ret == 0
    assert message in result.stdout.str()


def test_dont_list_conftest_fixture(testdir, message_template):
    testdir.makepyfile(conftest="""
        import pytest


        @pytest.fixture()
        def conftest_fixture():
            return 1
    """)

    testdir.makepyfile("""
        import pytest


        def test_conftest_fixture(conftest_fixture):
            assert 1 == conftest_fixture
    """)

    result = testdir.runpytest('--dead-fixtures')
    message = message_template.format(
        'conftest_fixture',
        'conftest'
    )

    assert result.ret == 0
    assert message not in result.stdout.str()


def test_list_conftest_unused_fixture(testdir, message_template):
    testdir.makepyfile(conftest="""
        import pytest


        @pytest.fixture()
        def conftest_fixture():
            return 1
    """)

    testdir.makepyfile("""
        import pytest


        def test_conftest_fixture():
            assert 1 == 1
    """)

    result = testdir.runpytest('--dead-fixtures')
    message = message_template.format(
        'conftest_fixture',
        'conftest'
    )

    assert result.ret == 0
    assert message in result.stdout.str()


def test_dont_list_decorator_usefixtures(testdir, message_template):
    testdir.makepyfile("""
        import pytest


        @pytest.fixture()
        def decorator_usefixtures():
            return 1


        @pytest.mark.usefixtures('decorator_usefixtures')
        def test_decorator_usefixtures():
            assert 1 == decorator_usefixtures
    """)

    result = testdir.runpytest('--dead-fixtures')
    message = message_template.format(
        'decorator_usefixtures',
        'test_dont_list_decorator_usefixtures'
    )

    assert result.ret == 0
    assert message not in result.stdout.str()


def test_write_docs_when_verbose(testdir):
    testdir.makepyfile("""
        import pytest


        @pytest.fixture()
        def some_fixture():
            '''Blabla fixture docs'''
            return 1


        def test_simple():
            assert 1 == 1
    """)

    result = testdir.runpytest('--dead-fixtures', '-v')

    assert 'Blabla fixture docs' in result.stdout.str()
