import audioread
import sys
import time


class AudioService:
    def __init__(self, supported_extensions: list = ['mp3', 'opus', 'wav', 'flac'], default_io_path: str = None, audio_filenames: list = None):
        self.supported_extensions = supported_extensions
        self.default_io_path = default_io_path
        self.audio_filenames = audio_filenames

    def select_audio_file(self) -> str:
        """Prompts user to select an audio file and return the selected filename."""
        if len(self.audio_filenames) > 1:
            print("Which audio file do you want to use?")
            for filename in self.audio_filenames:
                print(f"{self.audio_filenames.index(filename) + 1}: {filename}")

            selected_index = int(input()) - 1
            return f"{self.default_io_path}/{self.audio_filenames[selected_index]}"

        elif len(self.audio_filenames) == 1:
            return f"{self.default_io_path}/{self.audio_filenames[0]}"

        else:
            print("No audio files! Please insert an audio file into the IO directory and run the script again.")
            time.sleep(4)
            sys.exit()

    def get_audio_duration(self, audio_filename: str) -> float:
        """Get the duration of the specified audio file."""
        with audioread.audio_open(audio_filename) as f:
            return f.duration
