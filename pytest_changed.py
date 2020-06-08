# -*- coding: utf-8 -*-

import os
import re

import _pytest
from git import Repo

MATCH_PATTERN = r".*(?:def|class)\s([a-zA-Z_0-9]*).*"


def pytest_addoption(parser):
    parser.addoption(
        "--changed",
        action="store_true",
        default=False,
        help="Find changed test functions and only run those."
    )


def pytest_configure(config):
    changed = config.getoption("changed")
    if not changed:
        return

    changed_files = get_changed_files_with_functions(config=config)
    config.args = changed_files.keys()
    _display_affected_tests(config, changed_files)


def pytest_collection_modifyitems(session, config, items):
    changed = config.getoption("changed")
    if not changed:
        return

    run = []
    deselected = []
    changed_files_and_funcs = get_changed_files_with_functions(config=config)
    for item in items:
        item_path = item.location[0]
        for file_path, names in changed_files_and_funcs.items():
            if item_path in file_path:
                for name in names:
                    if item.cls is not None:
                        if name == item.cls.__name__ or name == item.name:
                            run.append(item)
                            continue
                    elif name == item.name:
                        run.append(item)
                        continue
                    deselected.append(item)
    run = _remove_duplicates(run)
    config.hook.pytest_deselected(items=deselected)
    items[:] = run


def _display_affected_tests(config, files):
    header_message = "Changed test files... {}:".format(len(files))
    files_messages = []
    for filename, changed in files.items():
        file_message = "+ {}:\n  {}"
        files_messages.append(file_message.format(filename, changed))
    _write(config, [header_message] + files_messages)


def _write(config, message):
    writer = _pytest.config.create_terminal_writer(config)
    writer.line()

    for line in message:
        writer.line(line)


def get_changed_files(repo):
    current_commit = repo.commit("HEAD~0")
    master_commit = repo.commit("origin/master")

    diff_index = master_commit.diff(current_commit, create_patch=True)
    modified = diff_index.iter_change_type('M')
    added = diff_index.iter_change_type('A')
    renamed = diff_index.iter_change_type('R')

    return modified, added, renamed


def get_changed_names(diff):
    changed = list()
    current_name = ""
    for line in diff.split(b'\n'):
        line = str(line.decode("utf-8"))
        match = re.search(MATCH_PATTERN, line)
        if match is not None:
            name = match.groups()[0].strip()
            if "test" in name.lower():
                current_name = name
                continue

        if current_name:
            if line.startswith("+") or line.startswith("-"):
                changed.append(current_name)

    return _remove_duplicates(changed)


def get_changed_files_with_functions(config):
    root_dir = str(config.rootdir)
    repository = Repo(path=root_dir)
    _modified, _added, _renamed = get_changed_files(repo=repository)
    test_file_convention = config._getini("python_files")
    changed = dict()
    for diff in _modified:
        filename = diff.a_path.rsplit("/")[-1]
        if _is_test_file(filename, test_file_convention):
            full_path = os.path.join(root_dir, diff.a_path)
            changed[full_path] = get_changed_names(diff=diff.diff)
    for diff in _added:
        filename = diff.b_path.rsplit("/")[-1]
        if _is_test_file(filename, test_file_convention):
            full_path = os.path.join(root_dir, diff.b_path)
            changed[full_path] = get_changed_names(diff=diff.diff)
    for diff in _renamed:
        filename_b = diff.b_path.rsplit("/")[-1]
        if _is_test_file(filename_b, test_file_convention):
            full_a_path = os.path.join(root_dir, diff.a_path)
            full_b_path = os.path.join(root_dir, diff.b_path)
            if full_a_path in changed:
                del changed[full_a_path]
                changed[full_b_path] = get_changed_names(diff=diff.diff)
            changed[full_b_path] = get_changed_names(diff=diff.diff)
    changed = filter_for_arguments(config.args, changed)
    return changed


def filter_for_arguments(config_args, changed_files):
    if not config_args:
        return changed_files

    changed = dict()
    for config_arg in config_args:
        for path, names in changed_files.items():
            if config_arg in path:
                changed[path] = names
    return changed


def _is_test_file(file_path, test_file_convention):
    re_list = [
        item.replace(".", r"\.").replace("*", ".*")
        for item in test_file_convention
    ]
    re_string = r"(\/|^)" + r"|".join(re_list)
    return bool(re.search(re_string, file_path))


def _remove_duplicates(seq):
    """
    This method preserves the order when filtering out duplicates
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
