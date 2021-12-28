import os.path
import subprocess
from os import path, walk
from os.path import expanduser

'''
ffprobe_language = "{filename} -show_entries stream=index:stream_tags=language -select_streams a -of compact=p=0:nk=1"
'''

journal = "journal.log"

resultpath = path.join("~", "Convert", "Result")
sourcepath = path.join("~", "2Convert", "Result")
valid_endings = ["mkv"]

format = ["av_mp4", "av_mkv", "av_webm"]
codec = ["x265", "x265_10bit", "x265_12bit"]

file_options = "--input {input} --output {output} --format {format} --markers "
video_options = "--encoder {codec} --quality 20 --two-pass "
audio_options = "--audio 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 --aencoder copy --audio-fallback he-aac "
subtitles_options = "--subtitle 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 "


def main():
    files = find_files()

    for file in files:
        real_path = expanduser(resultpath)
        os.makedirs(real_path, exist_ok=True)
        already_done = False
        with open(path.join(real_path, journal)) as f:
            lines = f.readlines()
            if path.basename(file) in lines:
                already_done = True

        if not already_done:
            result_file = path.join(real_path, path.basename(file))
            file_cmd = file_options.format(input=file, output=result_file, format=format[1])
            video_cmd = video_options.format(codec=codec[1])
            audio_cmd = audio_options
            subtitle_cmd = subtitles_options

            cmd = ("handbrakeCLI " + file_cmd + video_cmd + audio_cmd + subtitle_cmd).split()
            subprocess.run(cmd)
            journal_file = open(path.join(real_path, journal), 'a')
            journal_file.write(path.basename(file))


def find_files():
    absolute_paths = []
    real_path = expanduser(sourcepath)
    for (dirpath, dirname, filenames) in walk(real_path):

        for filename in filenames:
            split = str(filename).split(".")
            if split[len(split) - 1] in valid_endings:
                absolute_paths.append(path.join(dirpath, filename))

    return absolute_paths


if __name__ == '__main__':
    main()
