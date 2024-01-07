import os
import sys
import glob
import ffmpeg
import audioread
import cv2
import time
import numpy as np


filenames_mp3 = [os.path.basename(filename) for
                filename in glob.glob("IO/*.mp3")]

filenames_opus = [os.path.basename(filename) for
                filename in glob.glob("IO/*.opus")]

filenames_wav = [os.path.basename(filename) for
                filename in glob.glob("IO/*.wav")]

filenames_flac = [os.path.basename(filename) for
                filename in glob.glob("IO/*.flac")]

audio_filenames = filenames_mp3 + filenames_opus + filenames_wav + filenames_flac


if len(audio_filenames) > 1:

    print("Which audio file do you want to use?")

    for filename in audio_filenames:
        print(f"{audio_filenames.index(filename)+1}: {filename}")

    desired_audio_filename_index = int(input()) - 1
    desired_audio_filename_string = audio_filenames[desired_audio_filename_index]

elif len(audio_filenames) == 1:
    desired_audio_filename_string = audio_filenames[0]

else:
    print("No audio files! Please insert an audio file into the IO directory and run the script again.")
    time.sleep(2)
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
    print("No image files! Please insert an image file into the IO directory and run the script again.")
    time.sleep(2)
    sys.exit()


with open(f"IO/{desired_image_filename_string}", 'rb') as f:
    image_bytes = f.read()

image_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

image_width = image.shape[1]
image_height = image.shape[0]

# the following lines assure that the dimension (width or height) with the least pixels
# is scaled exactly to the amount of pixels on each predefined tuple (1440, 1080 or 720)
# and the other dimension is scaled proportionally. that ensures we don't end up with
# resolutions that are slightly below 1440, 1080 or 720p

min_dimension = min(image_width, image_height)
if min_dimension == image_width:
    if image_width >= 1250:
        ratio = 1440/image_width
        if round(image_height*ratio)%2 == 1:
            width_height = (1440, round(image_height*ratio)+1)
        else:
            width_height = (1440, round(image_height*ratio))
    elif 900 <= image_width < 1250:
        ratio = 1080/image_width
        if round(image_height*ratio)%2 == 1:
            width_height = (1080, round(image_height*ratio)+1)
        else:
            width_height = (1080, round(image_height*ratio))
    else:
        ratio = 720/image_width
        if round(image_height*ratio)%2 == 1:
            width_height = (720, round(image_height*ratio)+1)
        else:
            width_height = (720, round(image_height*ratio))

elif min_dimension == image_height:
    if image_height >= 1250:
        ratio = 1440/image_height
        if round(image_width*ratio)%2 == 1:
            width_height = (round(image_width*ratio)+1, 1440)
        else:
            width_height = (round(image_width*ratio), 1440)
    elif 900 <= image_height < 1250:
        ratio = 1080/image_height
        if round(image_width*ratio)%2 == 1:
            width_height = (round(image_width*ratio)+1, 1080)
        else:
            width_height = (round(image_width*ratio), 1080)
    else:
        ratio = 720/image_height
        if round(image_width*ratio)%2 == 1:
            width_height = (round(image_width*ratio)+1, 720)
        else:
            width_height = (round(image_width*ratio), 720)


resized_image = cv2.resize(image, width_height, interpolation = cv2.INTER_LANCZOS4)

image_extension = os.path.splitext(desired_image_filename_string)[1] # getting image format

success, encoded_image = cv2.imencode(image_extension, resized_image)

if success:
    output_path = f"IO/resize_{desired_image_filename_string}"
    with open(output_path, 'wb') as f:
        f.write(encoded_image)


video_input = ffmpeg.input(f"IO/resize_{desired_image_filename_string}",
                           loop = 1, framerate = 1, t = length)
audio_input = ffmpeg.input(f"IO/{desired_audio_filename_string}")

# the function below sets the arguments for video and audio codecs
# using flac as acodec speeds up the processing time, but the video filesize becomes bigger
# use libopus as acodec to improve filesize (at the cost of slowing down processing time by a factor of 2)

(
    ffmpeg
    .concat(video_input, audio_input, v = 1, a = 1)
    .output(f'IO/{os.path.splitext(desired_audio_filename_string)[0]}.mp4',
            acodec = 'flac')
    .run(overwrite_output = True)
)

os.remove(f"IO/resize_{desired_image_filename_string}")
