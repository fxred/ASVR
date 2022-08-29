import ffmpeg
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import pyperclip
from PIL import Image
import glob
import sys
import taglib

# reading the audio files
# mp3 files have priority over wave files

mp3_filename = glob.glob("IO/*.mp3")

# the empty list below is initially defined due to
# the type of output the glob library gives, which
# is an empty list if there's no files matching the parameters given

wav_filename = []

if mp3_filename == []:
  wav_filename = glob.glob("IO/*.wav")
  if wav_filename == []:
    print("NO audio files!")
    sys.exit()

if wav_filename != []:
  wav_filename = wav_filename[0][3:]

if mp3_filename != []:
  mp3_filename = mp3_filename[0][3:]

# reading the image files
# jpg files have priority over png files

jpg_filename = glob.glob("IO/*.jpg")

# for the same reason of lines 15-17, an empty list is defined for the secondary file type

png_filename = []

if jpg_filename == []:
  png_filename = glob.glob("IO/*.png")
  if png_filename == []:
    print("NO image files!")
    sys.exit()

if jpg_filename != []:
  jpg_filename = jpg_filename[0][3:]
  img = Image.open("IO/{}".format(jpg_filename))
  width = img.width
  img.close()

if png_filename != []:
  png_filename = png_filename[0][3:]
  img = Image.open("IO/{}".format(png_filename))
  width = img.width
  img.close()

if jpg_filename == [] and png_filename != []:
  jpg_filename = png_filename

# setting the width (which is also the height) of the video

if width >= 1440:
  width = 1440
elif width >= 1080 and width < 1440:
  width = 1080
else:
  width = 720

# getting the length of the audio file
# the variable "tag" here stores a list of metadata

if mp3_filename != []:
  audio = MP3("IO/{}".format(mp3_filename))
  length = float(audio.info.length)
  tag = taglib.File("IO/{}".format(mp3_filename))
  tag = tag.tags

else:
  if wav_filename != []:
    audio = WAVE("IO/{}".format(wav_filename))
    length = float(audio.info.length)
    tag = taglib.File("IO/{}".format(wav_filename))
    tag = tag.tags

if mp3_filename == [] and wav_filename != []:
  mp3_filename = wav_filename

# setting the unsanitized name based on metadata
# if there's insufficient metadata, the name is copied directly from the audio filename

if "TITLE" in tag:
  if "ARTIST" in tag:
    if "ALBUM" in tag:
      if tag["ALBUM"] != tag["TITLE"]:
        name = "{} - {} [{}]".format(tag["ARTIST"][0], tag["TITLE"][0], tag["ALBUM"][0])
      else:
        name = "{} - {}".format(tag["ARTIST"][0], tag["TITLE"][0])
    else:
      name = "{} - {}".format(tag["ARTIST"][0], tag["TITLE"][0])
else:
  name = mp3_filename[0:len(mp3_filename)-4]

# finally sanitizing the name (removing special characters)
# so we can set it as the video filename with no problems

if (name.count('/') != 0) or (name.count(':') != 0) or (name.count('?') != 0) or (name.count('>') != 0) or (name.count('<') != 0):
  character_replace = {'/': '',
                    ':': '',
                    '?': '',
                    '>': '',
                    '<': ''}
  for key, value in character_replace.items():
    name_sanitized = name.replace(key, value)
else:
  name_sanitized = name

# giving ffmpeg the input files

input_video = ffmpeg.input("IO/{}".format(jpg_filename), loop=1, framerate=1, t=length)
input_audio = ffmpeg.input("IO/{}".format(mp3_filename))

# setting up a few attributes to the video

(
    ffmpeg
    .concat(input_video, input_audio, v=1, a=1)
    .filter('scale', width, -1)
    .output('IO/{}.mp4'.format(name_sanitized), acodec='mp3', audio_bitrate='320k')
    .run(overwrite_output=True)
)

# copies the unsanitized name to the user clipboard

pyperclip.copy(name)