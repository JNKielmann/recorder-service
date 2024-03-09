from pathlib import Path

import cv2

from recorder_service.core import VideoSource, VideoFrame


class LocalVideoSource(VideoSource):
    """
    Video source that captures frames from a local video file.
    The frames are always captured from the beginning of the video.
    """
    def __init__(self, video_file_path: Path):
        if not video_file_path.exists():
            raise ValueError(f"{video_file_path} does not exist")
        self.video = cv2.VideoCapture(str(video_file_path))
        if not self.video.isOpened():
            raise ValueError(f"Failed to open {video_file_path}")

    def capture_last_frames(self, num_frames: int) -> list[VideoFrame]:
        frames = []
        i = 0
        # Always start capturing from the beginning of the video
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Capture the specified number of frames or until the end of the video
        while i < num_frames:
            ok, frame = self.video.read()
            if not ok:
                break
            frames.append(frame)
            i += 1
        return frames
