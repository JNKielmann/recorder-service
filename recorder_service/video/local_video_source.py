from pathlib import Path

import cv2

from recorder_service.core import VideoSource, VideoFrame


class LocalVideoSource(VideoSource):
    def capture_last_frames(self, num_frames: int) -> list[VideoFrame]:
        print(f"Capturing {num_frames} frames from video")
        return ["video_frame"] * num_frames
