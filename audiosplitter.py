import moviepy.editor as mp

def get_audio(file) -> AudioFileClip:
  videoclip = mp.VideoFileClip("Video File") 
  return videoclip.audio
