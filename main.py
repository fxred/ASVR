import ffmpeg
import glob
from PIL import Image
import sys
import os
import audioread


filenamesMP3 = [os.path.basename(filename) for filename in glob.glob("IO/*.mp3")]
filenamesWAV = [os.path.basename(filename) for filename in glob.glob("IO/*.wav")]
filenamesFLAC = [os.path.basename(filename) for filename in glob.glob("IO/*.flac")]

audioFilenames = filenamesFLAC + filenamesMP3 + filenamesWAV


if len(audioFilenames) > 1:

    print("Which audio file do you want to use?")

    for filename in audioFilenames:
        print("{}: {}".format(audioFilenames.index(filename)+1, filename))

    desiredAudioFilenameIndex = int(input()) - 1
    desiredAudioFilenameString = audioFilenames[desiredAudioFilenameIndex]

elif len(audioFilenames) == 1:
    desiredAudioFilenameString = audioFilenames[0]

else:
    print("No audio files! Please insert an audio file into the IO directory.")
    sys.exit()


with audioread.audio_open("IO/{}".format(desiredAudioFilenameString)) as f:
    length = f.duration


filenamesJPG = [os.path.basename(filename) for filename in glob.glob("IO/*.jpg")]
filenamesPNG = [os.path.basename(filename) for filename in glob.glob("IO/*.png")]

imageFilenames = filenamesJPG + filenamesPNG


if len(imageFilenames) > 1:

    print("Which image file do you want to use?")

    for filename in imageFilenames:
        print("{}: {}".format(imageFilenames.index(filename)+1, filename))

    desiredImageFilenameIndex = int(input()) - 1
    desiredImageFilenameString = imageFilenames[desiredImageFilenameIndex]

elif len(imageFilenames) == 1:
    desiredImageFilenameString = imageFilenames[0]

else:
    print("No image files! Please insert an image file into the IO directory.")
    sys.exit()


imageFile = Image.open("IO/{}".format(desiredImageFilenameString))
imageWidth = imageFile.width
imageFile.close()

if imageWidth >= 1440:
    videoWidth = 1440
elif imageWidth >= 1080 and imageWidth < 1440:
    videoWidth = 1080
else:
    videoWidth = 720


videoInput = ffmpeg.input("IO/{}".format(desiredImageFilenameString), loop = 1, framerate = 1, t = length)
audioInput = ffmpeg.input("IO/{}".format(desiredAudioFilenameString))

(
    ffmpeg
    .concat(videoInput, audioInput, v = 1, a = 1)
    .filter('scale', videoWidth, -1)
    .output('IO/{}.mp4'.format(os.path.splitext(desiredAudioFilenameString)[0]), acodec = 'mp3', audio_bitrate = '320k')
    .run(overwrite_output = True)
)