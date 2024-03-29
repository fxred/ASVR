# Automated Stillimage Video Rendering (ASVR)

## Objectives / Description

> #### _ASVR_ is a simple and lightweight Python program to render optimized MP4 ~~music~~ videos with a stillimage automatically. It was first designed [by me](https://github.com/fxred) to supply demands of a music-based YouTube channel.
>
>> #### If you run into whatever bugs or glitches within the code or just wanna leave any suggestions, feel free to [email me](mailto:fxr.ed03@gmail.com). Thanks for the attention!

## How to run

* First off, clone [this repository](https://github.com/fxred/ASVR);
* Download and install all the dependencies listed [here](#dependencies).


When you're all set, drag an audio and an image file ([check the list of supported file types](#currently-supported-file-types)) into the **IO** folder inside your directory and, finally, run the **main.py** file.

It's highly recommended to run it within mediums that offer standard user input from the keyboard, otherwise you'll be limited to not being able to properly select which files you want to work with.

If you insert exactly an image and an audio file into the __IO__ folder, the video will be automatically generated by simply running the __main.py__ file.
Otherwise (i.e. you threw multiple audio/image files inside of it), you're gonna be prompted for audio and image select. In this case, choose the desired files by typing, in the terminal, the index associated with the filename shown and press the _ENTER/RETURN_ key afterwards.

If everything goes well, an MP4 video will be generated inside the __IO__ folder, alongside the audio + image files.
If it doesn't, don't panic and try to understand what's being said and what actually happened. Send me an [email](mailto:fxr.ed03@gmail.com) if you have any questions about the program functioning.


## Dependencies

* [FFmpeg](https://ffmpeg.org/download.html)
* [Python 3.7+](https://www.python.org/downloads)


**After**, and **only after** installing Python and FFmpeg properly, you need to install those Python packages in order to properly execute the script:

* [Audioread](https://pypi.org/project/audioread): `pip install audioread`
* [FFmpeg for Python](https://pypi.org/project/ffmpeg-python): `pip install ffmpeg-python`
* [Headless OpenCV](https://pypi.org/project/opencv-python-headless): `pip install opencv-python-headless`
* [NumPy](https://pypi.org/project/numpy/): `pip install numpy`

### Important Note
Apparently, `pip install` isn't working properly to install Python packages in some machines, so keep in mind the commands above might not work in some environments (especially if you recently installed Python). In this case, try swapping `pip install` for `python -m pip install`, `python3 -m pip install` or even `py -m pip install` if the usual pip command doesn't work.

![python -m pip install](wwpLI.png "python -m pip install python -m pip install python -m pip install python -m pip install python -m pip install python -m pip install")

## Currently supported file types

### Audio files:

__MP3__ (.mp3) <br>
__FLAC__ (.flac) <br>
__WAVE__ (.wav) <br>
__OPUS__ (.opus)

### Image files:

__JPG__ (.jpg) <br>
__PNG__ (.png)

## Warnings

* Do **not** modify the directory structure apart from the inside of the __IO__ folder unless you know exactly what you're doing;
* Make sure you correctly installed all the dependencies listed above in your machine before running the script. They're all vital for the proper code functioning.