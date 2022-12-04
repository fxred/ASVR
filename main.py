import ffmpeg
import glob
from PIL import Image
import sys
import os
import audioread


filenames_mp3 = [os.path.basename(filename) for
                filename in glob.glob("IO/*.mp3")]

filenames_wav = [os.path.basename(filename) for
                filename in glob.glob("IO/*.wav")]

filenames_flac = [os.path.basename(filename) for
                filename in glob.glob("IO/*.flac")]

audio_filenames = filenames_flac + filenames_mp3 + filenames_wav


if len(audio_filenames) > 1:

    print("Which audio file do you want to use?")

    for filename in audio_filenames:
        print("{}: {}".format(audio_filenames.index(filename)+1, filename))

    desired_audio_filename_index = int(input()) - 1
    desired_audio_filename_string = audio_filenames[desired_audio_filename_index]

elif len(audio_filenames) == 1:
    desired_audio_filename_string = audio_filenames[0]

else:
    print("No audio files! Please insert an audio file into the IO directory.")
    sys.exit()


with audioread.audio_open("IO/{}".format(desired_audio_filename_string)) as f:
    length = f.duration


filenames_jpg = [os.path.basename(filename) for
                filename in glob.glob("IO/*.jpg")]

filenames_png = [os.path.basename(filename) for
                filename in glob.glob("IO/*.png")]

image_filenames = filenames_jpg + filenames_png


if len(image_filenames) > 1:

    print("Which image file do you want to use?")

    for filename in image_filenames:
        print("{}: {}".format(image_filenames.index(filename)+1, filename))

    desired_image_filename_index = int(input()) - 1
    desired_image_filename_string = image_filenames[desired_image_filename_index]

elif len(image_filenames) == 1:
    desired_image_filename_string = image_filenames[0]

else:
    print("No image files! Please insert an image file into the IO directory.")
    sys.exit()


image_file = Image.open("IO/{}".format(desired_image_filename_string))
image_width = image_file.width
image_file.close()

if image_width >= 1440:
    video_width = 1440
elif image_width >= 1080 and image_width < 1440:
    video_width = 1080
else:
    video_width = 720


video_input = ffmpeg.input("IO/{}".format(desired_image_filename_string),
                           loop = 1, framerate = 1, t = length)
audio_input = ffmpeg.input("IO/{}".format(desired_audio_filename_string))

(
    ffmpeg
    .concat(video_input, audio_input, v = 1, a = 1)
    .filter('scale', video_width, -1)
    .output('IO/{}.mp4'.format(
            os.path.splitext(desired_audio_filename_string)[0]),
            acodec = 'mp3', audio_bitrate = '320k')
    .run(overwrite_output = True)
)
