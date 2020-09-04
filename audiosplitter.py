import moviepy.editor as mp

def get_audio(file) -> AudioFileClip:
  videoclip = mp.VideoFileClip(file) 
  return videoclip.audio

def save_audio(file, dest):
  videoclip = mp.VideoFileClip(file) 
  videoclip.write_audiofile(dest) 
