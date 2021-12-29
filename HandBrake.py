import os.path
import platform
import shutil
import subprocess
from os import path, walk
from os.path import expanduser

journal = "journal.log"

'''
~ is the user home 
- expanduser(~) will determine the correct user home regardless of the operating system

so the path will be 
~/Convert/Result 
and 
~/Convert/Source
respectively
'''
target_path = expanduser(path.join("~", "Convert", "Result"))
source_path = expanduser(path.join("~", "Convert", "Source"))

'''
File endings which will be queued for conversion
'''
valid_endings = ["mkv", "m4v", "mp4"]

'''
Index for the target container file. 0 based
'''
selected_container = 1
container = ["av_mp4", "av_mkv", "av_webm"]
container_filetype = ["mp4", "mkv", "webm"]

'''
he-aac is the higher quality audio codec but only available on macos.
'''
fallback_audio = ["he-aac", "aac"]

'''
x265 encoders.
10 bit has a quality improvement over the 8 bit standard x265 regarding rounding errors
So the default will be 10bit
'''
selected_encoder = 1
encoder = ["x265", "x265_10bit", "x265_12bit"]

'''
General input parameters like format, source and output
'''
input_arg = ["--input"]
output_arg = ["--output"]
format_arg = ["--format"]
markers_arg = ["--markers"]

'''
Video options for quality 20 (lower number for higher quality).
If using the quality options, --two-pass is not necessary
'''
video_quality = "20"
selected_encoder_preset = 6
encoder_preset = ["ultrafast", "superfast", "veryfast", "faster", "medium", "slow", "slower", "veryslow", "placebo"]
video_options = "--encoder {codec} --quality {quality} --encoder-preset {encoder_preset}"

'''
audio options. audio tracks which aren't present will be skipped, so just enumerate from 1 to 15
copy all audio tracks and if not possible use fallback audio
'''
audio_options = "--audio 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 --aencoder copy --audio-fallback {audio_fallback} "

'''
Same as audio options. Tracks which aren't present will be skipped, so just enumerate from 1 to 15
'''
subtitles_options = "--subtitle 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 "


def get_audio_fallback():
    """
    If this script is running on mac os, use the higher quality fallback 'he-aac' codec.
    Otherwise default to "normal" 'aac'
    """
    system = platform.system()
    if system == 'Darwin':
        return fallback_audio[0]
    return fallback_audio[1]


def main():
    files_to_convert, files_to_copy = find_files()
    os.makedirs(target_path, exist_ok=True)

    """
    Copy non-convertible files to the result directory to keep the folder and file structure.
    Will copy things like thumbnails and subtitles
    """
    copy_non_convert_files(files_to_copy, target_path)

    for file in files_to_convert:
        convert_file = check_journal(file, target_path)

        if convert_file:
            target_dir = path.dirname(file).replace(source_path, target_path)
            target = path.join(target_dir, path.basename(file))
            os.makedirs(target_dir, exist_ok=True)
            if path.isfile(target):
                os.remove(target)

            cmd = create_command(file, target)
            subprocess.run(cmd)
            write_journal(file, target_path)


def write_journal(file, real_path):
    journal_file = open(path.join(real_path, journal), 'a')
    journal_file.write(path.basename(file))


def create_command(file, target):
    input_arg.append(file)
    output_arg.append(create_target_filename(target))
    format_arg.append(container[selected_container])
    file_cmd = input_arg + output_arg + format_arg + markers_arg
    video_cmd = video_options.format(codec=encoder[selected_encoder],
                                     quality=video_quality,
                                     encoder_preset=encoder_preset[selected_encoder_preset]).split()
    audio_cmd = audio_options.format(audio_fallback=get_audio_fallback()).split()
    subtitle_cmd = subtitles_options.split()

    cmd = ["handbrakeCLI"] + file_cmd + video_cmd + audio_cmd + subtitle_cmd
    print(cmd)
    return cmd


def create_target_filename(target):
    split = str(target).split(".")
    ending = split[len(split) - 1]
    target = target.replace("." + ending, "." + container_filetype[selected_container])
    target = target.replace("h264", "h265")
    return target


def check_journal(file, real_path):
    """
    If the file is already registered in the journal the script will not
    attempt to convert it again
    """
    with open(path.join(real_path, journal)) as f:
        lines = f.readlines()
        if path.basename(file) in lines:
            print(path.basename(file) + " was already processed. Skipping ...")
            return False
    return True


def copy_non_convert_files(files_to_copy, target_path):
    for file in files_to_copy:
        target_dir = path.dirname(file).replace(source_path, target_path)
        os.makedirs(target_dir, exist_ok=True)
        target = path.join(target_dir, path.basename(file))
        if not path.exists(target):
            shutil.copyfile(file, target)
            print("Copied " + file + " to " + target)


def find_files():
    files_to_convert = []
    files_to_copy = []
    for (dirpath, _, filenames) in walk(source_path):

        for filename in filenames:
            split = str(filename).split(".")
            if split[len(split) - 1] in valid_endings:
                files_to_convert.append(path.join(dirpath, filename))
            elif not str(filename).startswith("."):
                files_to_copy.append(path.join(dirpath, filename))

    return files_to_convert, files_to_copy


if __name__ == '__main__':
    main()
