import cv2
import numpy as np
import os
import sys
import time


class ImageService:
    def __init__(self, supported_extensions: list = ['jpg', 'png', 'jpeg'], default_io_path: str = None, image_filenames: list = None):
        self.supported_extensions = supported_extensions
        self.default_io_path = default_io_path
        self.image_filenames = image_filenames

    def select_image_file(self) -> str:
        """Prompt user to select an image file and return the selected filename."""
        if len(self.image_filenames) > 1:
            print("Which image file do you want to use?")
            for filename in self.image_filenames:
                print(f"{self.image_filenames.index(filename) + 1}: {filename}")

            selected_index = int(input()) - 1
            return self.image_filenames[selected_index]

        elif len(self.image_filenames) == 1:
            return self.image_filenames[0]

        else:
            print("No image files! Please insert an image file into the IO directory and run the script again.")
            time.sleep(4)
            sys.exit()

    def load_image(self, image_filename: str):
        """Load an image file from disk and return it as a NumPy array."""
        with open(f"{self.default_io_path}/{image_filename}", 'rb') as f:
            image_bytes = f.read()

        image_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image

    def compute_target_size(self, width: int, height: int) -> tuple:
        """Compute the output size preserving aspect ratio and even dimensions."""
        min_dimension = min(width, height)

        if min_dimension == width:
            if width >= 1250:
                target_width = 1440
            elif 900 <= width < 1250:
                target_width = 1080
            else:
                target_width = 720

            ratio = target_width / width
            target_height = round(height * ratio)
        else:
            if height >= 1250:
                target_height = 1440
            elif 900 <= height < 1250:
                target_height = 1080
            else:
                target_height = 720

            ratio = target_height / height
            target_width = round(width * ratio)

        if target_width % 2 == 1:
            target_width += 1
        if target_height % 2 == 1:
            target_height += 1

        return target_width, target_height

    def resize_image(self, image):
        """Resize the image to the target resolution while preserving aspect ratio."""
        image_height, image_width = image.shape[:2]
        target_size = self.compute_target_size(image_width, image_height)
        resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)
        return resized_image

    def save_resized_image(self, image_filename: str, resized_image) -> str:
        """Save the resized image to the IO directory and return the output path."""
        image_extension = os.path.splitext(image_filename)[1]
        output_path = f"{self.default_io_path}/tmp/resized_{image_filename}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        success, encoded_image = cv2.imencode(image_extension, resized_image)

        if not success:
            raise IOError("Failed to encode resized image.")

        with open(output_path, 'wb') as f:
            f.write(encoded_image)

        return output_path
