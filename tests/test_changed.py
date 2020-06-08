# -*- coding: utf-8 -*-
import pytest

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

GIT_DIFF_CHANGE_IN_FUNCTION = \
    b'diff --git a/dummy_test.py b/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/dummy_test.py\n' \
    b'+++ b/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b' class TestClassOne:\n' \
    b'\n' \
    b'     def test_class_one_test_one(self):\n' \
    b'+\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_one_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'\n' \
    b' class TestClassTwo:\n' \
    b'\n' \
    b'     def test_class_two_test_one(self):\n' \
    b'+\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_two_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n'

GIT_DIFF_CHANGE_IN_CLASS = \
    b'diff --git a/dummy_test.py b/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/dummy_test.py\n' \
    b'+++ b/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b' class TestClassOne:\n' \
    b'+\n' \
    b'\n' \
    b'     def test_class_one_test_one(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_one_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'\n' \
    b' class TestClassTwo:\n' \
    b'+\n' \
    b'\n' \
    b'     def test_class_two_test_one(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_two_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n'

GIT_DIFF_CODE_REMOVED = \
    b'diff --git a/dummy_test.py b/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/dummy_test.py\n' \
    b'+++ b/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b' class TestClassOne:\n' \
    b'\n' \
    b'-\n' \
    b'-\n' \
    b'     def test_class_one_test_one(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_one_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'\n' \
    b' class TestClassTwo:\n' \
    b'\n' \
    b'-\n' \
    b'-\n' \
    b'     def test_class_two_test_one(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_two_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n'

GIT_DIFF_CODE_REMOVED_IN_FUNCTION = \
    b'diff --git a/dummy_test.py b/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/dummy_test.py\n' \
    b'+++ b/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b' class TestClassOne:\n' \
    b'\n' \
    b'     def test_class_one_test_one(self):\n' \
    b'-\n' \
    b'-\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_one_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'\n' \
    b' class TestClassTwo:\n' \
    b'\n' \
    b'     def test_class_two_test_one(self):\n' \
    b'-\n' \
    b'-\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_two_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n'

GIT_DIFF_ADDED_CODE = \
    b'diff --git a/dummy_test.py b/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- dev/null\n' \
    b'+++ b/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b'+ class TestClassOne:\n' \
    b'+\n' \
    b'+     def test_class_one_test_one(self):\n' \
    b'+\n' \
    b'+         assert 1 + 1 == 2\n' \
    b'+\n' \
    b'+     def test_class_one_test_two(self):\n' \
    b'+         assert 1 + 1 == 2\n'

GIT_DIFF_ADDED_AND_RENAMED_CODE = \
    b'diff --git a/dummy_test.py b/dummy_2_test.py\n' \
    b'similarity index 93%\n' \
    b'rename from a/dummy_test.py' \
    b'rename to b/dummy_2_test.py' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/dummy_test.py\n' \
    b'+++ b/dummy_test_2.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b'+ class TestClassOne:\n' \
    b'+\n' \
    b'+     def test_class_one_test_one(self):\n' \
    b'+\n' \
    b'+         assert 1 + 1 == 2\n' \
    b'+\n' \
    b'+     def test_class_one_test_two(self):\n' \
    b'+         assert 1 + 1 == 2\n'

GIT_DIFF_CHANGE_IN_FUNCTION_CUT_OFF_METHOD_PARAMS = \
    b'diff --git a/dummy_test.py b/dummy_test.py\n' \
    b'index 6575e440acc807efabcbc156b8683c6344b6fda4..' \
    b'11314b99949c7e987f050255fa4d0c6497c529bc 100644\n' \
    b'--- a/dummy_test.py\n' \
    b'+++ b/dummy_test.py\n' \
    b'@@ -4,6 +4,7 @@ import pytest\n' \
    b' class TestClassOne:\n' \
    b'\n' \
    b'     def test_class_one_test_one\n' \
    b'+\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_one_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'\n' \
    b' class TestClassTwo:\n' \
    b'\n' \
    b'     def test_class_two_test_one(\n' \
    b'+\n' \
    b'         assert 1 + 1 == 2\n' \
    b'\n' \
    b'     def test_class_two_test_two(self):\n' \
    b'         assert 1 + 1 == 2\n'


def test_shows_changed_tests(testdir):
    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files..." in result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_output_no_changes(get_changed_files_mock, testdir, config_mock):
    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    renamed_mock = MagicMock()
    renamed_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock,
                                           renamed_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 0:" in result.stdout.str()


@pytest.mark.parametrize(
    "git_diff",
    [GIT_DIFF_CODE_REMOVED, GIT_DIFF_CHANGE_IN_CLASS]
)
@patch("pytest_changed.get_changed_files")
def test_output_removed_code(
        get_changed_files_mock,
        testdir,
        config_mock,
        git_diff
):
    """
    In case of changes inside the class body, the class names should
    be detected.

    To make sure all tests inside the class are running as changes in the class
    definition may affect test functions defined in the scope of the class.

    When pytest receives a class it will run all test-functions
    that are contained.
    """
    diff = MagicMock()
    diff.diff = git_diff
    diff.a_path = "dummy_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([diff]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    renamed_mock = MagicMock()
    renamed_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock,
                                           renamed_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 1:\n" \
               "+ %s/dummy_test.py:\n" \
               "  ['TestClassOne', 'TestClassTwo']" % str(testdir.tmpdir) \
               in result.stdout.str()


@pytest.mark.parametrize(
    "git_diff",
    [
        GIT_DIFF_CHANGE_IN_FUNCTION,
        GIT_DIFF_CODE_REMOVED_IN_FUNCTION,
        GIT_DIFF_CHANGE_IN_FUNCTION_CUT_OFF_METHOD_PARAMS
     ]
)
@patch("pytest_changed.get_changed_files")
def test_output_removed_code_in_function(
        get_changed_files_mock,
        testdir,
        config_mock,
        git_diff
):
    """
    In case of code removal just to specific functions
    their names will also be detected.
    """
    diff = MagicMock()
    diff.diff = git_diff
    diff.a_path = "dummy_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([diff]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    renamed_mock = MagicMock()
    renamed_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock,
                                           renamed_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        pytest_output = result.stdout.str()
        assert "Changed test files... 1:\n" \
               "+ %s/dummy_test.py:\n" \
               "  ['test_class_one_test_one', 'test_class_two_test_one']" \
               % str(testdir.tmpdir) in pytest_output


@patch("pytest_changed.get_changed_files")
def test_output_added_file(
        get_changed_files_mock,
        testdir,
        config_mock
):
    """
    In case of files being added all tests of the file must be detected.
    """
    diff = MagicMock()
    diff.diff = GIT_DIFF_ADDED_CODE
    diff.a_path = "/dev/null"
    diff.b_path = "dummy_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([diff]))

    renamed_mock = MagicMock()
    renamed_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock,
                                           renamed_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 1:\n" \
               "+ %s/dummy_test.py:\n" \
               "  ['TestClassOne', 'test_class_one_test_one', " \
               "'test_class_one_test_two']" % str(testdir.tmpdir) in \
               result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_output_file_not_in_args(
        get_changed_files_mock,
        testdir,
        config_mock
):
    """
    In case of files being added all tests of the file must be detected.
    """
    diff = MagicMock()
    diff.diff = GIT_DIFF_ADDED_CODE
    diff.a_path = "/dev/null"
    diff.b_path = "dummy_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([diff]))

    renamed_mock = MagicMock()
    renamed_mock.__iter__ = MagicMock(return_value=iter([]))

    get_changed_files_mock.return_value = (modified_mock, added_mock,
                                           renamed_mock)

    tests_dir = testdir.mkdir("tests")

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed", tests_dir)
        assert "Changed test files... 0:" in result.stdout.str()


@patch("pytest_changed.get_changed_files")
def test_output_file_renamed(
        get_changed_files_mock,
        testdir,
        config_mock
):
    """
    In case of files being added all tests of the file must be detected.
    """
    diff = MagicMock()
    diff.diff = GIT_DIFF_ADDED_AND_RENAMED_CODE
    diff.a_path = "dummy_test.py"
    diff.b_path = "dummy_2_test.py"

    modified_mock = MagicMock()
    modified_mock.__iter__ = MagicMock(return_value=iter([]))

    added_mock = MagicMock()
    added_mock.__iter__ = MagicMock(return_value=iter([]))

    renamed_mock = MagicMock()
    renamed_mock.__iter__ = MagicMock(return_value=iter([diff]))

    get_changed_files_mock.return_value = (modified_mock, added_mock,
                                           renamed_mock)

    with patch("pytest_changed.Repo"):
        result = testdir.runpytest("--changed")
        assert "Changed test files... 1:\n" \
               "+ %s/dummy_2_test.py:\n" \
               "  ['TestClassOne', 'test_class_one_test_one', " \
               "'test_class_one_test_two']" \
               % str(testdir.tmpdir) in result.stdout.str()
