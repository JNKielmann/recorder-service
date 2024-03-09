import abc
import typing

import cv2.typing

VideoFrame: typing.TypeAlias = cv2.typing.MatLike


class VideoSource(abc.ABC):
    """
    Interface for video source that allows capturing frames
    """
    @abc.abstractmethod
    def capture_last_frames(self, num_frames: int) -> list[VideoFrame]:
        """
        Capture the specified number of frames from the video source
        :param num_frames: Number of frames to capture
        :return: List of captured frames
        """
        pass
