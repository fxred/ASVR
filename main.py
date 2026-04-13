import os, time, shutil
from glob import glob
from src.image_service import ImageService
from src.metadata_service import MetadataService
from src.render_service import RenderService
from src.audio_service import AudioService
from src.upload_service import UploadService

DEFAULT_IO_PATH = "IO"

SUPPORTED_AUDIO_TYPES = ['mp3', 'opus', 'wav', 'flac']
audio_filenames = [
    os.path.basename(filename) 
    for ext in SUPPORTED_AUDIO_TYPES
    for filename in glob(f"{DEFAULT_IO_PATH}/*.{ext}")
]

audio_service = AudioService(SUPPORTED_AUDIO_TYPES, DEFAULT_IO_PATH, audio_filenames)
selected_audio = audio_service.select_audio_file()

SUPPORTED_IMAGE_TYPES = ['jpg', 'png', 'jpeg']
image_filenames = [
    os.path.basename(filename) 
    for ext in SUPPORTED_IMAGE_TYPES
    for filename in glob(f"{DEFAULT_IO_PATH}/*.{ext}")
]

image_service = ImageService(SUPPORTED_IMAGE_TYPES, DEFAULT_IO_PATH, image_filenames)
selected_image_string = image_service.select_image_file()
image = image_service.load_image(selected_image_string)
resized_image = image_service.resize_image(image)
resized_image = image_service.save_resized_image(selected_image_string, resized_image)

duration = audio_service.get_audio_duration(selected_audio)
render_service = RenderService(audio_path = selected_audio, image_path = resized_image, duration = duration)
video_path = render_service.render()

shutil.rmtree(f"{DEFAULT_IO_PATH}/tmp", ignore_errors=True)

if os.path.exists(video_path):
    print(f"\nRender complete: {video_path}\nHandling video metadata...")

    metadata_service = MetadataService(selected_audio)
    title = metadata_service.build_title()
    description = metadata_service.build_description()

    upload_service = UploadService()
    video_url = upload_service.upload_video(video_path, title, description, 10, 'public')

    if (video_url):
        print("Process finished. You can now view your video link above.")
        print("Close this window manually to exit.")
        while True:
            time.sleep(1)
else:
    print("\n[ERROR] Video file was not found. Rendering may have failed.")
    input("Press Enter to close...")