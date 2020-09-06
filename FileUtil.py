import os
import re
from pathlib import Path
from shutil import copyfile


def walk(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def copy_file(src, dest):
    assert src is not None
    assert dest is not None
    assert Path(src).exists()
    dest_path = Path(dest).parent
    if not dest_path.exists():
        dest_path.mkdir(parents=True, exist_ok=True)
    copyfile(src, dest)


def collect_files(directory, filter_file_type) -> list:
    assert Path(directory).exists()
    filtered_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            full_name = root + os.path.sep + file
            filename, file_extension = os.path.splitext(file)
            if os.path.isfile(full_name) and file_extension in filter_file_type:
                filtered_files.append(full_name)
    return filtered_files


def collect_files_with_regex(directory, filter_file_type, regex) -> list:
    assert Path(directory).exists()
    filtered_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            full_name = root + os.path.sep + file
            filename, file_extension = os.path.splitext(file)
            if regex is not None and is_file_matching_with_regex(full_name, file_extension, filter_file_type, regex):
                filtered_files.append(full_name)
            elif is_file_matching(full_name, file_extension, filter_file_type):
                filtered_files.append(full_name)
    return filtered_files


def is_file_matching_with_regex(full_name, file_extension, filter_file_type, regex) -> bool:
    return os.path.isfile(full_name) and (
            file_extension in filter_file_type or len(re.findall(regex, file_extension)) != 0)


def is_file_matching(full_name, file_extension, filter_file_type) -> bool:
    return os.path.isfile(full_name) and file_extension in filter_file_type
