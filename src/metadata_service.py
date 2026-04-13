from tinytag import TinyTag
import os
import sys


class MetadataService:
    def __init__(self, audio_path: str):
        self.audio_path = audio_path

    def build_title(self) -> str:
        """Build the video title from audio metadata or filename fallback."""
        try:
            tag = TinyTag.get(self.audio_path)

            if tag.artist and tag.title:
                video_title = f"{tag.artist} - {tag.title}"

        except Exception as e:
            print(f"Warning: Could not read tags ({e}). Using filename as title.")

        if not video_title:
            video_title = os.path.splitext(os.path.basename(self.audio_path))[0]

        print(f"Video title: {video_title}")

        return video_title

    def build_description(self) -> str:
        """Build the video description interactively."""
        description_lines = []

        print("Paste your links and description text below.")
        print("When finished: Press Enter, then Ctrl+Z (Windows) or Ctrl+D (Unix), then Enter again:")

        try:
            user_input = sys.stdin.read().strip()
            if user_input:
                description_lines.append(user_input)
        except EOFError:
            pass

        return "\n".join(description_lines)
