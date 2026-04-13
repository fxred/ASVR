import ffmpeg
import platform
import subprocess
import time
import os


class RenderService:
    def __init__(self, audio_path: str, image_path: str, duration: float, audio_codec: str = "flac"):
        self.audio_path = audio_path
        self.image_path = image_path
        self.duration = duration
        self.audio_codec = audio_codec

    @staticmethod
    def get_gpu_encoder() -> str:
        os_name = platform.system()
        hardware_info = ""

        try:
            if os_name == "Windows":
                hardware_info = subprocess.check_output(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        "Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty Name"
                    ],
                    text=True
                ).lower()
            elif os_name == "Linux":
                hardware_info = subprocess.check_output(["lspci"], text=True).lower()
            elif os_name == "Darwin":
                hardware_info = subprocess.check_output(
                    ["system_profiler", "SPDisplaysDataType"],
                    text=True
                ).lower()
                return "h264_videotoolbox"
        except Exception as e:
            print(f"Warning: Could not auto-detect GPU (Error: {e}). Defaulting to CPU.")
            time.sleep(2)
            return "libx264"

        if "nvidia" in hardware_info:
            return "h264_nvenc"
        if "amd" in hardware_info or "radeon" in hardware_info:
            return "h264_amf"
        if "intel" in hardware_info:
            return "h264_qsv"

        print("Warning: GPU manufacturer not recognized. Defaulting to CPU.")
        time.sleep(2)
        return "libx264"

    def render(self) -> str:
        video_input = ffmpeg.input(
            self.image_path,
            loop=1,
            framerate=1,
            t=self.duration,
        )
        audio_input = ffmpeg.input(self.audio_path)

        output_path = f"{os.path.splitext(self.audio_path)[0]}.mp4"

        (
            ffmpeg
            .concat(video_input, audio_input, v=1, a=1)
            .output(output_path, vcodec=self.get_gpu_encoder(), acodec=self.audio_codec)
            .run(overwrite_output=True)
        )

        return output_path
