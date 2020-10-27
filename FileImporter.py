import datetime
import getpass
import os
import sys
from pathlib import Path

import FileUtil

'''
Name of the directory where the files are located
'''
mediacard_folder_determiner = {"100EOS5D"}

'''
Name of the mountpoint, where the cardreader is mounted
'''
path_to_mount = "/run/media/" + getpass.getuser()

'''
Path where the videos will be imported to
'''
output_dir = os.environ['HOME'] + os.path.sep + "Videos/Import"

mov_file_endings = {".mov", ".MOV"}
raw_file_endings = {".mlv", ".MLV"}
raw_file_parts = "\\.M\\d\\d"


def find_media_card():
    for directories in FileUtil.walk(path_to_mount, level=2):

        for directory in directories:
            if not isinstance(directory, list):
                continue

            for directory_final in directory:
                if str(directory_final) in mediacard_folder_determiner:
                    return directories[0], directory_final
    return None, None


def create_directories(date, project_name):
    """
    Directories which are going to be created according to my workflow
    """
    directory = output_dir + os.path.sep + date
    directories = {
        directory + " - {0}/Footage/MOV".format(project_name),
        directory + " - {0}/Footage/RAW".format(project_name),
        directory + " - {0}/Footage/Audio".format(project_name),
        directory + " - {0}/Footage/Calibration".format(project_name),
        directory + " - {0}/Edit".format(project_name),
        directory + " - {0}/Script".format(project_name),
        directory + " - {0}/Review".format(project_name),
        directory + " - {0}/Final Cut".format(project_name),
        directory + " - {0}/Bill".format(project_name)
    }

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def process_mov(directory, date, project_name):
    mov_files = FileUtil.collect_files(directory, mov_file_endings)
    out = output_dir + os.path.sep + date + " - {0}/Footage/MOV".format(project_name)
    for file in mov_files:
        FileUtil.copy_file(file, out + os.path.sep + os.path.basename(file))


def process_raw(directory, date, project_name):
    raw_files = FileUtil.collect_files_with_regex(directory, raw_file_endings, raw_file_parts)
    out = output_dir + os.path.sep + date + " - {0}/Footage/RAW".format(project_name)
    for file in raw_files:
        parent_dir_name = Path(file).parent.name
        path_to_save = out + os.path.sep
        if parent_dir_name not in mediacard_folder_determiner:
            path_to_save = path_to_save + parent_dir_name + os.path.sep + os.path.basename(file)
        else:
            path_to_save = path_to_save + os.path.basename(file)
        FileUtil.copy_file(file, path_to_save)
        print("Imported " + file)


def main():
    arguments = sys.argv
    project_name = ""
    if len(arguments) >= 1:
        for arg in range(1, len(arguments)):
            project_name = project_name + arguments[arg] + " "
        project_name = project_name.strip()
    else:
        project_name = "{TEMPLATE}"

    date = get_date()
    create_directories(date, project_name)
    print("Successfully created " + output_dir + os.path.sep + date + " - {0}".format(project_name) + os.path.sep)
    rootdir, mediacard_directory = find_media_card()
    if mediacard_directory is None or rootdir is None:
        print("No files for import found")
        return
    card_dir = rootdir + os.path.sep + mediacard_directory
    process_mov(card_dir, date, project_name)
    process_raw(card_dir, date, project_name)
    print("All files imported")


def get_date():
    now = datetime.datetime.now()
    return now.strftime("%Y") + "." + now.strftime("%m") + "." + now.strftime("%d")


main()
