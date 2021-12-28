import moviepy.editor as mp
from moviepy.audio.io import AudioFileClip


def get_audio(file) -> AudioFileClip:
    return mp.VideoFileClip(file)


def save_audio(file, dest):
    mp.VideoFileClip(file).audio.write_audiofile(dest)
