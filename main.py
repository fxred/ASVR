import os
import sys
import glob
import ffmpeg
from PIL import Image
import audioread
import cv2


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
        print(f"{audio_filenames.index(filename)+1}: {filename}")

    desired_audio_filename_index = int(input()) - 1
    desired_audio_filename_string = audio_filenames[desired_audio_filename_index]

elif len(audio_filenames) == 1:
    desired_audio_filename_string = audio_filenames[0]

else:
    print("No audio files! Please insert an audio file into the IO directory.")
    sys.exit()

with audioread.audio_open(f"IO/{desired_audio_filename_string}") as f:
    length = f.duration


filenames_jpg = [os.path.basename(filename) for
                filename in glob.glob("IO/*.jpg")]

filenames_png = [os.path.basename(filename) for
                filename in glob.glob("IO/*.png")]

image_filenames = filenames_jpg + filenames_png


if len(image_filenames) > 1:

    print("Which image file do you want to use?")

    for filename in image_filenames:
        print(f"{image_filenames.index(filename)+1}: {filename}")

    desired_image_filename_index = int(input()) - 1
    desired_image_filename_string = image_filenames[desired_image_filename_index]

elif len(image_filenames) == 1:
    desired_image_filename_string = image_filenames[0]

else:
    print("No image files! Please insert an image file into the IO directory.")
    sys.exit()


with Image.open(f"IO/{desired_image_filename_string}") as image_file:
    image_width = image_file.width
    image_height = image_file.height

if image_height >= 1250:
    ratio = 1440/image_height
    width_height = (round(image_width*ratio), 1440)
elif 900 <= image_height < 1250:
    ratio = 1080/image_height
    width_height = (round(image_width*ratio), 1080)
else:
    ratio = 720/image_height
    width_height = (round(image_width*ratio), 720)

image = cv2.imread(f"IO/{desired_image_filename_string}")
new_image = cv2.resize(image, width_height, interpolation = cv2.INTER_LANCZOS4)
cv2.imwrite(f"IO/temp_{desired_image_filename_string}", new_image)


video_input = ffmpeg.input(f"IO/temp_{desired_image_filename_string}",
                           loop = 1, framerate = 1, t = length)
audio_input = ffmpeg.input(f"IO/{desired_audio_filename_string}")

(
    ffmpeg
    .concat(video_input, audio_input, v = 1, a = 1)
    .output(f'IO/{os.path.splitext(desired_audio_filename_string)[0]}.mp4',
            acodec = 'mp3', audio_bitrate = '320k')
    .run(overwrite_output = True)
)

os.remove(f"IO/temp_{desired_image_filename_string}")
