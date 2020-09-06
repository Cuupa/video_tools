import os
import datetime
import getpass
from shutil import copyfile

mediacard_folder_determiner = {"100EOS5D"}
path_to_mount = "/run/media/" + getpass.getuser()

output_dir = os.environ['HOME'] + os.path.sep + "Videos/Import"


def walk(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def find_media_card():
    for directories in walk(path_to_mount, level=2):
        for directory in directories:
            if isinstance(directory, list):
                for directory_final in directory:
                    if str(directory_final) in mediacard_folder_determiner:
                        return directories[0], directory_final
    return None


def create_directories(date):
    directory = output_dir + os.path.sep + date
    directories = {
        directory + " - {TEMPLATE}/Footage/MOV",
        directory + " - {TEMPLATE}/Footage/RAW",
        directory + " - {TEMPLATE}/Footage/Audio",
        directory + " - {TEMPLATE}/Footage/Calibration",
        directory + " - {TEMPLATE}/Edit",
        directory + " - {TEMPLATE}/Script",
        directory + " - {TEMPLATE}/Review"
    }

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def process_mov(directory, date):
    mov_files = []
    '''
    mov-files are not stored in a folder
    '''
    for root, _, files in os.walk(directory):
        for file in files:
            full_name = root + os.path.sep + file
            if os.path.isfile(full_name) and str(file).endswith(".mov"):
                mov_files.append(full_name)

    for file in mov_files:
        out = output_dir + os.path.sep + date + " - {TEMPLATE}/Footage/MOV"
        print("[2]. copying " + file + " to " + out + os.path.sep + os.path.basename(file))
        copyfile(file, out + os.path.sep + os.path.basename(file))
        print("[3]. done ...")


def process_raw(directory, date):
    raw_files = []
    '''
    mov-files are not stored in a folder
    '''
    for root, _, files in os.walk(directory):
        for file in files:
            full_name = root + os.path.sep + file
            if os.path.isfile(full_name) and (str(file).endswith(".mlv") or str(file).endswith(".MLV")):
                raw_files.append(full_name)

    for file in raw_files:
        out = output_dir + os.path.sep + date + " - {TEMPLATE}/Footage/RAW"
        print("[3]. copying " + file + " to " + out + os.path.sep + os.path.basename(file))
        copyfile(file, out + os.path.sep + os.path.basename(file))
        print("[3]. done ...")


def main():
    rootdir, directory = find_media_card()
    if directory is None or rootdir is None:
        return

    now = datetime.datetime.now()
    date = now.strftime("%Y") + "." + now.strftime("%m") + "." + now.strftime("%d")
    print("[1]. creating directories")
    create_directories(date)
    print("[1]. done ...")
    card_dir = rootdir + os.path.sep + directory
    print("[2]. processing mov files for " + card_dir)
    process_mov(card_dir, date)
    print("[2]. done ...")
    print("[3]. processing raw files for " + card_dir)
    process_raw(card_dir, date)
    print("[3]. done ...")
    exit(-42)


print(os.environ)
main()
